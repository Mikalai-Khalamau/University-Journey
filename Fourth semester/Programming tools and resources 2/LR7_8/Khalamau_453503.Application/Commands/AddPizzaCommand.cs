using MediatR;
using Khalamau_453503.Domain.Entities;

namespace Khalamau_453503.Application.Commands;

public class AddPizzaCommand : IRequest<Pizza>
{
    public string Name { get; set; } = string.Empty;   
    public string ImagePath { get; set; } = string.Empty; 
    public int Time { get; set; }
    public int OrderId { get; set; }
}