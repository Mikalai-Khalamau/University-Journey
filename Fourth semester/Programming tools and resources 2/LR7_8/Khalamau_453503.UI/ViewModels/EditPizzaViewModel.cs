using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Khalamau_453503.Application.Commands;
using Khalamau_453503.Domain.Entities;
using MediatR;

namespace Khalamau_453503.UI.ViewModels;

[QueryProperty(nameof(Pizza), "Pizza")]
public partial class EditPizzaViewModel : ObservableObject
{
    private readonly IMediator _mediator;

    [ObservableProperty]
    private Pizza _pizza = null!;

    [ObservableProperty]
    private string _name = string.Empty;

    [ObservableProperty]
    private int _time;

    public EditPizzaViewModel(IMediator mediator)
    {
        _mediator = mediator;
    }

    [RelayCommand]
    private async Task Save()
    {
        try
        {
            if (Pizza == null || string.IsNullOrWhiteSpace(Name))
            {
                await Shell.Current.DisplayAlert("Error", "Name is required", "OK");
                return;
            }

            var command = new UpdatePizzaCommand(
                Pizza.Id,
                Name.Trim(),
                Time,
                Pizza.ImagePath
            );

            await _mediator.Send(command);

            await Shell.Current.GoToAsync("//OrdersPage");
        }

        catch (Exception ex)
        {
            await Shell.Current.DisplayAlert("Error", ex.Message, "OK");
        }
    }


    [RelayCommand]
    private async Task Cancel()
    {
        await Shell.Current.GoToAsync("..");
    }
}