using Microsoft.EntityFrameworkCore;
using WEB_453503_Khalamau.Domain.Entities;

namespace WEB_453503_Khalamau.API.Data;

public static class DbInitializer
{
    public static async Task SeedData(WebApplication app)
    {
        using var scope = app.Services.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();

        await context.Database.MigrateAsync();

        var baseUrl = app.Configuration["ApiSettings:BaseUrl"];

        if (await context.GemTypes.AnyAsync())
        {
            return; 
        }

        var preciousType = new GemType
        {
            Name = "Драгоценный",
            NormalizedName = "precious"
        };
        var semiPreciousType = new GemType
        {
            Name = "Полудрагоценный",
            NormalizedName = "semi-precious"
        };

        context.GemTypes.AddRange(preciousType, semiPreciousType);
        await context.SaveChangesAsync();

        var gems = new List<Gem>
        {
            new Gem
            {
                Name = "Рубин",
                Description = "Драгоценный камень красного цвета",
                Type = preciousType,
                Price = 5000,
                Image = $"{baseUrl}/Images/ruby.jpg",
                MimeType = "image/jpeg"
            },
            new Gem
            {
                Name = "Алмаз",
                Description = "Самый твёрдый драгоценный камень",
                Type = preciousType,
                Price = 10000,
                Image = $"{baseUrl}/Images/diamond.jpg",
                MimeType = "image/jpeg"
            },
            new Gem
            {
                Name = "Сапфир",
                Description = "Драгоценный камень синего цвета",
                Type = preciousType,
                Price = 4500,
                Image = $"{baseUrl}/Images/sapphire.jpg",
                MimeType = "image/jpeg"
            },
            new Gem
            {
                Name = "Изумруд",
                Description = "Драгоценный камень зелёного цвета",
                Type = preciousType,
                Price = 6000,
                Image = $"{baseUrl}/Images/emerald.jpg",
                MimeType = "image/jpeg"
            },
            new Gem
            {
                Name = "Аметист",
                Description = "Полудрагоценный камень фиолетового цвета",
                Type = semiPreciousType,
                Price = 500,
                Image = $"{baseUrl}/Images/amethyst.jpg",
                MimeType = "image/jpeg"
            },
            new Gem
            {
                Name = "Жемчуг",
                Description = "Органический полудрагоценный камень",
                Type = semiPreciousType,
                Price = 800,
                Image = $"{baseUrl}/Images/pearl.jpg",
                MimeType = "image/jpeg"
            },
            new Gem
            {
                Name = "Гранат",
                Description = "Полудрагоценный камень тёмно-красного цвета",
                Type = semiPreciousType,
                Price = 400,
                Image = $"{baseUrl}/Images/garnet.jpg",
                MimeType = "image/jpeg"
            }
        };

        context.Gems.AddRange(gems);
        await context.SaveChangesAsync();
    }
}