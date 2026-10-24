using Khalamau_453503.Domain.Abstractions;
using Khalamau_453503.Domain.Entities;
using MediatR;

namespace Khalamau_453503.Application.Commands;

public class AddPizzaCommandHandler : IRequestHandler<AddPizzaCommand, Pizza>
{
    private readonly IUnitOfWork _unitOfWork;

    public AddPizzaCommandHandler(IUnitOfWork unitOfWork)
    {
        _unitOfWork = unitOfWork;
    }

    public async Task<Pizza> Handle(AddPizzaCommand request, CancellationToken cancellationToken)
    {
        var pizza = new Pizza
        {
            Name = request.Name,
            ImagePath = request.ImagePath,  
            Time = request.Time,
            OrderId = request.OrderId
        };

        await _unitOfWork.PizzaRepository.AddAsync(pizza, cancellationToken);
        await _unitOfWork.SaveAllAsync();

        return pizza;
    }
}