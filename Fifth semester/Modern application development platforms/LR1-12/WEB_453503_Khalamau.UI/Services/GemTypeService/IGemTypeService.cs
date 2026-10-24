namespace WEB_453503_Khalamau.UI.Services.GemTypeService;

public interface IGemTypeService
{
    Task<ResponseData<List<GemType>>> GetGemTypeListAsync();
}