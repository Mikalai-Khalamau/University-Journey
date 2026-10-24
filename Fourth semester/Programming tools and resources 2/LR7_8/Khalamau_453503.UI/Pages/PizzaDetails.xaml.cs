using Khalamau_453503.UI.ViewModels;
namespace Khalamau_453503.UI.Pages;

public partial class PizzaDetails : ContentPage
{
    public PizzaDetails(PizzaDetailsViewModel viewModel)
    {
        InitializeComponent();
        BindingContext = viewModel;
    }
}