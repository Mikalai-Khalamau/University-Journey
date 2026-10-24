using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Khalamau_453503.Application.Queries;
using Khalamau_453503.Domain.Abstractions;
using Khalamau_453503.Domain.Entities;
using MediatR;

namespace Khalamau_453503.Application.Queries
{
    public class GetPizzaByOrderIdQueryHandler : IRequestHandler<GetPizzaByOrderIdQuery, List<Pizza>>
    {
        private readonly IUnitOfWork _unitOfWork;

        public GetPizzaByOrderIdQueryHandler(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }

        public async Task<List<Pizza>> Handle(GetPizzaByOrderIdQuery request, CancellationToken cancellationToken)
        {
            return (await _unitOfWork.PizzaRepository.ListAsync(a => a.OrderId == request.OrderId, cancellationToken)).ToList();
        }
    }
}