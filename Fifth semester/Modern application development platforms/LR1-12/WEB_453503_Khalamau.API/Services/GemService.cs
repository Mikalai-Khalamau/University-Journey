using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.EntityFrameworkCore;
using WEB_453503_Khalamau.API.Data;
using WEB_453503_Khalamau.Domain.Entities;
using WEB_453503_Khalamau.Domain.Models;

namespace WEB_453503_Khalamau.API.Services;

public class GemService(
    AppDbContext context,
    IWebHostEnvironment? environment = null,
    IHttpContextAccessor? httpContextAccessor = null)
{
    public const int MaxPageSize = 20;

    public async Task<ResponseData<ListModel<Gem>>> GetGemListAsync(
        string? category = null,
        int pageNo = 1,
        int pageSize = 3)
    {
        if (pageSize > MaxPageSize)
        {
            pageSize = MaxPageSize;
        }

        var query = context.Gems.Include(g => g.Type).AsNoTracking();

        if (!string.IsNullOrEmpty(category))
        {
            query = query.Where(g => g.Type != null && g.Type.NormalizedName == category);
        }

        var totalCount = await query.CountAsync();
        var totalPages = (int)Math.Ceiling(totalCount / (double)(pageSize > 0 ? pageSize : 1));

        if (pageNo > totalPages && totalCount > 0)
        {
            return ResponseData<ListModel<Gem>>.Error("Номер страницы превышает общее количество страниц");
        }

        var items = await query
            .Skip((pageNo - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync();

        var listModel = new ListModel<Gem>
        {
            Items = items,
            PageNo = pageNo,
            PageSize = pageSize,
            TotalCount = totalCount
        };

        return ResponseData<ListModel<Gem>>.Ok(listModel);
    }
}
