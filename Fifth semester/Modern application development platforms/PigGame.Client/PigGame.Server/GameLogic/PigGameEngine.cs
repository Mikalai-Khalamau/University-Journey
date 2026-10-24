using PigGame.Shared.Models;

namespace PigGame.Server.GameLogic;

// Требование: бизнес-логика игры описана в отдельном классе
public class PigGameEngine
{
    private readonly Dictionary<string, GameState> _rooms = new();
    private readonly object _sync = new();
    private readonly IDiceRoller _dice;

    public PigGameEngine(IDiceRoller dice)
    {
        _dice = dice;
    }

    public bool RoomExists(string gameId)
    {
        lock (_sync)
        {
            return _rooms.ContainsKey(gameId);
        }
    }

    public GameState CreateRoom(
        string gameId,
        string connectionId,
        string playerName,
        GameMode mode = GameMode.Pig)
    {
        lock (_sync)
        {
            var state = new GameState
            {
                GameId = gameId,
                Mode = mode
            };

            state.Players.Add(new Player
            {
                ConnectionId = connectionId,
                Name = NormalizeName(playerName),
                IsReady = false
            });

            _rooms[gameId] = state;
            return state;
        }
    }

    public GameState? GetRoom(string gameId)
    {
        lock (_sync)
        {
            return _rooms.TryGetValue(gameId, out var state) ? state : null;
        }
    }

    public GameActionResult JoinRoom(string gameId, string connectionId, string playerName)
    {
        lock (_sync)
        {
            if (!_rooms.TryGetValue(gameId, out var state))
                return GameActionResult.Failure(null, "Комната не найдена.");

            if (state.Phase != GamePhase.Waiting)
                return GameActionResult.Failure(state, "Игра уже началась или завершена.");

            if (state.Players.Any(p => p.ConnectionId == connectionId))
                return GameActionResult.Failure(state, "Вы уже находитесь в этой комнате.");

            if (state.Players.Count >= GameState.MaxPlayers)
                return GameActionResult.Failure(state, $"В комнате может быть не больше {GameState.MaxPlayers} игроков.");

            var name = NormalizeName(playerName);
            if (state.Players.Any(p => string.Equals(p.Name, name, StringComparison.OrdinalIgnoreCase)))
                name = $"{name} {state.Players.Count + 1}";

            state.Players.Add(new Player
            {
                ConnectionId = connectionId,
                Name = name,
                IsReady = false
            });

            return GameActionResult.Success(state, $"{name} присоединился к игре.");
        }
    }

    public GameActionResult SetReady(string gameId, string connectionId, bool isReady)
    {
        lock (_sync)
        {
            if (!_rooms.TryGetValue(gameId, out var state))
                return GameActionResult.Failure(null, "Комната не найдена.");

            var player = state.Players.FirstOrDefault(p => p.ConnectionId == connectionId);
            if (player is null)
                return GameActionResult.Failure(state, "Вы не находитесь в этой комнате.");

            if (state.Phase != GamePhase.Waiting)
                return GameActionResult.Failure(state, "Игра уже началась или завершена.");

            player.IsReady = isReady;

            if (state.CanStart)
            {
                state.Phase = GamePhase.Playing;
                state.CurrentPlayerIndex = 0;
                state.TurnScore = 0;
                state.LastDiceRoll = 0;
                state.SecondDiceRoll = 0;
                state.RollNumber = 0;
                state.Pot = 0;
                state.WinnerPrize = 0;
                state.WinnerName = string.Empty;

                return GameActionResult.Success(
                    state,
                    $"Все игроки готовы. Игра «{state.Mode.DisplayName()}» началась! Ход: {state.CurrentPlayer!.Name}.");
            }

            var waiting = state.Players.Count < GameState.MinPlayers
                ? $"Нужно игроков: {state.Players.Count}/{GameState.MinPlayers}."
                : $"Осталось не готовы: {state.Players.Count(p => !p.IsReady)}.";

            return GameActionResult.Success(
                state,
                $"{player.Name}: {(isReady ? "готов" : "не готов")}. {waiting}");
        }
    }

