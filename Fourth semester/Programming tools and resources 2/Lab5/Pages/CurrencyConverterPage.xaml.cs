using Lab5.Services;
using Lab5.Models;

namespace Lab5.Pages;

public partial class CurrencyConverterPage : ContentPage
{
    private readonly IRateService _rateService;
    private List<Rate> _rates = new();

    private readonly string[] _targetCurrencies = { "RUB", "EUR", "USD", "CHF", "CNY", "GBP" };

    public CurrencyConverterPage(IRateService rateService)
    {
        InitializeComponent();
        _rateService = rateService;

        DatePicker.Date = DateTime.Today;
    }

    protected override async void OnAppearing()
    {
        base.OnAppearing();
        await LoadRates();
    }

    private async Task LoadRates()
    {
        try
        {
            LoadingIndicator.IsRunning = true;
            LoadingIndicator.IsVisible = true;

            _rates = (await _rateService.GetRatesAsync(DatePicker.Date)).ToList();

            var filteredRates = _rates
                .Where(r => _targetCurrencies.Contains(r.Cur_Abbreviation))
                .OrderBy(r => r.Cur_Name)
                .ToList();

            CurrencyPicker.ItemsSource = filteredRates.Select(r =>
                $"{r.Cur_Abbreviation} - {r.Cur_Name}").ToList();
        }
        catch (Exception ex)
        {
            await DisplayAlert("Ошибка", $"Не удалось загрузить курсы: {ex.Message}", "OK");
        }
        finally
        {
            LoadingIndicator.IsRunning = false;
            LoadingIndicator.IsVisible = false;
        }
    }

    private async void DatePicker_DateSelected(object sender, DateChangedEventArgs e)
    {
        await LoadRates();
    }

    private void CurrencyPicker_SelectedIndexChanged(object sender, EventArgs e)
    {
    }

    private void ConvertToCurrency_Clicked(object sender, EventArgs e)
    {
        ConvertCurrency(false); 
    }

    private void ConvertToByn_Clicked(object sender, EventArgs e)
    {
        ConvertCurrency(true); 
    }

    private void ConvertCurrency(bool toByn)
    {
        if (!decimal.TryParse(AmountEntry.Text, out decimal amount))
        {
            ResultLabel.Text = "Ошибка: введите корректную сумму";
            return;
        }

        if (CurrencyPicker.SelectedItem is not string selected)
        {
            ResultLabel.Text = "Ошибка: выберите валюту";
            return;
        }

        var currencyCode = selected.Split(" - ").FirstOrDefault();
        var rate = _rates.FirstOrDefault(r => r.Cur_Abbreviation == currencyCode);

        if (rate == null)
        {
            ResultLabel.Text = "Ошибка: курс не найден";
            return;
        }

        decimal result;
        if (toByn)
        {
            result = amount * rate.RatePerUnit;
            ResultLabel.Text = $"{amount:F2} {currencyCode} = {result:F2} BYN";
        }
        else
        {
            result = amount / rate.RatePerUnit;
            ResultLabel.Text = $"{amount:F2} BYN = {result:F2} {currencyCode}";
        }
    }
}