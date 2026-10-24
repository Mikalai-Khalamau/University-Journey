using PigGame.Shared.Models;

namespace PigGame.Shared.Contracts;

public interface IGameClient
{
    Task UpdateGameState(GameState gameState);

    Task ShowMessage(string message);
}
