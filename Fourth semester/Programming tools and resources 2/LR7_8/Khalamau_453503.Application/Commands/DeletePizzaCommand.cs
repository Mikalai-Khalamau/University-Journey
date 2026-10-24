using MediatR;

namespace Khalamau_453503.Application.Commands;

public sealed record DeletePizzaCommand(int PizzaId) : IRequest<Unit>;