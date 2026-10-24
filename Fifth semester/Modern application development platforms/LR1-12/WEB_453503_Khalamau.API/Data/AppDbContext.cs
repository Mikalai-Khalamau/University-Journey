using Microsoft.EntityFrameworkCore;
using WEB_453503_Khalamau.Domain.Entities;

namespace WEB_453503_Khalamau.API.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
    }

    public DbSet<Gem> Gems { get; set; }
    public DbSet<GemType> GemTypes { get; set; }
}