namespace _453503_Khalamau_Lab2.Entities
{
    public class Consumption
    {
        // Название услуги (должно совпадать с названием тарифа)
        public string ServiceName { get; }

        // Объем потребления (например, 100 кубов)
        public decimal Amount { get; }

        public Consumption(string serviceName, decimal amount)
        {
            if (string.IsNullOrEmpty(serviceName))
                throw new ArgumentException("Service name cannot be empty");
            if (amount < 0)
                throw new ArgumentException("Amount cannot be negative");

            ServiceName = serviceName;
            Amount = amount;
        }

        // Вычисляет стоимость данного потребления по списку тарифов
        public decimal CalculateCost(IEnumerable<Tariff> tariffs)
        {
            var tariff = tariffs.FirstOrDefault(t => t.ServiceName == ServiceName);
            if (tariff == null)
                throw new ArgumentException($"No tariff found for service '{ServiceName}'.");

            return tariff.CalculateCost(Amount);
        }
        public override string ToString()
            => $"Service: {ServiceName}, Amount: {Amount}";
    }

}
