using Khalamau_453503.UI.Pages;
namespace Khalamau_453503.UI
{
    public partial class AppShell : Shell
    {
        public AppShell()
        {
            InitializeComponent();
            Routing.RegisterRoute(nameof(OrdersPage), typeof(OrdersPage));
            Routing.RegisterRoute(nameof(PizzaDetails), typeof(PizzaDetails));
            Routing.RegisterRoute(nameof(AddOrderPage), typeof(AddOrderPage));
            Routing.RegisterRoute(nameof(AddPizzaPage), typeof(AddPizzaPage));
            Routing.RegisterRoute(nameof(EditPizzaPage), typeof(EditPizzaPage));
        }
    }
}