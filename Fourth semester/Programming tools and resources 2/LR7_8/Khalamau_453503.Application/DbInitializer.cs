using Microsoft.Extensions.DependencyInjection;
using Khalamau_453503.Domain.Abstractions;
using Khalamau_453503.Domain.Entities;

namespace Khalamau_453503.Application;

public static class DbInitializer
{
    public static async Task Initialize(IServiceProvider services)
    {
        var unitOfWork = services.GetRequiredService<IUnitOfWork>();

        await unitOfWork.DeleteDataBaseAsync();
        await unitOfWork.CreateDataBaseAsync();

        var order1 = new Order { Name = "Order for Anton" };
        var order2 = new Order { Name = "Order for Alex" };


        await unitOfWork.OrderRepository.AddAsync(order1);
        await unitOfWork.OrderRepository.AddAsync(order2);
        await unitOfWork.SaveAllAsync();

        await unitOfWork.PizzaRepository.AddAsync(new Pizza
        {
            Name = "Margarita",
            ImagePath = "\"C:\\4 semester BSUIR + T-Academy\\ИСП(Гламаздин)\\margherita.webp\"",
            Time = 15,
            OrderId = order1.Id
        });
        await unitOfWork.PizzaRepository.AddAsync(new Pizza
        {
            Name = "4 cheese",
            ImagePath = "\"C:\\4 semester BSUIR + T-Academy\\ИСП(Гламаздин)\\pizza.jpg\"",
            Time = 20,
            OrderId = order2.Id
        });
        await unitOfWork.PizzaRepository.AddAsync(new Pizza
        {
            Name = "Pala",
            ImagePath = "\"C:\\4 semester BSUIR + T-Academy\\ИСП(Гламаздин)\\pizza.jpg\"",
            Time = 20,
            OrderId = order2.Id
        });

        await unitOfWork.SaveAllAsync();
    }

}