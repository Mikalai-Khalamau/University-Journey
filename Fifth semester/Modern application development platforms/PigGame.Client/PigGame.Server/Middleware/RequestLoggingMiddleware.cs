using System.Diagnostics;

namespace PigGame.Server.Middleware;

public class RequestLoggingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleware> _logger;

    public RequestLoggingMiddleware(RequestDelegate next, ILogger<RequestLoggingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var stopwatch = Stopwatch.StartNew();

        try
        {
            await _next(context);
        }
        catch (Exception exception)
        {
            _logger.LogError(
                exception,
                "HTTP {Method} {Path}{Query} failed after {Elapsed} ms",
                context.Request.Method,
                context.Request.Path,
                context.Request.QueryString,
                stopwatch.ElapsedMilliseconds);

            throw;
        }
        finally
        {
            stopwatch.Stop();

            _logger.LogInformation(
                "HTTP {Method} {Path}{Query} -> {StatusCode} in {Elapsed} ms ({RemoteIp})",
                context.Request.Method,
                context.Request.Path,
                context.Request.QueryString,
                context.Response.StatusCode,
                stopwatch.ElapsedMilliseconds,
                context.Connection.RemoteIpAddress);
        }
    }
}
