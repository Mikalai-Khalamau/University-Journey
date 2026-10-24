using System.Net.Http.Json;
using System.Text.Json;
using WEB_453503_Khalamau.Domain.Entities;
using WEB_453503_Khalamau.Domain.Models;

namespace WEB_453503_Khalamau.UI.Services.GemTypeService;

public class ApiGemTypeService : IGemTypeService
{
    private readonly HttpClient _httpClient;
    private readonly JsonSerializerOptions _serializerOptions;
    private readonly ILogger<ApiGemTypeService> _logger;

    public ApiGemTypeService(HttpClient httpClient, ILogger<ApiGemTypeService> logger)
    {
        _httpClient = httpClient;
        _logger = logger;
        _serializerOptions = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
    }

    public async Task<ResponseData<List<GemType>>> GetGemTypeListAsync()
    {
        try
        {
            // Запрашиваем "gemtypes" относительно BaseAddress (".../api/")
            var response = await _httpClient.GetAsync("gemtypes");

            if (response.IsSuccessStatusCode)
            {
                // API возвращает просто массив, мы сами заворачиваем его в ResponseData
                var data = await response.Content.ReadFromJsonAsync<List<GemType>>(_serializerOptions);

                if (data != null)
                {
                    return ResponseData<List<GemType>>.Ok(data);
                }
                return ResponseData<List<GemType>>.Error("Пустой ответ от сервера");
            }

            _logger.LogError($"Ошибка получения типов: {response.StatusCode}");
            return ResponseData<List<GemType>>.Error($"Ошибка сервера: {response.StatusCode}");
        }
        catch (Exception ex)
        {
            _logger.LogError($"Исключение при запросе типов: {ex.Message}");
            return ResponseData<List<GemType>>.Error($"Ошибка соединения: {ex.Message}");
        }
    }
}