using Microsoft.Extensions.Logging;
using Lab5.Pages;
using Lab5.Services;

namespace Lab5
{
    public static class MauiProgram
    {
        public static MauiApp CreateMauiApp()
        {
            var builder = MauiApp.CreateBuilder();
            builder
                .UseMauiApp<App>()
                .ConfigureFonts(fonts =>
                {
                    fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
                    fonts.AddFont("OpenSans-Semibold.ttf", "OpenSansSemibold");
                });
            //ЛР 5
            builder.Services.AddTransient<IDbService, SQLiteService>();
            builder.Services.AddTransient<SuperheroesPage>();


            //ЛР 6
            builder.Services.AddHttpClient<IRateService, RateService>(client =>
            {
                client.BaseAddress = new Uri("https://www.nbrb.by/api/exrates/rates");
            });

            builder.Services.AddTransient<CurrencyConverterPage>();






#if DEBUG
            builder.Logging.AddDebug();
            builder.Logging.SetMinimumLevel(LogLevel.Trace);
#endif

            return builder.Build();
        }
    }
}
