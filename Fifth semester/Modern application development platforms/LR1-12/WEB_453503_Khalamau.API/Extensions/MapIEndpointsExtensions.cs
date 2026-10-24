using WEB_453503_Khalamau.API.Abstractions;

namespace WEB_453503_Khalamau.API.Extensions;

public static class MapIEndpointsExtensions
{
    public static void MapIEndpoints(this WebApplication app)
    {
        var endpoints = typeof(Program).Assembly
            .GetTypes()
            .Where(t => typeof(IEndpoint).IsAssignableFrom(t)
                        && !t.IsInterface
                        && !t.IsAbstract)
            .Select(type => Activator.CreateInstance(type) as IEndpoint)
            .ToArray();

        foreach (var endpoint in endpoints)
        {
            endpoint?.MapEndpoint(app);
        }
    }
}