    public GameActionResult RollDice(string gameId, string connectionId)
    {
        lock (_sync)
        {
            if (!_rooms.TryGetValue(gameId, out var state))
                return GameActionResult.Failure(null, "Комната не найдена.");

            var error = ValidateTurn(state, connectionId);
            if (error is not null)
                return GameActionResult.Failure(state, error);

            var currentPlayer = state.CurrentPlayer!;

            if (state.UsesTwoDice)
            {
                state.LastDiceRoll = Math.Clamp(_dice.Roll(), 1, 6);
                state.SecondDiceRoll = Math.Clamp(_dice.Roll(), 1, 6);
            }
            else
            {
                state.LastDiceRoll = Math.Clamp(_dice.Roll(), 1, 6);
                state.SecondDiceRoll = 0;
            }

            state.RollNumber++;

            return state.Mode == GameMode.BigPig
                ? RollBigPig(state, currentPlayer)
                : RollSingleDie(state, currentPlayer);
        }
    }

    public GameActionResult Hold(string gameId, string connectionId)
    {
        lock (_sync)
        {
            if (!_rooms.TryGetValue(gameId, out var state))
                return GameActionResult.Failure(null, "Комната не найдена.");

            var error = ValidateTurn(state, connectionId);
            if (error is not null)
                return GameActionResult.Failure(state, error);

            if (state.TurnScore == 0)
                return GameActionResult.Failure(state, "Сначала бросьте кость.");

            var currentPlayer = state.CurrentPlayer!;
            var earned = state.TurnScore;
            currentPlayer.TotalScore += earned;
            state.TurnScore = 0;

            if (currentPlayer.TotalScore >= GameState.WinScore)
            {
                state.Phase = GamePhase.Finished;
                state.WinnerName = currentPlayer.Name;

                var jackpotWinner = string.Empty;
                if (state.Mode == GameMode.Jackpot)
                {
                    state.WinnerPrize = state.Pot;
                    state.Pot = 0;

                    if (state.WinnerPrize > 0)
                        jackpotWinner = $" Джекпот достаётся победителю: {state.WinnerPrize}.";
                }

                return GameActionResult.Success(
                    state,
                    $"{currentPlayer.Name} победил, набрав {currentPlayer.TotalScore} очков!{jackpotWinner}");
            }

            NextTurn(state);
            return GameActionResult.Success(
                state,
                $"{currentPlayer.Name} забрал {earned} очк. Всего: {currentPlayer.TotalScore}. Ход переходит.");
        }
    }

    public GameActionResult SendChat(string gameId, string connectionId, string text)
    {
        lock (_sync)
        {
            if (!_rooms.TryGetValue(gameId, out var state))
                return GameActionResult.Failure(null, "Комната не найдена.");

            var player = state.Players.FirstOrDefault(p => p.ConnectionId == connectionId);
            if (player is null)
                return GameActionResult.Failure(state, "Вы не находитесь в этой комнате.");

            text = (text ?? string.Empty).Trim();
            if (text.Length == 0)
                return GameActionResult.Failure(state, "Сообщение не может быть пустым.");

            if (text.Length > 300)
                text = text[..300];

            state.Chat.Add(new ChatMessage
            {
                PlayerName = player.Name,
                Text = text,
                SentAt = DateTime.UtcNow
            });

            if (state.Chat.Count > GameState.MaxChatMessages)
                state.Chat.RemoveRange(0, state.Chat.Count - GameState.MaxChatMessages);

            return GameActionResult.Success(state, string.Empty);
        }
    }

