namespace Khalamau_453503.Domain.Entities;

public class Order : Entity
{
    public string Name { get; set; } = string.Empty;  

    public int Time
    {
        get
        {
            int mx = 0;
            foreach (var p in Pizzas)
                if (p.Time > mx)
                    mx = p.Time;
            return mx;
        }
    }

    public List<Pizza> Pizzas { get; set; } = new();
}