namespace WEB_453503_Khalamau.Domain.Entities;

public class Gem
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public int? TypeId { get; set; }
    public GemType? Type { get; set; }
    public decimal Price { get; set; } 
    public string? Image { get; set; } 
    public string? MimeType { get; set; }
}