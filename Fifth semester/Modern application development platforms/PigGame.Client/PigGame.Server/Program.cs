using PigGame.Server.GameLogic;
using PigGame.Server.Hubs;
using PigGame.Server.Middleware;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddSignalR();
builder.Services.AddSingleton<IDiceRoller, RandomDiceRoller>();
builder.Services.AddSingleton<PigGameEngine>();

var app = builder.Build();

app.UseMiddleware<RequestLoggingMiddleware>();

app.UseBlazorFrameworkFiles();
app.UseStaticFiles();

app.MapHub<GameHub>("/gamehub");
app.MapFallbackToFile("index.html");

app.Run();
