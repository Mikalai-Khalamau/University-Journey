using System.Text.Json.Serialization;
using WEB_453503_Khalamau.Domain.Entities;
using WEB_453503_Khalamau.UI.Extensions;

namespace WEB_453503_Khalamau.UI.Models;

public class SessionCart : Cart
{
    [JsonIgnore]
    public ISession? Session { get; set; }

    public static Cart GetCart(IServiceProvider services)
    {
        var session = services.GetRequiredService<IHttpContextAccessor>()
            .HttpContext?.Session;
        var cart = session?.Get<SessionCart>("cart") ?? new SessionCart();
        cart.Session = session;
        return cart;
    }

    public override void AddToCart(Gem gem)
    {
        base.AddToCart(gem);
        Session?.Set("cart", this);
    }

    public override void RemoveItems(int id)
    {
        base.RemoveItems(id);
        Session?.Set("cart", this);
    }

    public override void ClearAll()
    {
        base.ClearAll();
        Session?.Set("cart", this);
    }
}
