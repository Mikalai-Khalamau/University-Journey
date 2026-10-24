namespace WEB_453503_Khalamau.UI.Services.Authentication;

public interface ITokenAccessor
{
    Task SetAuthorizationHeaderAsync(HttpClient httpClient, bool isClient);
}
