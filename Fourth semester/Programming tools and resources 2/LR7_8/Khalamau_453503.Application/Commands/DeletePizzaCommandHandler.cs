using Khalamau_453503.Domain.Abstractions;
using MediatR;

namespace Khalamau_453503.Application.Commands;

public class DeletePizzaCommandHandler : IRequestHandler<DeletePizzaCommand, Unit>
{
    private readonly IUnitOfWork _unitOfWork;

    public DeletePizzaCommandHandler(IUnitOfWork unitOfWork)
    {
        _unitOfWork = unitOfWork;
    }

    public async Task<Unit> Handle(DeletePizzaCommand request, CancellationToken cancellationToken)
    {
        var pizza = await _unitOfWork.PizzaRepository.GetByIdAsync(request.PizzaId, cancellationToken);

        if (pizza == null)
            return Unit.Value;

        await _unitOfWork.PizzaRepository.DeleteAsync(pizza, cancellationToken);
        await _unitOfWork.SaveAllAsync();

        return Unit.Value;
    }
}