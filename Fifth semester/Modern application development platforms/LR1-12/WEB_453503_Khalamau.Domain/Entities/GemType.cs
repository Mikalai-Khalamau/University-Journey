using System.Text.Json.Serialization;

namespace WEB_453503_Khalamau.Domain.Entities;

public class GemType
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string NormalizedName { get; set; } = string.Empty;

    [JsonIgnore]
    public List<Gem> Gems { get; set; } = new();
}
