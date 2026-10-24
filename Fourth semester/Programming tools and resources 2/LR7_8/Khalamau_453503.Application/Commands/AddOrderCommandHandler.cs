using MediatR;
using Khalamau_453503.Domain.Abstractions;
using Khalamau_453503.Domain.Entities;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Khalamau_453503.Application.Commands
{
    public class AddOrderCommandHandler : IRequestHandler<AddOrderCommand, Order>
    {
        private readonly IUnitOfWork _unitOfWork;

        public AddOrderCommandHandler(IUnitOfWork unitOfWork)
        {
            _unitOfWork = unitOfWork;
        }

        public async Task<Order> Handle(AddOrderCommand request, CancellationToken cancellationToken)
        {
            var order = new Order { Name = request.Name };
            await _unitOfWork.OrderRepository.AddAsync(order, cancellationToken);
            await _unitOfWork.SaveAllAsync();
            return order;
        }
    }
}