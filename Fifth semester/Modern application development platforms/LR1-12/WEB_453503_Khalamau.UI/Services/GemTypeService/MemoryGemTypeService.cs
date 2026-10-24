namespace WEB_453503_Khalamau.UI.Services.GemTypeService;

public class MemoryGemTypeService : IGemTypeService
{
    public Task<ResponseData<List<GemType>>> GetGemTypeListAsync()
    {
        var gemTypes = new List<GemType>
        {
            new GemType { Id = 1, Name = "Драгоценные", NormalizedName = "precious" },
            new GemType { Id = 2, Name = "Полудрагоценные", NormalizedName = "semi-precious" },
            new GemType { Id = 3, Name = "Поделочные", NormalizedName = "ornamental" },
            new GemType { Id = 4, Name = "Органические", NormalizedName = "organic" },
            new GemType { Id = 5, Name = "Синтетические", NormalizedName = "synthetic" }
        };
        return Task.FromResult(ResponseData<List<GemType>>.Ok(gemTypes));
    }
}