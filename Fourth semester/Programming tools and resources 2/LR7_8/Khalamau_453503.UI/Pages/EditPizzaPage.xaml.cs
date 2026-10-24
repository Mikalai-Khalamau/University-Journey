using Khalamau_453503.UI.ViewModels;

namespace Khalamau_453503.UI.Pages;

public partial class EditPizzaPage : ContentPage
{
    public EditPizzaPage(EditPizzaViewModel viewModel)
    {
        InitializeComponent();
        BindingContext = viewModel;
    }
}