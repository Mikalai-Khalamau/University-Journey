using Microsoft.AspNetCore.SignalR;
using PigGame.Server.GameLogic;
using PigGame.Shared.Contracts;
using PigGame.Shared.Models;

namespace PigGame.Server.Hubs;

// Требование: строго типизированный Hub
public class GameHub : Hub<IGameClient>
{
    private readonly PigGameEngine _engine;
    private readonly ILogger<GameHub> _logger;

    public GameHub(PigGameEngine engine, ILogger<GameHub> logger)
    {
        _engine = engine;
        _logger = logger;
    }

    public async Task CreateGame(string playerName, GameMode mode)
    {
        if (!Enum.IsDefined(mode))
            mode = GameMode.Pig;

        var gameId = GenerateGameId();

        // Требование: Groups позволяют проводить несколько игр одновременно
        await Groups.AddToGroupAsync(Context.ConnectionId, gameId);

        var state = _engine.CreateRoom(gameId, Context.ConnectionId, playerName, mode);
        _logger.LogInformation(
            "Создана комната {GameId} ({Mode}) игроком {PlayerName} ({ConnectionId})",
            gameId, mode.DisplayName(), state.Players[0].Name, Context.ConnectionId);

        await Clients.Group(gameId).UpdateGameState(state);
        await Clients.Caller.ShowMessage($"Комната создана. ID: {gameId}. Передайте его второму игроку.");
    }

    public async Task JoinGame(string gameId, string playerName)
    {
        gameId = NormalizeGameId(gameId);

        var result = _engine.JoinRoom(gameId, Context.ConnectionId, playerName);
        if (!result.IsSuccess || result.State is null)
        {
            await Clients.Caller.ShowMessage(result.Message);
            return;
        }

        await Groups.AddToGroupAsync(Context.ConnectionId, gameId);
        _logger.LogInformation(
            "Игрок {PlayerName} ({ConnectionId}) вошёл в комнату {GameId}",
            playerName, Context.ConnectionId, gameId);

        await Clients.Group(gameId).UpdateGameState(result.State);
        await Clients.Group(gameId).ShowMessage(result.Message);
    }

    public async Task SetReady(string gameId, bool isReady)
    {
        gameId = NormalizeGameId(gameId);
        var result = _engine.SetReady(gameId, Context.ConnectionId, isReady);
        await SendResultAsync(gameId, result);
    }

    public async Task RollDice(string gameId)
    {
        gameId = NormalizeGameId(gameId);
        var result = _engine.RollDice(gameId, Context.ConnectionId);
        await SendResultAsync(gameId, result);
    }

    public async Task Hold(string gameId)
    {
        gameId = NormalizeGameId(gameId);
        var result = _engine.Hold(gameId, Context.ConnectionId);
        await SendResultAsync(gameId, result);
    }

    public async Task SendChat(string gameId, string text)
    {
        gameId = NormalizeGameId(gameId);
        var result = _engine.SendChat(gameId, Context.ConnectionId, text);

        if (!result.IsSuccess || result.State is null)
        {
            await Clients.Caller.ShowMessage(result.Message);
            return;
        }

        await Clients.Group(gameId).UpdateGameState(result.State);
    }

    public override async Task OnDisconnectedAsync(Exception? exception)
    {
        foreach (var (gameId, state, playerName) in _engine.RemovePlayer(Context.ConnectionId))
        {
            _logger.LogInformation(
                "Игрок {PlayerName} ({ConnectionId}) покинул комнату {GameId}",
                playerName, Context.ConnectionId, gameId);

            await Clients.Group(gameId).UpdateGameState(state);
            await Clients.Group(gameId).ShowMessage($"{playerName} покинул игру.");
        }

        await base.OnDisconnectedAsync(exception);
    }

    private async Task SendResultAsync(string gameId, GameActionResult result)
    {
        _logger.LogInformation("Комната {GameId}: {Message}", gameId, result.Message);

        if (result.IsSuccess && result.State is not null)
        {
            await Clients.Group(gameId).UpdateGameState(result.State);
            await Clients.Group(gameId).ShowMessage(result.Message);
        }
        else
        {
            await Clients.Caller.ShowMessage(result.Message);
        }
    }

    private string GenerateGameId()
    {
        string gameId;
        do
        {
            gameId = Guid.NewGuid().ToString("N")[..6];
        }
        while (_engine.RoomExists(gameId));

        return gameId;
    }

    private static string NormalizeGameId(string? gameId) =>
        (gameId ?? string.Empty).Trim().ToLowerInvariant();
}
