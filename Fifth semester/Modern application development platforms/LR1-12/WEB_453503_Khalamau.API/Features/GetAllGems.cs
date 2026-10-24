using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Caching.Hybrid;
using WEB_453503_Khalamau.API.Abstractions;
using WEB_453503_Khalamau.API.Data;
using WEB_453503_Khalamau.Domain.Entities;
using WEB_453503_Khalamau.Domain.Models;

namespace WEB_453503_Khalamau.API.Features;

public static class GetAllGems
{
    private const int MaxPageSize = 20;

    public sealed class Endpoint : IEndpoint
    {
        public void MapEndpoint(IEndpointRouteBuilder app)
        {
            app.MapGet("/api/gems/{category:regex([a-zA-Z\\-]+)?}", Handler)
               .WithName("GetAllGems_Vertical")
               .WithTags("Gems")
               .RequireAuthorization();
        }
    }

    public static async Task<IResult> Handler(
        string? category,
        AppDbContext db,
        HybridCache cache,
        int pageNo = 1,        
        int pageSize = 3)      
    {
        var actualPageSize = Math.Min(pageSize, MaxPageSize);

        var listModel = await cache.GetOrCreateAsync(
            $"gems_{category}_{pageNo}_{actualPageSize}",
            async token =>
            {
                var query = db.Gems.Include(g => g.Type).AsNoTracking();

                if (!string.IsNullOrEmpty(category))
                {
                    query = query.Where(g => g.Type != null && g.Type.NormalizedName == category);
                }

                var totalCount = await query.CountAsync(token);

                var items = await query
                    .Skip((pageNo - 1) * actualPageSize)
                    .Take(actualPageSize)
                    .ToListAsync(token);

                return new ListModel<Gem>
                {
                    Items = items,
                    PageNo = pageNo,
                    PageSize = actualPageSize,
                    TotalCount = totalCount
                };
            },
            options: new HybridCacheEntryOptions
            {
                Expiration = TimeSpan.FromMinutes(1),
                LocalCacheExpiration = TimeSpan.FromSeconds(30)
            }
        );

        return TypedResults.Ok(ResponseData<ListModel<Gem>>.Ok(listModel));
    }
}
