using System.IO;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Khalamau_453503.Application.Commands;
using MediatR;
using Microsoft.Maui.Storage;  

namespace Khalamau_453503.UI.ViewModels;

public partial class AddPizzaViewModel : ObservableObject
{
    private readonly IMediator _mediator;

    public AddPizzaViewModel(IMediator mediator)
    {
        _mediator = mediator;
    }

    [ObservableProperty]
    private string name = string.Empty;

    [ObservableProperty]
    private string imagePath = string.Empty;  

    [ObservableProperty]
    private int time;

    [ObservableProperty]
    private int orderId;

    [RelayCommand]
    private async Task SavePizza()
    {
        string savedImageName = string.Empty;

        if (!string.IsNullOrEmpty(ImagePath) && File.Exists(ImagePath))
        {
            string imagesFolder = Path.Combine(FileSystem.Current.AppDataDirectory, "Images");
            Directory.CreateDirectory(imagesFolder);

            string tempName = $"temp_{Guid.NewGuid()}.jpg";
            string destPath = Path.Combine(imagesFolder, tempName);
            File.Copy(ImagePath, destPath, overwrite: true);

            savedImageName = tempName; 
        }

        var command = new AddPizzaCommand
        {
            Name = string.IsNullOrWhiteSpace(Name) ? " " : Name.Trim(),
            ImagePath = savedImageName,  
            Time = time,
            OrderId = orderId
        };

        var pizza = await _mediator.Send(command);

        if (!string.IsNullOrEmpty(savedImageName) && pizza.Id > 0)
        {
            string imagesFolder = Path.Combine(FileSystem.Current.AppDataDirectory, "Images");
            string oldPath = Path.Combine(imagesFolder, savedImageName);
            string newPath = Path.Combine(imagesFolder, $"{pizza.Id}.jpg");

            if (File.Exists(oldPath))
                File.Move(oldPath, newPath, overwrite: true);
        }

        await Shell.Current.GoToAsync("..");
    }
}