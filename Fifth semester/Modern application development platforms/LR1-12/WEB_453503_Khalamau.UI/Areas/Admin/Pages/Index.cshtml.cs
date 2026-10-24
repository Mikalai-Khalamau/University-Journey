using Microsoft.AspNetCore.Mvc.RazorPages;
using WEB_453503_Khalamau.Domain.Entities;
using WEB_453503_Khalamau.UI.Services.GemService;

namespace WEB_453503_Khalamau.UI.Areas.Admin.Pages;

public class IndexModel : PageModel
{
    private const int PageSize = 10;

    private readonly IGemService _gemService;

    public IndexModel(IGemService gemService)
    {
        _gemService = gemService;
    }

    public IList<Gem> Gem { get; set; } = new List<Gem>();
    public int PageNo { get; set; } = 1;
    public int TotalPages { get; set; }

    public async Task OnGetAsync(int pageNo = 1)
    {
        var response = await _gemService.GetGemListAsync(null, pageNo, PageSize);

        if (response.Successfull && response.Data is not null)
        {
            Gem = response.Data.Items.ToList();
            PageNo = response.Data.PageNo;
            TotalPages = (int)Math.Ceiling(response.Data.TotalCount / (double)response.Data.PageSize);
        }
        else
        {
            ViewData["ErrorMessage"] = response.ErrorMessage;
        }
    }
}
