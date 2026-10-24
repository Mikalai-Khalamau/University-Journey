using Khalamau_453503.UI.ViewModels;
using MediatR;
using Microsoft.Maui;
using Microsoft.Maui.Controls;


namespace Khalamau_453503.UI.Pages
{
    [QueryProperty(nameof(OrderId), "OrderId")]
    public partial class AddPizzaPage : ContentPage
    {
        public AddPizzaPage(IMediator mediator)
        {
            InitializeComponent();
            BindingContext = new AddPizzaViewModel(mediator);
        }

        public int OrderId
        {
            set
            {
                if (BindingContext is AddPizzaViewModel viewModel)
                {
                    viewModel.OrderId = value;
                }
            }
        }
    }
}