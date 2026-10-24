namespace WEB_453503_Khalamau.Domain.Entities;

public class CartItem
{
    public Gem Item { get; set; } = new();
    public int Count { get; set; }
}
