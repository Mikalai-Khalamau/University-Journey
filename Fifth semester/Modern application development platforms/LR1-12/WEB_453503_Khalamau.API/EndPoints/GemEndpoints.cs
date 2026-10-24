using Microsoft.EntityFrameworkCore;
using MediatR;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http.HttpResults;
using WEB_453503_Khalamau.API.Use_Cases;
using WEB_453503_Khalamau.API.Data;
using WEB_453503_Khalamau.Domain.Entities;
using Microsoft.Extensions.Caching.Hybrid;

namespace WEB_453503_Khalamau.API.EndPoints;

public static class GemEndpoints
{
    public static void MapGemEndpoints (this IEndpointRouteBuilder routes)
    {
        var group = routes.MapGroup("/api/gems");

        group.MapGet("/{category:regex([a-zA-Z\\-]+)?}", async (
           IMediator mediator,
           HybridCache cache,
           string? category,
           int pageNo = 1,
           [FromQuery] int pageSize = 3) =>
        {
            var data = await cache.GetOrCreateAsync(
                $"gems_{category}_{pageNo}",
                async token => await mediator.Send(new GetListOfGems(category, pageNo, pageSize)),
                options: new HybridCacheEntryOptions
                {
                    Expiration = TimeSpan.FromMinutes(1),
                    LocalCacheExpiration = TimeSpan.FromSeconds(30)
                }
            );
            return TypedResults.Ok(data);
        })
       .WithName("GetAllGems")
       .WithOpenApi()
       .RequireAuthorization();

        group.MapGet("/{id}", async Task<Results<Ok<Gem>, NotFound>> (int id, AppDbContext db) =>
        {
            return await db.Gems.AsNoTracking()
                .FirstOrDefaultAsync(model => model.Id == id)
                is Gem model
                    ? TypedResults.Ok(model)
                    : TypedResults.NotFound();
        })
        .WithName("GetGemById")
        .WithOpenApi()
        .AllowAnonymous();

        group.MapPut("/{id}", async Task<Results<Ok, NotFound>> (int id, Gem gem, AppDbContext db) =>
        {
            var affected = await db.Gems
                .Where(model => model.Id == id)
                .ExecuteUpdateAsync(setters => setters
                    .SetProperty(m => m.Id, gem.Id)
                    .SetProperty(m => m.Name, gem.Name)
                    .SetProperty(m => m.Description, gem.Description)
                    .SetProperty(m => m.Price, gem.Price)
                    .SetProperty(m => m.Image, gem.Image)
                    .SetProperty(m => m.MimeType, gem.MimeType)
                    );
            return affected == 1 ? TypedResults.Ok() : TypedResults.NotFound();
        })
        .WithName("UpdateGem")
        .RequireAuthorization("admin");

        group.MapPost("/", async (Gem gem, AppDbContext db) =>
        {
            db.Gems.Add(gem);
            await db.SaveChangesAsync();
            return TypedResults.Created($"/api/Gem/{gem.Id}",gem);
        })
        .WithName("CreateGem")
        .RequireAuthorization("admin");

        group.MapDelete("/{id}", async Task<Results<Ok, NotFound>> (int id, AppDbContext db) =>
        {
            var affected = await db.Gems
                .Where(model => model.Id == id)
                .ExecuteDeleteAsync();
            return affected == 1 ? TypedResults.Ok() : TypedResults.NotFound();
        })
        .WithName("DeleteGem")
        .RequireAuthorization("admin");
    }
}
