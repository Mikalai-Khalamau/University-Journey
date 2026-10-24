namespace PigGame.Server.GameLogic;

public interface IDiceRoller
{
    int Roll();
}

public sealed class RandomDiceRoller : IDiceRoller
{
    public int Roll() => Random.Shared.Next(1, 7);
}
