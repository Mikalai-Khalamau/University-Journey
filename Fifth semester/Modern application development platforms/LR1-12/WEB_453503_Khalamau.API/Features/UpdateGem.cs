using MediatR;
using System.Text.Json;
using FluentValidation;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using WEB_453503_Khalamau.API.Abstractions;
using WEB_453503_Khalamau.API.Data;
using WEB_453503_Khalamau.API.Use_Cases;
using WEB_453503_Khalamau.Domain.Models;

namespace WEB_453503_Khalamau.API.Features;

public static class UpdateGem
{
    private static readonly JsonSerializerOptions ParseOptions =
        new() { PropertyNameCaseInsensitive = true };

    public sealed class Endpoint : IEndpoint
    {
        public void MapEndpoint(IEndpointRouteBuilder app)
        {
            app.MapPut("/api/gems/{id:int}", Handler)
               .DisableAntiforgery()
               .WithName("UpdateGem_Vertical")
               .WithTags("Gems")
               .RequireAuthorization("admin");
        }
    }

    public static async Task<IResult> Handler(
        int id,
        [FromForm] string gem,
        [FromForm] IFormFile? file,
        AppDbContext db,
        IMediator mediator,
        IValidator<AddNewGem.RequestDTO> validator,
        CancellationToken cancellationToken)
    {
        var existingGem = await db.Gems
            .Include(g => g.Type)
            .FirstOrDefaultAsync(g => g.Id == id, cancellationToken);

        if (existingGem is null)
        {
            return TypedResults.NotFound(ResponseData<Domain.Entities.Gem>.Error($"Камень с id={id} не найден"));
        }

        AddNewGem.RequestDTO? request;
        try
        {
            request = JsonSerializer.Deserialize<AddNewGem.RequestDTO>(gem, ParseOptions);
        }
        catch (JsonException ex)
        {
            return TypedResults.BadRequest($"Некорректные данные объекта: {ex.Message}");
        }

        if (request is null)
        {
            return TypedResults.BadRequest("Данные объекта не переданы");
        }

        var validationResult = await validator.ValidateAsync(request);
        if (!validationResult.IsValid)
        {
            return TypedResults.BadRequest(
                validationResult.Errors.Select(e => e.ErrorMessage));
        }

        var gemType = await db.GemTypes.FindAsync(new object[] { request.TypeId }, cancellationToken);
        if (gemType is null)
        {
            return TypedResults.BadRequest("Указанный тип камня не найден");
        }

        if (file is not null)
        {
            await mediator.Send(new DeleteImage(existingGem.Image), cancellationToken);
            existingGem.Image = await mediator.Send(new SaveImage(file), cancellationToken);
            existingGem.MimeType = file.ContentType;
        }

        existingGem.Name = request.Name;
        existingGem.Description = request.Description;
        existingGem.Price = request.Price;
        existingGem.Type = gemType;

        await db.SaveChangesAsync(cancellationToken);

        return TypedResults.Ok(ResponseData<Domain.Entities.Gem>.Ok(existingGem));
    }
}
