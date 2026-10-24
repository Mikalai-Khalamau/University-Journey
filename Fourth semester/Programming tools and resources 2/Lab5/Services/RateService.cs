using System.Net.Http;
using System.Text.Json;
using Lab5.Models;

namespace Lab5.Services
{
    public class RateService : IRateService
    {
        private readonly HttpClient _httpClient;

        public RateService(HttpClient httpClient)
        {
            _httpClient = httpClient;
        }

        public async Task<IEnumerable<Rate>> GetRatesAsync(DateTime date)
        {
            string requestUrl = $"?periodicity=0&ondate={date:yyyy-MM-dd}";

            var response = await _httpClient.GetAsync(requestUrl);

            response.EnsureSuccessStatusCode();

            using var responseStream = await response.Content.ReadAsStreamAsync();

            var options = new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            };

            var rates = await JsonSerializer.DeserializeAsync<IEnumerable<Rate>>(responseStream, options);

            return rates ?? Enumerable.Empty<Rate>();
        }
    }
}