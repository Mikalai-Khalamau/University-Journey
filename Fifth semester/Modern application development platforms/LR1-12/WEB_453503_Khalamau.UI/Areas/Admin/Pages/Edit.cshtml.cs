using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.AspNetCore.Mvc.Rendering;
using WEB_453503_Khalamau.Domain.Entities;
using WEB_453503_Khalamau.UI.Services.GemService;
using WEB_453503_Khalamau.UI.Services.GemTypeService;

namespace WEB_453503_Khalamau.UI.Areas.Admin.Pages;

public class EditModel : PageModel
{
    private readonly IGemService _gemService;
    private readonly IGemTypeService _gemTypeService;

    public EditModel(IGemService gemService, IGemTypeService gemTypeService)
    {
        _gemService = gemService;
        _gemTypeService = gemTypeService;
    }

    [BindProperty]
    public Gem Gem { get; set; } = default!;

    [BindProperty]
    public IFormFile? Image { get; set; }

    public SelectList GemTypes { get; set; } = default!;

    public async Task<IActionResult> OnGetAsync(int? id)
    {
        if (id is null)
        {
            return NotFound();
        }

        var response = await _gemService.GetGemByIdAsync(id.Value);
        if (!response.Successfull || response.Data is null)
        {
            return NotFound();
        }

        Gem = response.Data;
        await LoadGemTypesAsync();
        return Page();
    }

    public async Task<IActionResult> OnPostAsync()
    {
        if (!ModelState.IsValid)
        {
            await LoadGemTypesAsync();
            return Page();
        }

        if (Gem.TypeId is null or < 1)
        {
            ModelState.AddModelError("Gem.TypeId", "Выберите тип камня");
            await LoadGemTypesAsync();
            return Page();
        }

        try
        {
            await _gemService.UpdateGemAsync(Gem.Id, Gem, Image);
        }
        catch (HttpRequestException ex)
        {
            ModelState.AddModelError(string.Empty, ex.Message);
            await LoadGemTypesAsync();
            return Page();
        }

        return RedirectToPage("./Index");
    }

    private async Task LoadGemTypesAsync()
    {
        var response = await _gemTypeService.GetGemTypeListAsync();
        var types = response.Successfull && response.Data is not null
            ? response.Data
            : new List<GemType>();

        GemTypes = new SelectList(types, nameof(GemType.Id), nameof(GemType.Name), Gem?.TypeId);
    }
}
