using Khalamau_453503.Domain.Abstractions;
using Khalamau_453503.Domain.Entities;
using MediatR;

namespace Khalamau_453503.Application.Queries
{
    public class GetAllOrdersQueryHandler : IRequestHandler<GetAllOrdersQuery, List<Order>>
    {
        private readonly IUnitOfWork _unitOfWork;

        public GetAllOrdersQueryHandler(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }

        public async Task<List<Order>> Handle(GetAllOrdersQuery request, CancellationToken cancellationToken)
        {
            var orders = await _unitOfWork.OrderRepository.ListAllAsync(cancellationToken);
            if (orders == null || !orders.Any())
            {
                return new List<Order>();
            }
            return orders.ToList();
        }
    }
}