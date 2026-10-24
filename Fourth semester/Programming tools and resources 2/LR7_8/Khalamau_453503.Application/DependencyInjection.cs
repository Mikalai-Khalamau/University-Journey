using Microsoft.Extensions.DependencyInjection;

namespace Khalamau_453503.Application;

public static class DependencyInjection
{
    // Регистрирует сервисы слоя Application
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        // Регистрируем MediatR и сканируем текущую сборку на наличие обработчиков
        services.AddMediatR(cfg =>
            cfg.RegisterServicesFromAssembly(typeof(DependencyInjection).Assembly));

        return services;
    }
}