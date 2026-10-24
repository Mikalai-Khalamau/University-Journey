using System.Reflection;
using CommunityToolkit.Maui;
using Khalamau_453503.Application;             
using Khalamau_453503.Persistence;
using Khalamau_453503.UI.Pages;
using Khalamau_453503.UI.ViewModels;
using MediatR;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Microsoft.Maui.Storage;
using Persistence.Data;

namespace Khalamau_453503.UI;

public static class MauiProgram
{
    public static MauiApp CreateMauiApp()
    {
        var builder = MauiApp.CreateBuilder();

        builder
            .UseMauiApp<App>()
            .UseMauiCommunityToolkit()
            .ConfigureFonts(fonts =>
            {
                fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
                fonts.AddFont("OpenSans-Semibold.ttf", "OpenSansSemibold");
            });

        // Конфигурация
        var assembly = Assembly.GetExecutingAssembly();
        using var stream = assembly.GetManifestResourceStream("Khalamau_453503.UI.appsettings.json");
        if (stream != null)
            builder.Configuration.AddJsonStream(stream);

        // БД
        var connStr = builder.Configuration.GetConnectionString("SqliteConnection");
        if (string.IsNullOrEmpty(connStr))
        {
            string dataDirectory = FileSystem.Current.AppDataDirectory + "/";
            connStr = $"Data Source={dataDirectory}Khalamau_453503.db";
            System.Diagnostics.Debug.WriteLine($"Using default connection: {connStr}");
        }
        else
        {
            string dataDirectory = FileSystem.Current.AppDataDirectory + "/";
            connStr = string.Format(connStr, dataDirectory);
        }

        var options = new DbContextOptionsBuilder<AppDbContext>()
            .UseSqlite(connStr)
            .Options;

        builder.Services
            .AddApplication()
            .AddPersistence(options);

        Khalamau_453503.UI.DependencyInjection.RegisterPages(builder.Services);
        Khalamau_453503.UI.DependencyInjection.RegisterViewModels(builder.Services);

#if DEBUG
        builder.Logging.AddDebug();
#endif

        var app = builder.Build();

#if DEBUG
        Khalamau_453503.Application.DbInitializer.Initialize(app.Services).Wait();
#endif

        return app;
    }
}