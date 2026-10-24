namespace WEB_453503_Khalamau.UI.Extensions;

public static class HttpRequestExtensions
{
    public static bool IsAjaxRequest(this HttpRequest request)
    {
        return request.Headers.TryGetValue("x-requested-with", out var headerValue)
               && headerValue.ToString().Equals("xmlhttprequest", StringComparison.OrdinalIgnoreCase);
    }
}
