using WEB_453503_Khalamau.UI.HelperClasses;
using WEB_453503_Khalamau.UI.Services.Authentication;
using WEB_453503_Khalamau.UI.Services.FileService;

namespace WEB_453503_Khalamau.UI.Extensions;

public static class HostingExtensions
{
    public static void RegisterCustomServices(this WebApplicationBuilder builder)
    {
        builder.Services.AddScoped<IGemTypeService, MemoryGemTypeService>();
        builder.Services.AddScoped<IGemService, MemoryGemService>();
    }

    public static void RegisterAuthServices(this WebApplicationBuilder builder)
    {
        builder.Services.Configure<KeycloakData>(builder.Configuration.GetSection("Keycloak"));
        builder.Services.AddHttpClient<ITokenAccessor, KeycloakTokenAccessor>();
        builder.Services.AddScoped<IFileService, LocalFileService>();
    }
}
