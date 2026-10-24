using PigGame.Shared.Models;

namespace PigGame.Server.GameLogic;

public record GameActionResult(GameState? State, string Message, bool IsSuccess)
{
    public static GameActionResult Success(GameState state, string message) =>
        new(state, message, true);

    public static GameActionResult Failure(GameState? state, string message) =>
        new(state, message, false);
}
