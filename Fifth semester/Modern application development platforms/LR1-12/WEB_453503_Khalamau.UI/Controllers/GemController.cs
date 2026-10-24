using Microsoft.AspNetCore.Mvc;
using WEB_453503_Khalamau.Domain.Entities;
using WEB_453503_Khalamau.UI.Extensions;
using WEB_453503_Khalamau.UI.Services.GemService;
using WEB_453503_Khalamau.UI.Services.GemTypeService;

namespace WEB_453503_Khalamau.UI.Controllers;

public class GemController : Controller
{
    private readonly IGemService _gemService;
    private readonly IGemTypeService _gemTypeService;

    public GemController(IGemService gemService, IGemTypeService gemTypeService)
    {
        _gemService = gemService;
        _gemTypeService = gemTypeService;
    }

    [Route("Catalog/{type?}")]
    public async Task<IActionResult> Index(string? type, int pageNo = 1)
    {
        // 1. Получить список категорий
        var categoriesResponse = await _gemTypeService.GetGemTypeListAsync();
        if (!categoriesResponse.Successfull)
            return NotFound(categoriesResponse.ErrorMessage);

        var gemTypes = categoriesResponse.Data as List<GemType> ?? categoriesResponse.Data?.ToList();
        ViewData["categories"] = gemTypes;
        ViewBag.GemTypes = gemTypes;

        // 2. Передать во ViewData имя текущей категории
        var currentCategory = type == null
            ? "Все"
            : gemTypes?.FirstOrDefault(c => c.NormalizedName == type)?.Name;

        ViewData["currentCategory"] = currentCategory;
        ViewBag.CurrentTypeName = currentCategory ?? "Все";
        ViewBag.CurrentType = type;

        // 3. Получить список объектов
        var gemResponse = await _gemService.GetGemListAsync(type, pageNo);
        if (!gemResponse.Successfull)
            return NotFound(gemResponse.ErrorMessage);

        // 4. Проверить, был ли запрос асинхронным
        var request = HttpContext?.Request;
        if (request != null)
        {
            ViewData["ReturnUrl"] = request.Path + request.QueryString.ToUriComponent();
            if (request.IsAjaxRequest())
                return PartialView("_ListPartial", gemResponse.Data);
        }

        // 5. Вернуть полное представление
        return View(gemResponse.Data);
    }
}
