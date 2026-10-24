using PigGame.Server.GameLogic;
using PigGame.Shared.Models;

namespace PigGame.Tests;

public class PigGameEngineTests
{
    private const string GameId = "room1";
    private const string AliceId = "c1";
    private const string BobId = "c2";

    [Fact]
    public void CreateRoom_AddsPlayerAndWaitingPhase()
    {
        var engine = CreateEngine();

        var state = engine.CreateRoom(GameId, AliceId, "Alice");

        Assert.Equal(GamePhase.Waiting, state.Phase);
        Assert.Equal(GameId, state.GameId);
        Assert.Single(state.Players);
        Assert.Equal("Alice", state.Players[0].Name);
        Assert.False(state.Players[0].IsReady);
        Assert.True(engine.RoomExists(GameId));
    }

    [Fact]
    public void CreateRoom_StoresSelectedMode()
    {
        var engine = CreateEngine();

        var state = engine.CreateRoom(GameId, AliceId, "Alice", GameMode.BigPig);

        Assert.Equal(GameMode.BigPig, state.Mode);
        Assert.True(state.UsesTwoDice);
    }

    [Fact]
    public void JoinRoom_AddsSecondPlayer()
    {
        var engine = CreateEngine();
        engine.CreateRoom(GameId, AliceId, "Alice");

        var result = engine.JoinRoom(GameId, BobId, "Bob");

        Assert.True(result.IsSuccess);
        Assert.NotNull(result.State);
        Assert.Equal(2, result.State!.Players.Count);
        Assert.Contains("Bob", result.Message);
    }

    [Fact]
    public void JoinRoom_RejectsUnknownRoom()
    {
        var engine = CreateEngine();

        var result = engine.JoinRoom("missing", BobId, "Bob");

        Assert.False(result.IsSuccess);
        Assert.Contains("не найдена", result.Message);
    }

    [Fact]
    public void Game_StartsOnlyWhenAllPlayersAreReady()
    {
        var engine = CreateEngine();
        engine.CreateRoom(GameId, AliceId, "Alice");
        engine.JoinRoom(GameId, BobId, "Bob");

        var aliceReady = engine.SetReady(GameId, AliceId, true);
        Assert.True(aliceReady.IsSuccess);
        Assert.Equal(GamePhase.Waiting, aliceReady.State!.Phase);

        var bobReady = engine.SetReady(GameId, BobId, true);
        Assert.True(bobReady.IsSuccess);
        Assert.Equal(GamePhase.Playing, bobReady.State!.Phase);
        Assert.Equal(0, bobReady.State.CurrentPlayerIndex);
        Assert.Equal("Alice", bobReady.State.CurrentPlayer!.Name);
    }

    [Fact]
    public void JoinRoom_RejectsJoinAfterStart()
    {
        var engine = CreateEngine();
        CreateStartedGame(engine);

        var result = engine.JoinRoom(GameId, "c3", "Carol");

        Assert.False(result.IsSuccess);
        Assert.Contains("уже началась", result.Message);
    }

    [Fact]
    public void RollDice_FailsBeforeStart()
    {
        var engine = CreateEngine();
        engine.CreateRoom(GameId, AliceId, "Alice");
        engine.JoinRoom(GameId, BobId, "Bob");

        var result = engine.RollDice(GameId, AliceId);

        Assert.False(result.IsSuccess);
        Assert.Contains("не началась", result.Message);
    }

    [Fact]
    public void RollDice_AddsRollToTurnScore()
    {
        var engine = CreateEngine(6);
        CreateStartedGame(engine);

        var result = engine.RollDice(GameId, AliceId);

        Assert.True(result.IsSuccess);
        Assert.Equal(6, result.State!.TurnScore);
        Assert.Equal(6, result.State.LastDiceRoll);
        Assert.Equal(0, result.State.SecondDiceRoll);
        Assert.Equal(1, result.State.RollNumber);
        Assert.Equal(AliceId, result.State.CurrentPlayer!.ConnectionId);
    }

    [Fact]
    public void RollDice_OneResetsTurnScoreAndPassesTurn()
    {
        var engine = CreateEngine(5, 1);
        var state = CreateStartedGame(engine);
        engine.RollDice(GameId, AliceId);

        var result = engine.RollDice(GameId, AliceId);

        Assert.True(result.IsSuccess);
        Assert.Equal(0, state.TurnScore);
        Assert.Equal(1, state.LastDiceRoll);
        Assert.Equal(BobId, state.CurrentPlayer!.ConnectionId);
        Assert.Contains("потерял 5", result.Message);
    }

