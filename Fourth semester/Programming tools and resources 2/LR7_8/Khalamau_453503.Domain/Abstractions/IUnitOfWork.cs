using Khalamau_453503.Domain.Entities;

namespace Khalamau_453503.Domain.Abstractions
{
    public interface IUnitOfWork
    {
        IRepository<Order> OrderRepository { get; }
        IRepository<Pizza> PizzaRepository { get; }
        Task SaveAllAsync();
        Task DeleteDataBaseAsync();
        Task CreateDataBaseAsync();
    }
}