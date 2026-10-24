using System.Net.Http.Json;
using System.Text.Json;
using WEB_453503_Khalamau.Domain.Entities;
using WEB_453503_Khalamau.Domain.Models;
using WEB_453503_Khalamau.UI.Services.Authentication;

namespace WEB_453503_Khalamau.UI.Services.GemService;

public class ApiGemService : IGemService
{
    private readonly HttpClient _httpClient;
    private readonly string _pageSize;
    private readonly JsonSerializerOptions _serializerOptions;
    private readonly ILogger<ApiGemService> _logger;
    private readonly ITokenAccessor _tokenAccessor;

    public ApiGemService(HttpClient httpClient, IConfiguration configuration,
        ILogger<ApiGemService> logger, ITokenAccessor tokenAccessor)
    {
        _httpClient = httpClient;
        _logger = logger;
        _tokenAccessor = tokenAccessor;
        _pageSize = configuration.GetValue<string>("ItemsPerPage", "3");
        _serializerOptions = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
    }

    public async Task<ResponseData<ListModel<Gem>>> GetGemListAsync(string? typeNormalizedName, int pageNo = 1, int? pageSize = null)
    {
        try
        {
            await _tokenAccessor.SetAuthorizationHeaderAsync(_httpClient, false);

            // 1. Безопасное формирование пути относительно BaseAddress (".../api/")
            string path = "gems";

            if (!string.IsNullOrEmpty(typeNormalizedName))
            {
                path += $"/{typeNormalizedName}";
            }

            path += $"?pageNo={pageNo}&pageSize={pageSize?.ToString() ?? _pageSize}";

            // 2. Отправка запроса (итоговый URL будет: .../api/gems/precious?pageNo=1&pageSize=3)
            var response = await _httpClient.GetAsync(path);

            // 3. Обработка ответа
            if (response.IsSuccessStatusCode)
            {
                var data = await response.Content.ReadFromJsonAsync<ResponseData<ListModel<Gem>>>(_serializerOptions);
                return data ?? ResponseData<ListModel<Gem>>.Error("Пустой ответ от сервера");
            }

            _logger.LogError($"Данные не получены от сервера. Error: {response.StatusCode}");
            return ResponseData<ListModel<Gem>>.Error($"Данные не получены. Error: {response.StatusCode}");
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError($"Ошибка HTTP запроса: {ex.Message}");
            return ResponseData<ListModel<Gem>>.Error($"Не удалось подключиться к API: {ex.Message}");
        }
        catch (JsonException ex)
        {
            _logger.LogError($"Ошибка парсинга JSON: {ex.Message}");
            return ResponseData<ListModel<Gem>>.Error($"Ошибка формата данных: {ex.Message}");
        }
    }

    public async Task<ResponseData<Gem>> GetGemByIdAsync(int id)
    {
        try
        {
            await _tokenAccessor.SetAuthorizationHeaderAsync(_httpClient, false);

            var response = await _httpClient.GetAsync($"gems/{id}");

            if (response.IsSuccessStatusCode)
            {
                var data = await response.Content.ReadFromJsonAsync<ResponseData<Gem>>(_serializerOptions);
                return data ?? ResponseData<Gem>.Error("Пустой ответ от сервера");
            }

            _logger.LogError($"Объект не получен. Error: {response.StatusCode}");
            return ResponseData<Gem>.Error($"Объект не получен. Error: {response.StatusCode}");
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError($"Ошибка HTTP запроса: {ex.Message}");
            return ResponseData<Gem>.Error($"Не удалось подключиться к API: {ex.Message}");
        }
        catch (JsonException ex)
        {
            _logger.LogError($"Ошибка парсинга JSON: {ex.Message}");
            return ResponseData<Gem>.Error($"Ошибка формата данных: {ex.Message}");
        }
    }

    public async Task<ResponseData<Gem>> CreateGemAsync(Gem gem, IFormFile? formFile)
    {
        try
        {
            await _tokenAccessor.SetAuthorizationHeaderAsync(_httpClient, false);

            gem.Image = "Images/noimage.jpg";

            var request = new HttpRequestMessage
            {
                Method = HttpMethod.Post,
                RequestUri = new Uri(_httpClient.BaseAddress!, "gems")
            };

            var content = new MultipartFormDataContent();

            if (formFile != null)
            {
                var streamContent = new StreamContent(formFile.OpenReadStream());
                content.Add(streamContent, "file", formFile.FileName);
            }

            var data = new StringContent(JsonSerializer.Serialize(new
            {
                gem.Name,
                gem.Description,
                gem.Price,
                gem.TypeId
            }));
            content.Add(data, "gem");

            request.Content = content;

            var response = await _httpClient.SendAsync(request, CancellationToken.None);

            if (response.IsSuccessStatusCode)
            {
                var responseData = await response.Content.ReadFromJsonAsync<ResponseData<Gem>>(_serializerOptions);
                return responseData ?? ResponseData<Gem>.Error("Пустой ответ от сервера");
            }

            _logger.LogError($"-----> object not created. Error: {response.StatusCode}");
            return ResponseData<Gem>.Error($"Объект не добавлен. Error: {response.StatusCode}");
        }
        catch (HttpRequestException ex)
        {
            _logger.LogError($"Ошибка HTTP запроса: {ex.Message}");
            return ResponseData<Gem>.Error($"Не удалось подключиться к API: {ex.Message}");
        }
        catch (JsonException ex)
        {
            _logger.LogError($"Ошибка парсинга JSON: {ex.Message}");
            return ResponseData<Gem>.Error($"Ошибка формата данных: {ex.Message}");
        }
    }

    public async Task UpdateGemAsync(int id, Gem gem, IFormFile? formFile)
    {
        try
        {
            await _tokenAccessor.SetAuthorizationHeaderAsync(_httpClient, false);
        }
        catch (Exception e)
        {
            throw new HttpRequestException($"Объект не изменён. Error: {e.Message}");
        }

        var request = new HttpRequestMessage
        {
            Method = HttpMethod.Put,
            RequestUri = new Uri(_httpClient.BaseAddress!, $"gems/{id}")
        };

        var content = new MultipartFormDataContent();

        if (formFile != null)
        {
            var streamContent = new StreamContent(formFile.OpenReadStream());
            content.Add(streamContent, "file", formFile.FileName);
        }

        var data = new StringContent(JsonSerializer.Serialize(new
        {
            gem.Name,
            gem.Description,
            gem.Price,
            gem.TypeId
        }));
        content.Add(data, "gem");

        request.Content = content;

        var response = await _httpClient.SendAsync(request, CancellationToken.None);

        if (!response.IsSuccessStatusCode)
        {
            var body = await response.Content.ReadAsStringAsync();
            _logger.LogError($"-----> object not updated. Error: {response.StatusCode}. {body}");
            throw new HttpRequestException($"Объект не изменён. Error: {response.StatusCode}");
        }
    }

    public async Task DeleteGemAsync(int id)
    {
        try
        {
            await _tokenAccessor.SetAuthorizationHeaderAsync(_httpClient, false);
        }
        catch (Exception e)
        {
            throw new HttpRequestException($"Объект не удалён. Error: {e.Message}");
        }

        var response = await _httpClient.DeleteAsync($"gems/{id}");

        if (!response.IsSuccessStatusCode)
        {
            _logger.LogError($"-----> object not deleted. Error: {response.StatusCode}");
            throw new HttpRequestException($"Объект не удалён. Error: {response.StatusCode}");
        }
    }
}