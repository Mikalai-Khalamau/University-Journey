using Lab5.Models;

namespace Lab5.Services
{
    public interface IRateService
    {
        Task<IEnumerable<Rate>> GetRatesAsync(DateTime date);
    }
}