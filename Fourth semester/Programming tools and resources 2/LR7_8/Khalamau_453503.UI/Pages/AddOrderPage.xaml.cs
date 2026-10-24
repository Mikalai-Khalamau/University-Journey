namespace Khalamau_453503.UI.Pages;
using Khalamau_453503.UI.ViewModels;
public partial class AddOrderPage : ContentPage
{
    public AddOrderPage(AddOrderViewModel viewModel)
    {
        InitializeComponent();
        BindingContext = viewModel;
    }
}