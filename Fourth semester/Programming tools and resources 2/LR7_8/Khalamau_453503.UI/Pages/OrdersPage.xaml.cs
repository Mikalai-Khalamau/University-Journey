namespace Khalamau_453503.UI.Pages;
using Khalamau_453503.UI.ViewModels;
public partial class OrdersPage : ContentPage
{
    private readonly OrderViewModel _viewModel;
    public OrdersPage(OrderViewModel viewModel)
    {
        InitializeComponent();
        _viewModel = viewModel;
        BindingContext = viewModel;
        viewModel.UpdateOrdersCommand.Execute(null);
    }

    private async void OnOrderSelected(object sender, EventArgs e)
    {
        var vm = (OrderViewModel)BindingContext;
        await vm.UpdatePizzasCommand.ExecuteAsync(null);
    }
    protected override async void OnAppearing()
    {
        base.OnAppearing();
        await _viewModel.UpdateOrdersCommand.ExecuteAsync(null);
    }
}