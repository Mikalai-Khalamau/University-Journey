using Microsoft.EntityFrameworkCore;
using WEB_453503_Khalamau.API.Abstractions;
using WEB_453503_Khalamau.API.Data;
using WEB_453503_Khalamau.Domain.Entities;
using WEB_453503_Khalamau.Domain.Models;

namespace WEB_453503_Khalamau.API.Features;

public static class GetGemById
{
    public sealed class Endpoint : IEndpoint
    {
        public void MapEndpoint(IEndpointRouteBuilder app)
        {
            app.MapGet("/api/gems/{id:int}", Handler)
               .WithName("GetGemById_Vertical")
               .WithTags("Gems")
               .AllowAnonymous();
        }
    }

    public static async Task<IResult> Handler(int id, AppDbContext db)
    {
        var gem = await db.Gems
            .Include(g => g.Type)
            .AsNoTracking()
            .FirstOrDefaultAsync(g => g.Id == id);

        return gem is null
            ? TypedResults.NotFound(ResponseData<Gem>.Error($"Камень с id={id} не найден"))
            : TypedResults.Ok(ResponseData<Gem>.Ok(gem));
    }
}
