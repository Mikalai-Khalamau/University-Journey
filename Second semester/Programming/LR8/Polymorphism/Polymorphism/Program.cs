using Polymorphism;

class Program
{
    static void Main(string[] args)
    {
        try
        {
            // 1. Демонстрация работы через интерфейсные ссылки
            Console.WriteLine("=== Демонстрация ===");

            IPrice noDiscountStrategy = new NoDiscount(5000);
            IPrice discountStrategy = new Discount(4000, 10);

            Console.WriteLine($"Цена без скидки: {noDiscountStrategy.GetPrice()} руб.");
            Console.WriteLine($"Цена со скидкой: {discountStrategy.GetPrice()} руб.");

            // 2. Демонстрация паттерна Strategy в работе аэропорта
            Console.WriteLine("\n=== Работа аэропорта ===");

            Airport airport = new Airport();

            airport.AddTariff(new Tariff("Москва", 5000));
            airport.AddTariff(new Tariff("Санкт-Петербург", 4000, 10));
            airport.AddTariff(new Tariff("Сочи", 3000));
            airport.AddTariff(new Tariff("Калининград", 3500, 15));

            Tariff maxTariff = airport.GetMaxTariff();
            Console.WriteLine($"Самый дорогой тариф: {maxTariff.Name} - {maxTariff.Price} руб.");

        }
        catch (Exception ex)
        {
            Console.WriteLine($"Произошла ошибка: {ex.Message}");
        }
    }
}