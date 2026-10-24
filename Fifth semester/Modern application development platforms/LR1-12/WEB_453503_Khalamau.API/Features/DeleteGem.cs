using MediatR;
using Microsoft.EntityFrameworkCore;
using WEB_453503_Khalamau.API.Abstractions;
using WEB_453503_Khalamau.API.Data;
using WEB_453503_Khalamau.API.Use_Cases;
using WEB_453503_Khalamau.Domain.Entities;
using WEB_453503_Khalamau.Domain.Models;

namespace WEB_453503_Khalamau.API.Features;

public static class DeleteGem
{
    public sealed class Endpoint : IEndpoint
    {
        public void MapEndpoint(IEndpointRouteBuilder app)
        {
            app.MapDelete("/api/gems/{id:int}", Handler)
               .WithName("DeleteGem_Vertical")
               .WithTags("Gems")
               .RequireAuthorization("admin");
        }
    }

    public static async Task<IResult> Handler(
        int id,
        AppDbContext db,
        IMediator mediator,
        CancellationToken cancellationToken)
    {
        var gem = await db.Gems.FirstOrDefaultAsync(g => g.Id == id, cancellationToken);

        if (gem is null)
        {
            return TypedResults.NotFound(ResponseData<Gem>.Error($"Камень с id={id} не найден"));
        }

        await mediator.Send(new DeleteImage(gem.Image), cancellationToken);

        db.Gems.Remove(gem);
        await db.SaveChangesAsync(cancellationToken);

        return TypedResults.Ok(ResponseData<Gem>.Ok(gem));
    }
}
