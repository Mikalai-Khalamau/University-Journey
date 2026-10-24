using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using WEB_453503_Khalamau.Domain.Entities;
using WEB_453503_Khalamau.UI.Services.GemService;

namespace WEB_453503_Khalamau.UI.Areas.Admin.Pages;

public class DeleteModel : PageModel
{
    private readonly IGemService _gemService;

    public DeleteModel(IGemService gemService)
    {
        _gemService = gemService;
    }

    [BindProperty]
    public Gem Gem { get; set; } = default!;

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
        return Page();
    }

    public async Task<IActionResult> OnPostAsync(int? id)
    {
        if (id is null)
        {
            return NotFound();
        }

        try
        {
            await _gemService.DeleteGemAsync(id.Value);
        }
        catch (HttpRequestException ex)
        {
            ModelState.AddModelError(string.Empty, ex.Message);
            var response = await _gemService.GetGemByIdAsync(id.Value);
            if (!response.Successfull || response.Data is null)
            {
                return NotFound();
            }
            Gem = response.Data;
            return Page();
        }

        return RedirectToPage("./Index");
    }
}
