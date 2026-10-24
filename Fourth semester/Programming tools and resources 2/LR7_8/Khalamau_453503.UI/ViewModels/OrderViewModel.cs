using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Khalamau_453503.Application.Queries;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Khalamau_453503.Domain.Entities;
using Khalamau_453503.UI.Pages;
using MediatR;
using Microsoft.Maui;
namespace Khalamau_453503.UI.ViewModels
{
    public partial class OrderViewModel : ObservableObject
    {
        private readonly IMediator _mediator;

        public OrderViewModel(IMediator mediator)
        {
            _mediator = mediator;
        }

        public ObservableCollection<Order> Orders { get; set; } = new();
        public ObservableCollection<Pizza> Pizzas { get; set; } = new();

        private Order _selectedOrder;
        public Order SelectedOrder
        {
            get => _selectedOrder;
            set
            {
                SetProperty(ref _selectedOrder, value);
                OnPropertyChanged(nameof(IsOrderSelected));
            }
        }

        public bool IsOrderSelected => SelectedOrder != null;

        [RelayCommand]
        private async Task UpdateOrders()
        {
            var orders = await _mediator.Send(new GetAllOrdersQuery());
            Orders.Clear();
            foreach (var order in orders)
            {
                Orders.Add(order);
            }
        }

        [RelayCommand]
        private async Task UpdatePizzas()
        {
            if (SelectedOrder != null)
            {
                var pizzas = await _mediator.Send(new GetPizzaByOrderIdQuery { OrderId = SelectedOrder.Id });
                Pizzas.Clear();
                foreach (var pizza in pizzas)
                {
                    Pizzas.Add(pizza);
                }
            }
        }

        [RelayCommand]
        private async Task AddOrder()
        {
            Pizzas.Clear();
            await Shell.Current.GoToAsync(nameof(AddOrderPage));
        }

        [RelayCommand]
        private async Task AddPizza()
        {
            Pizzas.Clear();
            if (SelectedOrder != null)
            {
                await Shell.Current.GoToAsync(nameof(AddPizzaPage), new Dictionary<string, object> { { "OrderId", SelectedOrder.Id } });
            }
        }

        [RelayCommand]
        private async Task ShowDetails(Pizza pizza)
        {
            var parameters = new Dictionary<string, object>
    {
        { "Pizza", pizza }
    };
            await Shell.Current.GoToAsync(nameof(PizzaDetails), parameters);
        }
    }
}