using System;
using Khalamau_Lab4;
using System.Threading;
using System.Threading.Tasks;
using Microsoft.Maui.Controls;

namespace Lab4Maui;

public partial class IntegrationPage : ContentPage
{
    private CancellationTokenSource _cts;
    private Sinus _sinus;

    public IntegrationPage()
    {
        InitializeComponent();
    }

    private async void StartButton_Clicked(object sender, EventArgs e)
    {
        StartButton.IsEnabled = false;
        CancelButton.IsEnabled = true;

        StatusLabel.Text = "Вычисление...";
        ProgressBar.Progress = 0;
        PercentLabel.Text = "0%";

        _cts = new CancellationTokenSource();
        _sinus = new Sinus();

        var progress = new Progress<double>(p =>
        {
            ProgressBar.Progress = p;
            PercentLabel.Text = $"{p:P0}";
        });

        double result = 0;
        try
        {
            result = await Task.Run(() => _sinus.ComputeIntegral(progress, _cts.Token), _cts.Token);

            StatusLabel.Text = $"Результат: {result:F6}";
        }
        catch (OperationCanceledException)
        {
            StatusLabel.Text = "Задание отменено";
        }
        catch (Exception ex)
        {
            StatusLabel.Text = $"Ошибка: {ex.Message}";
        }
        finally
        {
            StartButton.IsEnabled = true;
            CancelButton.IsEnabled = false;
            _cts?.Dispose();
            _cts = null;
        }
    }

    private void CancelButton_Clicked(object sender, EventArgs e)
    {
        _cts?.Cancel();
    }
}