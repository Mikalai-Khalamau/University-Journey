using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Khalamau_453503.Application.Queries;
using Khalamau_453503.Domain.Entities;
using Khalamau_453503.UI.Pages;
using MediatR;
using Microsoft.Maui.Controls;

namespace Khalamau_453503.UI.ViewModels;

public partial class MainViewModel : ObservableObject
{
    private readonly IMediator _mediator;

    public MainViewModel(IMediator mediator)
    {
        _mediator = mediator;
    }

    // Коллекция заказов (группы)
    [ObservableProperty]
    private ObservableCollection<Order> _orders = new();

    // Коллекция пицц выбранного заказа
    [ObservableProperty]
    private ObservableCollection<Pizza> _pizzas = new();

    // Выбранный заказ
    [ObservableProperty]
    private Order? _selectedOrder;

    // Команда загрузки списка заказов
    [RelayCommand]
    private async Task LoadOrders()
    {
        var orders = await _mediator.Send(new GetAllOrdersQuery());

        await MainThread.InvokeOnMainThreadAsync(() =>
        {
            Orders.Clear();
            foreach (var order in orders)
                Orders.Add(order);
        });
    }

    // Команда загрузки пицц для выбранного заказа
    [RelayCommand]
    private async Task LoadPizzas()
    {
        if (SelectedOrder == null)
            return;

        var query = new GetPizzaByOrderIdQuery { OrderId = SelectedOrder.Id };
        var pizzas = await _mediator.Send(query);

        await MainThread.InvokeOnMainThreadAsync(() =>
        {
            Pizzas.Clear();
            foreach (var pizza in pizzas)
                Pizzas.Add(pizza);
        });
    }

    // Команда перехода на страницу деталей пиццы
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