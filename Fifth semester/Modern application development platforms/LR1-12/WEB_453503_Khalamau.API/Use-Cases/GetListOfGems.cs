using MediatR;
using Microsoft.EntityFrameworkCore;
using WEB_453503_Khalamau.API.Data;
using WEB_453503_Khalamau.Domain.Entities;
using WEB_453503_Khalamau.Domain.Models;

namespace WEB_453503_Khalamau.API.Use_Cases;

public sealed record GetListOfGems(
    string? categoryNormalizedName,
    int pageNo = 1,
    int pageSize = 3) : IRequest<ResponseData<ListModel<Gem>>>;

public class GetListOfGemsHandler(AppDbContext db) : IRequestHandler<GetListOfGems, ResponseData<ListModel<Gem>>>
{
    private readonly int _maxPageSize = 20;

    public async Task<ResponseData<ListModel<Gem>>> Handle(GetListOfGems request, CancellationToken cancellationToken)
    {
        var pageSize = Math.Min(request.pageSize, _maxPageSize);

        var query = db.Gems.Include(g => g.Type).AsNoTracking();

        if (!string.IsNullOrEmpty(request.categoryNormalizedName))
        {
            query = query.Where(g => g.Type != null && g.Type.NormalizedName == request.categoryNormalizedName);
        }

        var totalCount = await query.CountAsync(cancellationToken);
        var totalPages = (int)Math.Ceiling(totalCount / (double)(pageSize > 0 ? pageSize : 1));

        if (request.pageNo > totalPages && totalCount > 0)
        {
            return ResponseData<ListModel<Gem>>.Error("Номер страницы превышает общее количество страниц");
        }

        var items = await query
            .Skip((request.pageNo - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync(cancellationToken);

        var listModel = new ListModel<Gem>
        {
            Items = items,
            PageNo = request.pageNo,
            PageSize = pageSize,
            TotalCount = totalCount
        };

        return ResponseData<ListModel<Gem>>.Ok(listModel);
    }
}