    [Fact]
    public void BigPig_SingleOneResetsTurnScoreAndPassesTurn()
    {
        var engine = CreateEngine(3, 4, 1, 5);
        var state = CreateStartedGame(engine, GameMode.BigPig);

        engine.RollDice(GameId, AliceId);
        Assert.Equal(7, state.TurnScore);
        Assert.Equal(4, state.SecondDiceRoll);

        var result = engine.RollDice(GameId, AliceId);

        Assert.True(result.IsSuccess);
        Assert.Equal(0, state.TurnScore);
        Assert.Equal(1, state.LastDiceRoll);
        Assert.Equal(5, state.SecondDiceRoll);
        Assert.Equal(BobId, state.CurrentPlayer!.ConnectionId);
        Assert.Contains("1-5", result.Message);
        Assert.Contains("Потеряно 7", result.Message);
    }

    [Fact]
    public void BigPig_DoubleOneGives25AndKeepsTurn()
    {
        var engine = CreateEngine(1, 1);
        var state = CreateStartedGame(engine, GameMode.BigPig);

        var result = engine.RollDice(GameId, AliceId);

        Assert.True(result.IsSuccess);
        Assert.Equal(25, state.TurnScore);
        Assert.Equal(AliceId, state.CurrentPlayer!.ConnectionId);
        Assert.Contains("1-1", result.Message);
        Assert.Contains("25", result.Message);
    }

    [Fact]
    public void BigPig_OtherDoubleAndRegularRollFollowRulebookExample()
    {
        var engine = CreateEngine(5, 5, 2, 6);
        var state = CreateStartedGame(engine, GameMode.BigPig);

        engine.RollDice(GameId, AliceId);
        Assert.Equal(20, state.TurnScore);

        var result = engine.RollDice(GameId, AliceId);

        Assert.True(result.IsSuccess);
        Assert.Equal(28, state.TurnScore);
        Assert.Equal(AliceId, state.CurrentPlayer!.ConnectionId);
        Assert.Contains("2-6", result.Message);
        Assert.Contains("8", result.Message);
    }

    [Fact]
    public void Jackpot_RollingOneAddsContributionFromEveryPlayer()
    {
        var engine = CreateEngine(1);
        var state = CreateStartedGame(engine, GameMode.Jackpot);

        var result = engine.RollDice(GameId, AliceId);

        Assert.True(result.IsSuccess);
        Assert.Equal(0, state.TurnScore);
        Assert.Equal(2, state.Pot);
        Assert.Equal(state.Players.Count * GameState.JackpotContribution, state.Pot);
        Assert.Equal(BobId, state.CurrentPlayer!.ConnectionId);
        Assert.Contains("Кон пополнен", result.Message);
    }

    [Fact]
    public void Jackpot_WinnerTakesPot()
    {
        var engine = CreateEngine(4);
        var state = CreateStartedGame(engine, GameMode.Jackpot);
        state.Players[0].TotalScore = 96;
        state.Pot = 10;

        engine.RollDice(GameId, AliceId);
        var result = engine.Hold(GameId, AliceId);

        Assert.True(result.IsSuccess);
        Assert.Equal(GamePhase.Finished, state.Phase);
        Assert.Equal("Alice", state.WinnerName);
        Assert.Equal(10, state.WinnerPrize);
        Assert.Equal(0, state.Pot);
        Assert.Contains("Джекпот", result.Message);
    }

    [Fact]
    public void RollDice_RejectsOutOfTurn()
    {
        var engine = CreateEngine(3);
        CreateStartedGame(engine);

        var result = engine.RollDice(GameId, BobId);

        Assert.False(result.IsSuccess);
        Assert.Contains("не ваш ход", result.Message);
    }

    [Fact]
    public void Hold_AddsTurnScoreAndPassesTurn()
    {
        var engine = CreateEngine(4);
        var state = CreateStartedGame(engine);
        engine.RollDice(GameId, AliceId);

        var result = engine.Hold(GameId, AliceId);

        Assert.True(result.IsSuccess);
        Assert.Equal(4, state.Players[0].TotalScore);
        Assert.Equal(0, state.TurnScore);
        Assert.Equal(BobId, state.CurrentPlayer!.ConnectionId);
    }

