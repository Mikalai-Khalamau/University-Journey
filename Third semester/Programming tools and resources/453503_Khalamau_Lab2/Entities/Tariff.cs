namespace _453503_Khalamau_Lab2.Entities
{
    public class Tariff
    {
        // Название услуги, например "Вода" или "Электричество"
        public string ServiceName { get; }

        // Цена за единицу услуги (например, 1 куб воды)
        public decimal UnitPrice { get; }

        public Tariff(string serviceName, decimal unitPrice)
        {
            if (string.IsNullOrEmpty(serviceName))
                throw new ArgumentException("Service name cannot be empty");
            if (unitPrice < 0)
                throw new ArgumentException("Price cannot be negative");

            ServiceName = serviceName;
            UnitPrice = unitPrice;
        }

        // Метод вычисляет стоимость услуги по количеству потребления
        public decimal CalculateCost(decimal amount)
        {
            if (amount < 0)
                throw new ArgumentException("Amount cannot be negative.");
            return UnitPrice * amount;
        }
        public override string ToString()
            => $"Service: {ServiceName}, UnitPrice: {UnitPrice}";
    }

}
 