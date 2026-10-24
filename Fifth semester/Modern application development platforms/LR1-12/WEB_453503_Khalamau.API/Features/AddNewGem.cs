using MediatR;
using System.Text.Json;
using FluentValidation;
using Microsoft.AspNetCore.Mvc;
using WEB_453503_Khalamau.API.Abstractions;
using WEB_453503_Khalamau.API.Data;
using WEB_453503_Khalamau.API.Use_Cases;
using WEB_453503_Khalamau.Domain.Entities;

namespace WEB_453503_Khalamau.API.Features;

public static class AddNewGem
{
    public sealed record RequestDTO(
        string Name,
        string Description,
        decimal Price,
        int TypeId);

    private static readonly JsonSerializerOptions ParseOptions =
        new() { PropertyNameCaseInsensitive = true };

    public class RequestValidator : AbstractValidator<RequestDTO>
    {
        public RequestValidator()
        {
            RuleFor(r => r.Name)
                .NotEmpty()
                .MaximumLength(100);

            RuleFor(r => r.Description)
                .NotEmpty();

            RuleFor(r => r.Price)
                .GreaterThan(0);

            RuleFor(r => r.TypeId)
                .GreaterThan(0);
        }
    }
    public sealed class Endpoint : IEndpoint
    {
        public void MapEndpoint(IEndpointRouteBuilder app)
        {
            app.MapPost("/api/gems", Handler)
               .DisableAntiforgery()
               .WithName("CreateGem_Vertical")
               .WithTags("Gems")
               .RequireAuthorization("admin");
        }
    }
    public static async Task<IResult> Handler(
        [FromForm] string gem,
        [FromForm] IFormFile? file,
        AppDbContext db,
        IMediator mediator,
        IHttpContextAccessor httpContextAccessor,
        IValidator<RequestDTO> validator,
        CancellationToken cancellationToken)
    {
        RequestDTO? request;
        try
        {
            request = JsonSerializer.Deserialize<RequestDTO>(gem, ParseOptions);
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

        var gemType = await db.GemTypes.FindAsync(request.TypeId);
        if (gemType == null)
        {
            return TypedResults.BadRequest("Указанный тип камня не найден");
        }

        var newGem = new Gem
        {
            Name = request.Name,
            Description = request.Description,
            Price = request.Price,
            Type = gemType,
            Image = "Images/noimage.jpg",
            MimeType = "image/jpeg"
        };

        if (file is not null)
        {
            newGem.Image = await mediator.Send(new SaveImage(file), cancellationToken);
            newGem.MimeType = file.ContentType;
        }
        else
        {
            var httpContext = httpContextAccessor.HttpContext;
            if (httpContext is not null)
            {
                newGem.Image = $"{httpContext.Request.Scheme}://{httpContext.Request.Host}/Images/noimage.jpg";
            }
        }

        db.Gems.Add(newGem);
        await db.SaveChangesAsync(cancellationToken);

        return TypedResults.Created($"/api/gems/{newGem.Id}", newGem);
    }
}
