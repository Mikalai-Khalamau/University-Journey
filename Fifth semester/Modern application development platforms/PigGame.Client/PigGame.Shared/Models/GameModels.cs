namespace PigGame.Shared.Models;

public enum GamePhase
{
    Waiting,
    Playing,
    Finished
}

public enum GameMode
{
    Pig = 0,
    BigPig = 1,
    Jackpot = 2
}

public static class GameModeExtensions
{
    public static string DisplayName(this GameMode mode) => mode switch
    {
        GameMode.BigPig => "Большая свинья",
        GameMode.Jackpot => "Джекпот",
        _ => "Свинья"
    };

    public static string Description(this GameMode mode) => mode switch
    {
        GameMode.BigPig =>
            "Две кости. Одна единица — ход сгорает, 1-1 — 25 очков, другой дубль — двойная сумма. Цель — 100 очков.",
        GameMode.Jackpot =>
            "Одна кость. Каждая выпавшая единица пополняет кон: по 1 очку с каждого игрока. Первый, кто наберёт 100 очков, забирает кон.",
        _ =>
            "Одна кость. Единица — ход сгорает. Первый, кто наберёт 100 очков, побеждает."
    };
}

public class Player
{
    public string ConnectionId { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public int TotalScore { get; set; }
    public bool IsReady { get; set; }
}

public class ChatMessage
{
    public string PlayerName { get; set; } = string.Empty;
    public string Text { get; set; } = string.Empty;
    public DateTime SentAt { get; set; } = DateTime.UtcNow;
}

public class GameState
{
    public const int WinScore = 100;
    public const int MinPlayers = 2;
    public const int MaxPlayers = 6;
    public const int MaxChatMessages = 50;
    public const int JackpotStake = 10;
    public const int JackpotContribution = JackpotStake / 10;

    public string GameId { get; set; } = string.Empty;
    public GameMode Mode { get; set; } = GameMode.Pig;
    public List<Player> Players { get; set; } = new();
    public GamePhase Phase { get; set; } = GamePhase.Waiting;
    public int CurrentPlayerIndex { get; set; }
    public int TurnScore { get; set; }
    public int LastDiceRoll { get; set; }
    public int SecondDiceRoll { get; set; }
    public int RollNumber { get; set; }
    public int Pot { get; set; }
    public int WinnerPrize { get; set; }
    public string WinnerName { get; set; } = string.Empty;
    public List<ChatMessage> Chat { get; set; } = new();

    public bool UsesTwoDice => Mode == GameMode.BigPig;

    public bool IsGameOver => Phase == GamePhase.Finished;

    public bool IsStarted => Phase == GamePhase.Playing;

    public bool IsWaitingForPlayers => Phase == GamePhase.Waiting;

    public bool CanStart =>
        Phase == GamePhase.Waiting &&
        Players.Count >= MinPlayers &&
        Players.All(p => p.IsReady);

    public Player? CurrentPlayer =>
        Players.Count == 0 ? null : Players[Math.Clamp(CurrentPlayerIndex, 0, Players.Count - 1)];
}
