namespace _453503_Khalamau_Lab3.Entities
{
    public class Tariff
    {
        public string Name { get; set; }
        public decimal Price { get; set; }

        public Tariff(string name, decimal price)
        {
            Name = name;
            Price = price;
        }

        public override string ToString() => $"{Name} — {Price} руб.";
    }
}
