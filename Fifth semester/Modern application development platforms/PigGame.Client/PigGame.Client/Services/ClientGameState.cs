using PigGame.Shared.Models;

namespace PigGame.Client.Services;

public class ClientGameState
{
    public string MyConnectionId { get; set; } = string.Empty;
    public string MyName { get; set; } = string.Empty;
    public string CurrentGameId { get; set; } = string.Empty;
    public GameState? CurrentState { get; set; }
    public List<string> Messages { get; } = new();

    public Player? Me =>
        CurrentState?.Players.FirstOrDefault(p => p.ConnectionId == MyConnectionId);

    public bool IsMyTurn =>
        CurrentState is { Phase: GamePhase.Playing, CurrentPlayer: { } player } &&
        !string.IsNullOrEmpty(MyConnectionId) &&
        player.ConnectionId == MyConnectionId;

    public bool IsWaitingForPlayers => CurrentState?.IsWaitingForPlayers ?? true;

    public IReadOnlyList<ChatMessage> ChatMessages =>
        CurrentState is { } state ? state.Chat : Array.Empty<ChatMessage>();

    public void AddMessage(string message)
    {
        Messages.Add(message);
        if (Messages.Count > 8)
            Messages.RemoveAt(0);
    }
}
