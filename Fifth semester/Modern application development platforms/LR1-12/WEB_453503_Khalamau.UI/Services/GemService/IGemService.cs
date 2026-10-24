namespace WEB_453503_Khalamau.UI.Services.GemService;

public interface IGemService
{
    Task<ResponseData<ListModel<Gem>>> GetGemListAsync(string? typeNormalizedName, int pageNo = 1, int? pageSize = null);
    Task<ResponseData<Gem>> GetGemByIdAsync(int id);
    Task UpdateGemAsync(int id, Gem gem, IFormFile? formFile);
    Task DeleteGemAsync(int id);
    Task<ResponseData<Gem>> CreateGemAsync(Gem gem, IFormFile? formFile);
}