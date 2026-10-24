using Microsoft.Extensions.Configuration;

namespace WEB_453503_Khalamau.UI.Services.GemService;

public class MemoryGemService : IGemService
{
    private List<Gem> _gems;
    private readonly List<GemType> _gemTypes;
    private readonly int _itemsPerPage;

    public MemoryGemService(IConfiguration config, IGemTypeService gemTypeService)
    {
        _gemTypes = gemTypeService.GetGemTypeListAsync().Result.Data ?? new List<GemType>();
        _itemsPerPage = config.GetValue<int>("ItemsPerPage", 3);
        _gems = new List<Gem>();
        SetupData();
    }

    private void SetupData()
    {
        _gems = new List<Gem>
        {
            new Gem
            {
                Id = 1,
                Name = "Алмаз",
                Description = "Крепкий орешек",
                Price = 5000,
                Image = "/Images/diamond.jpg",
                MimeType = "image/jpeg",
                Type = _gemTypes.Find(t => t.NormalizedName == "precious")
            },
            new Gem
            {
                Id = 2,
                Name = "Рубин",
                Description = "Как томатный сок",
                Price = 3500,
                Image = "/Images/ruby.jpg",
                MimeType = "image/jpeg",
                Type = _gemTypes.Find(t => t.NormalizedName == "precious")
            },
            new Gem
            {
                Id = 3,
                Name = "Сапфир",
                Description = "Голубой и овальный",
                Price = 2800,
                Image = "/Images/sapphire.jpg",
                MimeType = "image/jpeg",
                Type = _gemTypes.Find(t => t.NormalizedName == "precious")
            },
            new Gem
            {
                Id = 4,
                Name = "Аметист",
                Description = "Не разбираюсь",
                Price = 150,
                Image = "/Images/amethyst.jpg",
                MimeType = "image/jpeg",
                Type = _gemTypes.Find(t => t.NormalizedName == "semi-precious")
            },
            new Gem
            {
                Id = 5,
                Name = "Изумруд",
                Description = "Страна ОЗ",
                Price = 4200,
                Image = "/Images/emerald.jpg",
                MimeType = "image/jpeg",
                Type = _gemTypes.Find(t => t.NormalizedName == "precious")
            },
            new Gem
            {
                Id = 6,
                Name = "Жемчуг",
                Description = "Бусинки",
                Price = 300,
                Image = "/Images/pearl.jpg",
                MimeType = "image/jpeg",
                Type = _gemTypes.Find(t => t.NormalizedName == "organic")
            },
            new Gem
            {
                Id = 7,
                Name = "Гранат",
                Description = "Зернышки полузгать можно",
                Price = 200,
                Image = "/Images/garnet.jpg",
                MimeType = "image/jpeg",
                Type = _gemTypes.Find(t => t.NormalizedName == "semi-precious")
            },
            new Gem
            {
                Id = 8,
                Name = "Малахит",
                Description = "Шкатулка у Бажова такая была",
                Price = 200,
                Image = "/Images/malahit.jpg",
                MimeType = "image/jpeg",
                Type = _gemTypes.Find(t => t.NormalizedName == "ornamental")
            }
        };
    }

    public Task<ResponseData<ListModel<Gem>>> GetGemListAsync(string? typeNormalizedName, int pageNo = 1, int? pageSize = null)
    {
        var itemsPerPage = pageSize ?? _itemsPerPage;

        // Фильтрация по типу
        var filtered = _gems
            .Where(g => typeNormalizedName == null || g.Type?.NormalizedName == typeNormalizedName)
            .ToList();

        // Пагинация
        var totalCount = filtered.Count;

        var items = filtered
            .Skip((pageNo - 1) * itemsPerPage)
            .Take(itemsPerPage)
            .ToList();

        var result = new ListModel<Gem>
        {
            Items = items,
            PageNo = pageNo,
            PageSize = itemsPerPage,
            TotalCount = totalCount
        };

        return Task.FromResult(ResponseData<ListModel<Gem>>.Ok(result));
    }

    // Заглушки для остальных методов
    public Task<ResponseData<Gem>> GetGemByIdAsync(int id) => throw new NotImplementedException();
    public Task UpdateGemAsync(int id, Gem gem, IFormFile? formFile) => Task.CompletedTask;
    public Task DeleteGemAsync(int id) => Task.CompletedTask;
    public Task<ResponseData<Gem>> CreateGemAsync(Gem gem, IFormFile? formFile) => throw new NotImplementedException();
}