    public List<(string GameId, GameState State, string PlayerName)> RemovePlayer(string connectionId)
    {
        lock (_sync)
        {
            var result = new List<(string GameId, GameState State, string PlayerName)>();

            foreach (var (gameId, state) in _rooms.ToList())
            {
                var player = state.Players.FirstOrDefault(p => p.ConnectionId == connectionId);
                if (player is null)
                    continue;

                var index = state.Players.IndexOf(player);
                state.Players.RemoveAt(index);

                if (state.Players.Count == 0)
                {
                    _rooms.Remove(gameId);
                    continue;
                }

                if (state.Phase == GamePhase.Playing && state.Players.Count < GameState.MinPlayers)
                {
                    state.Phase = GamePhase.Waiting;
                    state.CurrentPlayerIndex = 0;
                    state.TurnScore = 0;
                    state.LastDiceRoll = 0;
                    state.SecondDiceRoll = 0;
                    state.RollNumber = 0;
                    state.Pot = 0;
                    state.WinnerPrize = 0;
                    state.WinnerName = string.Empty;

                    foreach (var remaining in state.Players)
                        remaining.IsReady = false;
                }
                else
                {
                    if (index < state.CurrentPlayerIndex)
                    {
                        state.CurrentPlayerIndex--;
                    }
                    else if (index == state.CurrentPlayerIndex)
                    {
                        state.TurnScore = 0;
                    }

                    if (state.CurrentPlayerIndex >= state.Players.Count)
                        state.CurrentPlayerIndex = 0;
                }

                result.Add((gameId, state, player.Name));
            }

            return result;
        }
    }

    private static GameActionResult RollSingleDie(GameState state, Player currentPlayer)
    {
        var roll = state.LastDiceRoll;

        if (roll == 1)
        {
            var lost = state.TurnScore;
            state.TurnScore = 0;

            var potMessage = string.Empty;
            if (state.Mode == GameMode.Jackpot)
            {
                var contribution = state.Players.Count * GameState.JackpotContribution;
                state.Pot += contribution;
                potMessage = $" Кон пополнен на {contribution}, теперь в кону {state.Pot}.";
            }

            NextTurn(state);
            return GameActionResult.Success(
                state,
                $"{currentPlayer.Name} выбросил 1 и потерял {lost} очк. Ход переходит.{potMessage}");
        }

        state.TurnScore += roll;
        return GameActionResult.Success(
            state,
            $"{currentPlayer.Name} выбросил {roll}. Очки за ход: {state.TurnScore}.");
    }

    private static GameActionResult RollBigPig(GameState state, Player currentPlayer)
    {
        var first = state.LastDiceRoll;
        var second = state.SecondDiceRoll;

        if (first == 1 && second == 1)
        {
            state.TurnScore += 25;
            return GameActionResult.Success(
                state,
                $"{currentPlayer.Name} выбросил 1-1 и получил 25 очков. Очки за ход: {state.TurnScore}.");
        }

        if (first == 1 || second == 1)
        {
            var lost = state.TurnScore;
            state.TurnScore = 0;
            NextTurn(state);
            return GameActionResult.Success(
                state,
                $"{currentPlayer.Name} выбросил {first}-{second} — единица. Потеряно {lost} очк. Ход переходит.");
        }

        var points = first == second
            ? 2 * (first + second)
            : first + second;

        state.TurnScore += points;

        var doubleMessage = first == second ? " (дубль)" : string.Empty;
        return GameActionResult.Success(
            state,
            $"{currentPlayer.Name} выбросил {first}-{second}{doubleMessage} и получил {points} очков. Очки за ход: {state.TurnScore}.");
    }

    private static string? ValidateTurn(GameState state, string connectionId)
    {
        if (state.Phase == GamePhase.Finished)
            return "Игра уже окончена.";

        if (state.Phase == GamePhase.Waiting)
            return "Игра ещё не началась. Дождитесь готовности всех игроков.";

        var currentPlayer = state.CurrentPlayer;
        if (currentPlayer is null || currentPlayer.ConnectionId != connectionId)
            return "Сейчас не ваш ход!";

        return null;
    }

    private static void NextTurn(GameState state)
    {
        if (state.Players.Count == 0)
            return;

        state.CurrentPlayerIndex = (state.CurrentPlayerIndex + 1) % state.Players.Count;
    }

    private static string NormalizeName(string? name)
    {
        name = name?.Trim();
        return string.IsNullOrWhiteSpace(name) ? "Игрок" : name;
    }
}
