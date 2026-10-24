using Microsoft.Data.Sqlite;
using Microsoft.EntityFrameworkCore;
using WEB_453503_Khalamau.API.Data;
using WEB_453503_Khalamau.API.Services;
using WEB_453503_Khalamau.Domain.Entities;
using Xunit;

namespace WEB_453503_Khalamau.Tests;

public class GemServiceTests : IDisposable
{
    private readonly SqliteConnection _connection;
    private readonly DbContextOptions<AppDbContext> _contextOptions;

    public GemServiceTests()
    {
        _connection = new SqliteConnection("Filename=:memory:");
        _connection.Open();

        _contextOptions = new DbContextOptionsBuilder<AppDbContext>()
            .UseSqlite(_connection)
            .Options;

        using var context = new AppDbContext(_contextOptions);
        context.Database.EnsureCreated();
        SeedDatabase(context);
    }

    private void SeedDatabase(AppDbContext context)
    {
        var type1 = new GemType { Id = 1, Name = "Precious", NormalizedName = "precious" };
        var type2 = new GemType { Id = 2, Name = "Semi-Precious", NormalizedName = "semi-precious" };

        context.GemTypes.AddRange(type1, type2);

        for (int i = 1; i <= 5; i++)
        {
            context.Gems.Add(new Gem
            {
                Id = i,
                Name = $"Gem {i}",
                Description = $"Desc {i}",
                Price = 100 * i,
                TypeId = i <= 3 ? 1 : 2,
                Type = i <= 3 ? type1 : type2
            });
        }

        context.SaveChanges();
    }

    public void Dispose()
    {
        _connection.Dispose();
    }

    private AppDbContext CreateContext() => new AppDbContext(_contextOptions);

    [Fact]
    public async Task ServiceReturnsFirstPageOfThreeItems()
    {
        using var context = CreateContext();
        var service = new GemService(context);
        var result = await service.GetGemListAsync(null, 1);

        Assert.NotNull(result);
        Assert.True(result.Successfull);
        Assert.Equal(1, result.Data!.PageNo);
        Assert.Equal(3, result.Data.Items.Count());
        Assert.Equal(2, result.Data.TotalPages);
        Assert.Equal("Gem 1", result.Data.Items.First().Name);
    }

    [Fact]
    public async Task ServiceSelectsGivenPage()
    {
        using var context = CreateContext();
        var service = new GemService(context);
        var result = await service.GetGemListAsync(null, 2);

        Assert.NotNull(result);
        Assert.True(result.Successfull);
        Assert.Equal(2, result.Data!.PageNo);
        Assert.Equal(2, result.Data.Items.Count());
        Assert.Equal("Gem 4", result.Data.Items.First().Name);
    }

    [Fact]
    public async Task ServiceFiltersObjectsByCategory()
    {
        using var context = CreateContext();
        var service = new GemService(context);
        var result = await service.GetGemListAsync("semi-precious", 1);

        Assert.NotNull(result);
        Assert.True(result.Successfull);
        Assert.Equal(2, result.Data!.TotalCount);
        Assert.Equal("Gem 4", result.Data.Items.First().Name);
    }

    [Fact]
    public async Task ServiceCapsPageSizeAtMaximum()
    {
        using var context = CreateContext();
        var service = new GemService(context);
        var result = await service.GetGemListAsync(null, 1, 100);

        Assert.NotNull(result);
        Assert.True(result.Successfull);
        Assert.Equal(GemService.MaxPageSize, result.Data!.PageSize);
    }

    [Fact]
    public async Task ServiceReturnsUnsuccessful_WhenPageExceedsTotal()
    {
        using var context = CreateContext();
        var service = new GemService(context);
        var result = await service.GetGemListAsync(null, 10);

        Assert.NotNull(result);
        Assert.False(result.Successfull);
    }
}
