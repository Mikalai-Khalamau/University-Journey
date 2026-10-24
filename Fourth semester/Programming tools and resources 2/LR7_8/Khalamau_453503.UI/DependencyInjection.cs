using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Khalamau_453503.UI.Pages;
using Khalamau_453503.UI.ViewModels;

namespace Khalamau_453503.UI
{
    public static class DependencyInjection
    {
        public static IServiceCollection RegisterPages(this IServiceCollection services)
        {
            services
                .AddTransient<OrdersPage>()
                .AddTransient<PizzaDetails>()
                .AddTransient<AddOrderPage>()
                .AddTransient<AddPizzaPage>()
                .AddTransient<EditPizzaPage>();
            return services;
        }

        public static IServiceCollection RegisterViewModels(this IServiceCollection services)
        {
            services
                .AddTransient<OrderViewModel>()
                .AddTransient<PizzaDetailsViewModel>()
                .AddTransient<AddOrderViewModel>()
                .AddTransient<AddPizzaViewModel>()
                .AddTransient<EditPizzaViewModel>();
            return services;
        }
    }
}