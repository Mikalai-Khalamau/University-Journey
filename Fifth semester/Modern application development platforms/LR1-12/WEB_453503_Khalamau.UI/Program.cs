using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Serilog;
using WEB_453503_Khalamau.Domain.Entities;
using WEB_453503_Khalamau.UI;
using WEB_453503_Khalamau.UI.Extensions;
using WEB_453503_Khalamau.UI.HelperClasses;
using WEB_453503_Khalamau.UI.Middleware;
using WEB_453503_Khalamau.UI.Models;
using WEB_453503_Khalamau.UI.Services.GemService;
using WEB_453503_Khalamau.UI.Services.GemTypeService;

var builder = WebApplication.CreateBuilder(args);

// Serilog: конфигурация читается из секции "Serilog" файла appsettings.json
// (см. https://github.com/serilog/serilog-settings-configuration)
builder.Host.UseSerilog((context, loggerConfiguration) =>
    loggerConfiguration.ReadFrom.Configuration(context.Configuration));

builder.Services.AddControllersWithViews();
builder.Services.AddRazorPages();
builder.Services.AddHttpContextAccessor();
builder.Services.AddHttpClient();

builder.Services.AddDistributedMemoryCache();
builder.Services.AddSession();
builder.Services.AddScoped<Cart>(SessionCart.GetCart);

var uriData = new UriData();
builder.Configuration.GetSection("UriData").Bind(uriData);

builder.Services.AddHttpClient<IGemTypeService, ApiGemTypeService>(options =>
{
    options.BaseAddress = new Uri(uriData.ApiUri);
});

builder.Services.AddHttpClient<IGemService, ApiGemService>(options =>
{
    options.BaseAddress = new Uri(uriData.ApiUri);
});

var keycloakData = new KeycloakData();
builder.Configuration.GetSection("Keycloak").Bind(keycloakData);

builder.RegisterAuthServices();

builder.Services
    .AddAuthentication(options =>
    {
        options.DefaultScheme = CookieAuthenticationDefaults.AuthenticationScheme;
        options.DefaultChallengeScheme = "keycloak";
    })
    .AddCookie()
    .AddOpenIdConnect("keycloak", options =>
    {
        options.Authority = $"{keycloakData.Host}/realms/{keycloakData.Realm}";
        options.ClientId = keycloakData.ClientId;
        options.ClientSecret = keycloakData.ClientSecret;
        options.ResponseType = "code";
        options.Scope.Add("openid");
        options.Scope.Add("email");
        options.SaveTokens = true;
        options.RequireHttpsMetadata = false;
        options.MapInboundClaims = false;
        options.MetadataAddress =
            $"{keycloakData.Host}/realms/{keycloakData.Realm}/.well-known/openid-configuration";
        options.TokenValidationParameters.NameClaimType = "preferred_username";
        options.TokenValidationParameters.RoleClaimType = "role";
    });

builder.Services.AddAuthorization(opt =>
    opt.AddPolicy("admin", p => p.RequireRole("POWER-USER")));

var app = builder.Build();

// Логирование всех запросов с кодом ответа, отличным от 2xx.
// Middleware стоит первым, чтобы видеть итоговый StatusCode всех нижележащих компонентов.
app.UseMiddleware<RequestLoggingMiddleware>();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseSession();

app.UseRouting();

app.UseAuthentication();
app.UseAuthorization();

app.MapRazorPages()
    .RequireAuthorization("admin");

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

app.Run();