    [Fact]
    public void Hold_FailsWithoutRoll()
    {
        var engine = CreateEngine();
        CreateStartedGame(engine);

        var result = engine.Hold(GameId, AliceId);

        Assert.False(result.IsSuccess);
        Assert.Contains("Сначала бросьте", result.Message);
    }

    [Fact]
    public void Hold_ReachingWinScoreFinishesGame()
    {
        var engine = CreateEngine(4);
        var state = CreateStartedGame(engine);
        state.Players[0].TotalScore = 96;

        engine.RollDice(GameId, AliceId);
        var result = engine.Hold(GameId, AliceId);

        Assert.True(result.IsSuccess);
        Assert.Equal(GamePhase.Finished, state.Phase);
        Assert.True(state.IsGameOver);
        Assert.Equal("Alice", state.WinnerName);
        Assert.Equal(100, state.Players[0].TotalScore);
    }

    [Fact]
    public void SendChat_StoresTrimmedMessage()
    {
        var engine = CreateEngine();
        var state = engine.CreateRoom(GameId, AliceId, "Alice");

        var result = engine.SendChat(GameId, AliceId, "  Привет  ");

        Assert.True(result.IsSuccess);
        var message = Assert.Single(state.Chat);
        Assert.Equal("Alice", message.PlayerName);
        Assert.Equal("Привет", message.Text);
    }

    [Fact]
    public void SendChat_RejectsEmptyMessage()
    {
        var engine = CreateEngine();
        var state = engine.CreateRoom(GameId, AliceId, "Alice");

        var result = engine.SendChat(GameId, AliceId, "   ");

        Assert.False(result.IsSuccess);
        Assert.Empty(state.Chat);
    }

    [Fact]
    public void SendChat_KeepsOnlyLastMessages()
    {
        var engine = CreateEngine();
        var state = engine.CreateRoom(GameId, AliceId, "Alice");

        for (var i = 0; i < GameState.MaxChatMessages + 5; i++)
            engine.SendChat(GameId, AliceId, $"message {i}");

        Assert.Equal(GameState.MaxChatMessages, state.Chat.Count);
        Assert.Equal($"message {GameState.MaxChatMessages + 4}", state.Chat[^1].Text);
    }

    [Fact]
    public void RemovePlayer_DuringGameReturnsRoomToLobby()
    {
        var engine = CreateEngine(5);
        CreateStartedGame(engine);
        engine.RollDice(GameId, AliceId);

        var removed = engine.RemovePlayer(BobId);

        var room = Assert.Single(removed);
        Assert.Equal(GameId, room.GameId);
        Assert.Equal(GamePhase.Waiting, room.State.Phase);
        Assert.Single(room.State.Players);
        Assert.False(room.State.Players[0].IsReady);
        Assert.Equal(0, room.State.TurnScore);
    }

    [Fact]
    public void RemoveLastPlayer_DeletesRoom()
    {
        var engine = CreateEngine();
        engine.CreateRoom(GameId, AliceId, "Alice");
        engine.JoinRoom(GameId, BobId, "Bob");

        engine.RemovePlayer(AliceId);
        engine.RemovePlayer(BobId);

        Assert.False(engine.RoomExists(GameId));
    }

    private static PigGameEngine CreateEngine(params int[] rolls) =>
        new(new SequenceDiceRoller(rolls));

    private static GameState CreateStartedGame(PigGameEngine engine, GameMode mode = GameMode.Pig)
    {
        engine.CreateRoom(GameId, AliceId, "Alice", mode);
        var join = engine.JoinRoom(GameId, BobId, "Bob");
        Assert.True(join.IsSuccess);

        var aliceReady = engine.SetReady(GameId, AliceId, true);
        Assert.True(aliceReady.IsSuccess);
        Assert.Equal(GamePhase.Waiting, aliceReady.State!.Phase);

        var bobReady = engine.SetReady(GameId, BobId, true);
        Assert.True(bobReady.IsSuccess);
        Assert.Equal(GamePhase.Playing, bobReady.State!.Phase);

        return bobReady.State;
    }

    private sealed class SequenceDiceRoller : IDiceRoller
    {
        private readonly Queue<int> _rolls;

        public SequenceDiceRoller(IEnumerable<int> rolls)
        {
            _rolls = new Queue<int>(rolls);
        }

        public int Roll() => _rolls.Count > 0 ? _rolls.Dequeue() : 1;
    }
}
