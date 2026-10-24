using Persistence.Data;
using Persistence.Repository;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;

namespace Khalamau_453503.Persistence;

public static class DependencyInjection
{
    // Базовая регистрация 
    public static IServiceCollection AddPersistence(this IServiceCollection services)
    {
        return services;
    }

    // Регистрация с настройками БД (вызывается из MauiProgram)
    public static IServiceCollection AddPersistence(
        this IServiceCollection services,
        DbContextOptions<AppDbContext> options)
    {
        services.AddPersistence() // вызывает метод выше
                .AddSingleton<AppDbContext>(sp => new AppDbContext(options))
                .AddSingleton<IUnitOfWork, EfUnitOfWork>();

        return services;
    }
}