using System.Net.Http.Headers;
using System.Text.Json.Nodes;
using Microsoft.AspNetCore.Authentication;
using Microsoft.Extensions.Options;
using WEB_453503_Khalamau.UI.HelperClasses;

namespace WEB_453503_Khalamau.UI.Services.Authentication;

public class KeycloakTokenAccessor(
    IHttpContextAccessor contextAccessor,
    IOptions<KeycloakData> options,
    HttpClient httpClient) : ITokenAccessor
{
    public async Task SetAuthorizationHeaderAsync(HttpClient httpClient, bool isClient)
    {
        try
        {
            string? token = isClient
                ? await GetClientTokenAsync()
                : await GetUserTokenAsync();

            if (!string.IsNullOrEmpty(token))
            {
                httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("bearer", token);
            }
            else
            {
                httpClient.DefaultRequestHeaders.Authorization = null;
            }
        }
        catch
        {
            httpClient.DefaultRequestHeaders.Authorization = null;
        }
    }

    private async Task<string?> GetUserTokenAsync()
    {
        var context = contextAccessor.HttpContext;
        if (context is null)
        {
            return null;
        }

        try
        {
            var token = await context.GetTokenAsync("keycloak", "access_token");
            if (!string.IsNullOrEmpty(token))
            {
                return token;
            }
        }
        catch
        {
            // Ignore
        }

        try
        {
            var authResult = await context.AuthenticateAsync("keycloak");
            if (authResult?.Properties is not null)
            {
                var token = authResult.Properties.GetTokenValue("access_token");
                if (!string.IsNullOrEmpty(token))
                {
                    return token;
                }
            }
        }
        catch
        {
            // Ignore
        }

        return null;
    }

    private async Task<string> GetClientTokenAsync()
    {
        var data = options.Value;
        var requestUri = $"{data.Host}/realms/{data.Realm}/protocol/openid-connect/token";

        HttpContent content = new FormUrlEncodedContent([
            new KeyValuePair<string, string>("client_id", data.ClientId),
            new KeyValuePair<string, string>("grant_type", "client_credentials"),
            new KeyValuePair<string, string>("client_secret", data.ClientSecret)
        ]);

        var response = await httpClient.PostAsync(requestUri, content);
        if (!response.IsSuccessStatusCode)
        {
            throw new HttpRequestException(response.StatusCode.ToString());
        }

        var jsonString = await response.Content.ReadAsStringAsync();
        var tokenNode = JsonNode.Parse(jsonString)?["access_token"];
        return tokenNode!.GetValue<string>();
    }
}
