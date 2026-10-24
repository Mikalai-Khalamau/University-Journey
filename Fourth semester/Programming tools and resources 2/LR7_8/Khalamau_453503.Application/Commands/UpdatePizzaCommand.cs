using MediatR;
using Khalamau_453503.Domain.Entities;

namespace Khalamau_453503.Application.Commands;

public sealed record UpdatePizzaCommand(
    int Id,
    string Name,
    int Time,
    string ImagePath
) : IRequest<Pizza>;