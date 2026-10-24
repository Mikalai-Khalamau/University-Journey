using Lab5.Services;
using Lab5.Entities;

namespace Lab5.Pages;

public partial class SuperheroesPage : ContentPage
{
    private readonly IDbService _dbService;

    public SuperheroesPage(IDbService dbService)
    {
        InitializeComponent();
        _dbService = dbService;
    }

    protected override async void OnAppearing()
    {
        base.OnAppearing();
        await LoadSuperheroes();
    }

    private async Task LoadSuperheroes()
    {
        var superheroes = _dbService.GetAllSuperheroes();
        HeroPicker.ItemsSource = superheroes.Select(h => h.Name).ToList();
    }

    private void HeroPicker_SelectedIndexChanged(object sender, EventArgs e)
    {
        if (HeroPicker.SelectedItem is string selectedName)
        {
            var superheroes = _dbService.GetAllSuperheroes().ToList();
            var selectedHero = superheroes.FirstOrDefault(h => h.Name == selectedName);

            if (selectedHero != null)
            {
                var powers = _dbService.GetSuperheroPowers(selectedHero.Id);
                PowersCollection.ItemsSource = powers.ToList();
            }
        }
    }
}
