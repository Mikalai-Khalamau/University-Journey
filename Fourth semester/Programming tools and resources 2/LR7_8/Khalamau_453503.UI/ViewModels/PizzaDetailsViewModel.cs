using System.IO;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using Khalamau_453503.Application.Commands;
using Khalamau_453503.Domain.Abstractions;
using Khalamau_453503.UI.Pages;
using Khalamau_453503.Domain.Entities;
using MediatR;

namespace Khalamau_453503.UI.ViewModels;

[QueryProperty(nameof(Pizza), "Pizza")]  
public partial class PizzaDetailsViewModel : ObservableObject
{
    private readonly IMediator _mediator;

    [ObservableProperty] 
    private Pizza _pizza = null!;

    public PizzaDetailsViewModel(IMediator mediator)
    {
        _mediator = mediator;
    }


    [RelayCommand]
    private async Task Edit()
    {
        if (Pizza == null) return;

        var parameters = new Dictionary<string, object>
    {
        { "Pizza", Pizza }
    };
        await Shell.Current.GoToAsync(nameof(EditPizzaPage), parameters);
    }

    [RelayCommand]
    private async Task Delete()
    {
        if (Pizza == null) return;

        bool confirm = await Shell.Current.DisplayAlert(
            "Delete?",
            $"Delete pizza \"{Pizza.Name}\"?",
            "Yes",
            "No");

        if (!confirm) return;

        try
        {
            if (!string.IsNullOrEmpty(Pizza.ImagePath))
            {
                string imagePath = Path.Combine(FileSystem.Current.AppDataDirectory, "Images", Pizza.ImagePath);
                if (File.Exists(imagePath))
                    File.Delete(imagePath);
            }

            await _mediator.Send(new DeletePizzaCommand(Pizza.Id));

            await Shell.Current.GoToAsync("..");
        }
        catch (Exception ex)
        {
            await Shell.Current.DisplayAlert("Error", $"Failed to delete: {ex.Message}", "OK");
        }
    }

    [RelayCommand]
    private async Task SelectImage()
    {
        if (Pizza == null) return;

        try
        {
            var result = await FilePicker.Default.PickAsync(new PickOptions
            {
                PickerTitle = "Выберите изображение",
                FileTypes = FilePickerFileType.Images
            });

            if (result == null) return;

            string imagesFolder = Path.Combine(FileSystem.Current.AppDataDirectory, "Images");
            Directory.CreateDirectory(imagesFolder);

            string destPath = Path.Combine(imagesFolder, $"{Pizza.Id}.jpg");
            using var source = await result.OpenReadAsync();
            using var dest = File.Create(destPath);
            await source.CopyToAsync(dest);

            // Обновляем путь в сущности
            Pizza.ImagePath = $"{Pizza.Id}.jpg";

            // Триггерим обновление для конвертера
            OnPropertyChanged(nameof(Pizza));
        }
        catch (Exception ex)
        {
            await Shell.Current.DisplayAlert("Ошибка", ex.Message, "OK");
        }
    }
}