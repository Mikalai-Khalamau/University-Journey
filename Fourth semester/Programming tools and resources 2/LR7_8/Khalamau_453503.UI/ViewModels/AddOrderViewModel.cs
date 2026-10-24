using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;
using Khalamau_453503.Application.Commands;
using Khalamau_453503.Application.Queries;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using MediatR;
using Microsoft.Maui;
namespace Khalamau_453503.UI.ViewModels
{
    public partial class AddOrderViewModel : ObservableObject
    {
        private readonly IMediator _mediator;

        public AddOrderViewModel(IMediator mediator)
        {
            _mediator = mediator;
        }

        [ObservableProperty]
        private string name;

        [RelayCommand]
        private async Task SaveOrder()
        {
            var name = string.IsNullOrWhiteSpace(Name) ? " " : Name.Trim();

            var command = new AddOrderCommand { Name = name };
            await _mediator.Send(command);
            var superheroes = await _mediator.Send(new GetAllOrdersQuery());
            await Shell.Current.GoToAsync("..");
        }
    }
}