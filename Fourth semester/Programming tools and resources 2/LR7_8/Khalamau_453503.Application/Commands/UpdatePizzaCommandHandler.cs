using Khalamau_453503.Domain.Abstractions;
using Khalamau_453503.Domain.Entities;
using MediatR;

namespace Khalamau_453503.Application.Commands;

public class UpdatePizzaCommandHandler : IRequestHandler<UpdatePizzaCommand, Pizza>
{
    private readonly IUnitOfWork _unitOfWork;

    public UpdatePizzaCommandHandler(IUnitOfWork unitOfWork)
    {
        _unitOfWork = unitOfWork;
    }

    public async Task<Pizza> Handle(UpdatePizzaCommand request, CancellationToken cancellationToken)
    {
        var pizza = await _unitOfWork.PizzaRepository.GetByIdAsync(request.Id, cancellationToken);

        if (pizza == null)
            throw new Exception("Pizza not found");

        pizza.Name = request.Name;
        pizza.Time = request.Time;
        pizza.ImagePath = request.ImagePath;

        await _unitOfWork.PizzaRepository.UpdateAsync(pizza, cancellationToken);
        await _unitOfWork.SaveAllAsync();

        return pizza;
    }
}