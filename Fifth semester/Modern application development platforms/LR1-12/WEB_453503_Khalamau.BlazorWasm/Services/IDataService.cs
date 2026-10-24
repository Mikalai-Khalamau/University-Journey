using WEB_453503_Khalamau.Domain.Entities;

namespace WEB_453503_Khalamau.BlazorWasm.Services;

public interface IDataService
{
    event Action? DataLoaded;

    List<GemType> Categories { get; set; }
    List<Gem> Dishes { get; set; }
    List<Gem> ObjectsList { get; }
    bool Success { get; set; }
    string ErrorMessage { get; set; }
    int TotalPages { get; set; }
    int CurrentPage { get; set; }
    GemType? SelectedCategory { get; set; }

    Task GetProductListAsync(int pageNo = 1);
    Task GetCategoryListAsync();
}
