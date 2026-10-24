using MediatR;
using Khalamau_453503.Domain.Entities;

namespace Khalamau_453503.Application.Commands;

public class AddOrderCommand : IRequest<Order>
{
    public string Name { get; set; } = string.Empty;  
}