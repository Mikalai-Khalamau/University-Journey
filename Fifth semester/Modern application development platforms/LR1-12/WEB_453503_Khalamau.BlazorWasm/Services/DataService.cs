using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;
using System.Text;
using System.Text.Json;
using Microsoft.AspNetCore.Components.WebAssembly.Authentication;
using Microsoft.Extensions.Configuration;
using WEB_453503_Khalamau.Domain.Entities;
using WEB_453503_Khalamau.Domain.Models;

namespace WEB_453503_Khalamau.BlazorWasm.Services;

public class DataService : IDataService
{
    private readonly HttpClient _httpClient;
    private readonly IAccessTokenProvider _tokenProvider;
    private readonly string _pageSize;
    private readonly JsonSerializerOptions _serializerOptions = new(JsonSerializerDefaults.Web)
    {
        PropertyNameCaseInsensitive = true
    };

    public DataService(HttpClient httpClient, IAccessTokenProvider tokenProvider, IConfiguration configuration)
    {
        _httpClient = httpClient;
        _tokenProvider = tokenProvider;
        _pageSize = configuration["ApiSettings:PageSize"] ?? "3";
    }

    public event Action? DataLoaded;

    public List<GemType> Categories { get; set; } = [];
    public List<Gem> Dishes { get; set; } = [];
    public List<Gem> ObjectsList => Dishes;
    public bool Success { get; set; }
    public string ErrorMessage { get; set; } = string.Empty;
    public int TotalPages { get; set; }
    public int CurrentPage { get; set; } = 1;
    public GemType? SelectedCategory { get; set; }

    public async Task GetProductListAsync(int pageNo = 1)
    {
        try
        {
            await SetAuthorizationHeaderAsync();

            var route = new StringBuilder("gems");

            if (SelectedCategory is not null)
            {
                route.Append($"/{Uri.EscapeDataString(SelectedCategory.NormalizedName)}");
            }

            var queryData = new List<KeyValuePair<string, string>>();

            if (pageNo > 1)
            {
                queryData.Add(KeyValuePair.Create("pageNo", pageNo.ToString()));
            }

            queryData.Add(KeyValuePair.Create("pageSize", _pageSize));
            route.Append(BuildQueryString(queryData));

            var response = await _httpClient.GetAsync(route.ToString());

            if (response.IsSuccessStatusCode)
            {
                var result = await response.Content
                    .ReadFromJsonAsync<ResponseData<ListModel<Gem>>>(_serializerOptions);

                if (result?.Successfull == true && result.Data is not null)
                {
                    Dishes = result.Data.Items.ToList();
                    CurrentPage = result.Data.PageNo;
                    TotalPages = result.Data.TotalPages;
                    Success = true;
                    ErrorMessage = string.Empty;
                }
                else
                {
                    Dishes = [];
                    TotalPages = 0;
                    Success = false;
                    ErrorMessage = result?.ErrorMessage ?? "API вернул пустой ответ.";
                }
            }
            else if (response.StatusCode == HttpStatusCode.Unauthorized)
            {
                Dishes = [];
                TotalPages = 0;
                Success = false;
                ErrorMessage = "Требуется вход в систему: API отклонил запрос без JWT-токена.";
            }
            else if (response.StatusCode == HttpStatusCode.Forbidden)
            {
                Dishes = [];
                TotalPages = 0;
                Success = false;
                ErrorMessage = "Недостаточно прав для получения списка камней.";
            }
            else
            {
                Dishes = [];
                TotalPages = 0;
                Success = false;
                ErrorMessage = $"Ошибка API: {(int)response.StatusCode} {response.ReasonPhrase}.";
            }
        }
        catch (AccessTokenNotAvailableException)
        {
            Dishes = [];
            TotalPages = 0;
            Success = false;
            ErrorMessage = "Не удалось получить JWT-токен. Войдите в систему заново.";
        }
        catch (HttpRequestException ex)
        {
            Dishes = [];
            TotalPages = 0;
            Success = false;
            ErrorMessage = $"Не удалось подключиться к API: {ex.Message}";
        }
        catch (JsonException ex)
        {
            Dishes = [];
            TotalPages = 0;
            Success = false;
            ErrorMessage = $"Ошибка разбора ответа API: {ex.Message}";
        }
        finally
        {
            DataLoaded?.Invoke();
        }
    }

    public async Task GetCategoryListAsync()
    {
        try
        {
            await SetAuthorizationHeaderAsync();

            var response = await _httpClient.GetAsync("GemTypes");

            if (response.IsSuccessStatusCode)
            {
                var categories = await response.Content
                    .ReadFromJsonAsync<List<GemType>>(_serializerOptions);

                Categories = categories ?? [];
                Success = true;
                ErrorMessage = string.Empty;
            }
            else
            {
                Categories = [];
                Success = false;
                ErrorMessage = $"Не удалось загрузить категории: {(int)response.StatusCode} {response.ReasonPhrase}.";
            }
        }
        catch (AccessTokenNotAvailableException)
        {
            Categories = [];
            Success = false;
            ErrorMessage = "Не удалось получить JWT-токен для загрузки категорий.";
        }
        catch (HttpRequestException ex)
        {
            Categories = [];
            Success = false;
            ErrorMessage = $"Не удалось подключиться к API: {ex.Message}";
        }
        catch (JsonException ex)
        {
            Categories = [];
            Success = false;
            ErrorMessage = $"Ошибка разбора списка категорий: {ex.Message}";
        }
        finally
        {
            DataLoaded?.Invoke();
        }
    }

    private async Task SetAuthorizationHeaderAsync()
    {
        var tokenRequest = await _tokenProvider.RequestAccessToken();

        if (tokenRequest.TryGetToken(out var token))
        {
            _httpClient.DefaultRequestHeaders.Authorization =
                new AuthenticationHeaderValue("Bearer", token.Value);
        }
        else
        {
            _httpClient.DefaultRequestHeaders.Authorization = null;
        }
    }

    private static string BuildQueryString(IEnumerable<KeyValuePair<string, string>> values)
    {
        var query = string.Join("&", values.Select(value =>
            $"{Uri.EscapeDataString(value.Key)}={Uri.EscapeDataString(value.Value)}"));

        return string.IsNullOrEmpty(query) ? string.Empty : $"?{query}";
    }
}
