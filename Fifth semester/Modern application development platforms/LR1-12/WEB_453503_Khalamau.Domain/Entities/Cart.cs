namespace WEB_453503_Khalamau.Domain.Entities;

public class Cart
{
    public Dictionary<int, CartItem> CartItems { get; set; } = new();

    public virtual void AddToCart(Gem gem)
    {
        if (CartItems.TryGetValue(gem.Id, out var cartItem))
        {
            cartItem.Count++;
        }
        else
        {
            CartItems[gem.Id] = new CartItem { Item = gem, Count = 1 };
        }
    }

    public virtual void RemoveItems(int id)
    {
        CartItems.Remove(id);
    }

    public virtual void ClearAll()
    {
        CartItems.Clear();
    }

    public int Count => CartItems.Sum(item => item.Value.Count);
    public decimal TotalPrice => CartItems.Sum(item => item.Value.Item.Price * item.Value.Count);
}
