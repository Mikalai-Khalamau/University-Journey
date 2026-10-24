using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.SignalR.Client;
using PigGame.Shared.Models;

namespace PigGame.Client.Services;

public class GameHubConnection : IAsyncDisposable
{
    private readonly ClientGameState _state;
    private readonly NavigationManager _navigation;
    private HubConnection? _hubConnection;

    public event Action? OnStateChanged;
    public event Action? OnMessageReceived;

    public GameHubConnection(ClientGameState state, NavigationManager navigation)
    {
        _state = state;
        _navigation = navigation;
    }

    public bool IsConnected => _hubConnection?.State == HubConnectionState.Connected;

    public async Task ConnectAsync()
    {
        if (IsConnected)
            return;

        if (_hubConnection is null)
        {
            var hubUrl = new Uri(new Uri(_navigation.BaseUri), "gamehub").ToString();

            _hubConnection = new HubConnectionBuilder()
                .WithUrl(hubUrl)
                .WithAutomaticReconnect()
                .Build();

            _hubConnection.On<GameState>("UpdateGameState", state =>
            {
                _state.CurrentState = state;
                _state.CurrentGameId = state.GameId;
                OnStateChanged?.Invoke();
            });

            _hubConnection.On<string>("ShowMessage", message =>
            {
                _state.AddMessage(message);
                OnMessageReceived?.Invoke();
            });

            _hubConnection.Reconnected += connectionId =>
            {
                _state.MyConnectionId = connectionId ?? string.Empty;
                _state.AddMessage("Соединение восстановлено. Если игра не обновляется, перезайдите в комнату.");
                OnMessageReceived?.Invoke();
                return Task.CompletedTask;
            };

            _hubConnection.Closed += _ =>
            {
                _state.AddMessage("Соединение с сервером потеряно.");
                OnMessageReceived?.Invoke();
                return Task.CompletedTask;
            };
        }

        try
        {
            await _hubConnection.StartAsync();
            _state.MyConnectionId = _hubConnection.ConnectionId ?? string.Empty;
            _state.AddMessage("Подключение к серверу установлено.");
            OnMessageReceived?.Invoke();
        }
        catch (Exception ex)
        {
            _state.AddMessage($"Не удалось подключиться к серверу: {ex.Message}");
            OnMessageReceived?.Invoke();
        }
    }

    public Task CreateGameAsync(string playerName, GameMode mode) => InvokeAsync("CreateGame", playerName, mode);

    public Task JoinGameAsync(string gameId, string playerName) => InvokeAsync("JoinGame", gameId, playerName);

    public Task RollDiceAsync(string gameId) => InvokeAsync("RollDice", gameId);

    public Task HoldAsync(string gameId) => InvokeAsync("Hold", gameId);

    public Task SetReadyAsync(string gameId, bool isReady) => InvokeAsync("SetReady", gameId, isReady);

    public Task SendChatAsync(string gameId, string text) => InvokeAsync("SendChat", gameId, text);

    private async Task InvokeAsync(string method, params object?[] args)
    {
        if (_hubConnection is null || !IsConnected)
        {
            _state.AddMessage("Нет соединения с сервером.");
            OnMessageReceived?.Invoke();
            return;
        }

        try
        {
            await _hubConnection.InvokeCoreAsync(method, args);
        }
        catch (Exception ex)
        {
            _state.AddMessage($"Ошибка: {ex.Message}");
            OnMessageReceived?.Invoke();
        }
    }

    public async ValueTask DisposeAsync()
    {
        if (_hubConnection is not null)
            await _hubConnection.DisposeAsync();
    }
}
