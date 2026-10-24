using MediatR;
using Khalamau_453503.Domain.Entities;

namespace Khalamau_453503.Application.Queries
{
    public class GetAllOrdersQuery : IRequest<List<Order>>
    {
    }
    public class GetPizzaByOrderIdQuery : IRequest<List<Pizza>>
    {
        public int OrderId { get; set; }
    }
}