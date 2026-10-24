namespace WEB_453503_Khalamau.UI.Middleware;

/// <summary>
/// Middleware для логирования всех запросов,
/// ответ на которые имеет код состояния, отличный от 2xx.
/// Формат сообщения: ---&gt; request /menu returns 404
/// </summary>
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
        await _next(context);

        var statusCode = context.Response.StatusCode;

        if (statusCode < 200 || statusCode >= 300)
        {
            var url = context.Request.Path.ToString() + context.Request.QueryString.ToString();
            _logger.LogInformation("---> request {Url} returns {StatusCode}", url, statusCode);
        }
    }
}
