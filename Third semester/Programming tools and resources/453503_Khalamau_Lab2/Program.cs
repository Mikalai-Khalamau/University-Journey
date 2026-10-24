using System;
using _453503_Khalamau_Lab2.Collections;
using _453503_Khalamau_Lab2.Entities;

namespace _453503_Khalamau_Lab2
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8; // чтобы корректно показывать кириллицу

            var housingService = new HousingService<decimal>(); // основной сервис
            var journal = new Journal(); // журнал событий

            // 🔹 Подписываем журнал на события
            //housingService.TariffsOrResidentsChanged += journal.RecordEvent;
            housingService.ServicePurchased += journal.RecordEvent;

            // 🔹 Подписка программы (лямбда-выражение) на покупки услуг
            housingService.ServicePurchased += (sender, info) =>
            {
                Console.WriteLine($"[Событие] {info}");
            };

            Console.WriteLine("=== Демонстрация событий и исключений ===\n");

            // 1. Добавляем тарифы
            try
            {
                housingService.AddTariff("Вода", 2.5m);
                housingService.AddTariff("Электричество", 1.2m);
                housingService.AddTariff("", 1m);

                // Ошибка: повторное добавление тарифа
                housingService.AddTariff("Вода", 3.0m);
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"[Ошибка] {ex.Message}");
            }

            // 2. Добавляем жильцов
            try
            {
                housingService.AddResident("Иванов");
                housingService.AddResident("Петров");

                // Ошибка: дубликат жильца
                housingService.AddResident("Иванов");
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"[Ошибка] {ex.Message}");
            }

            // 3. Добавляем потребление услуг
            try
            {
                housingService.AddConsumption("Иванов", "Вода", 100);
                housingService.AddConsumption("Петров", "Электричество", 50);

                // Ошибка: отрицательное количество
                housingService.AddConsumption("Иванов", "Вода", -10);
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"[Ошибка] {ex.Message}");
            }

            // Ошибка: несуществующий тариф
            try
            {
                housingService.AddConsumption("Иванов", "Газ", 15);
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"[Ошибка] {ex.Message}");
            }

            // Ошибка: несуществующий жилец
            try
            {
                housingService.AddConsumption("Сидоров", "Вода", 30);
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"[Ошибка] {ex.Message}");
            }

            // 4. Проверяем работу с коллекцией и исключения MyCustomCollection
            try
            {
                var residents = housingService.GetResidents();

                Console.WriteLine("\nСписок жильцов:");
                foreach (var r in residents)
                    Console.WriteLine(r);

                Console.WriteLine("\nТест неправильного индекса:");
                Console.WriteLine(residents[10]); // IndexOutOfRangeException
            }
            catch (IndexOutOfRangeException ex)
            {
                Console.WriteLine($"[Ошибка коллекции] {ex.Message}");
            }

            try
            {
                // Проверка Remove, если элемента нет
                var tariffs = housingService.GetTariffs();
                tariffs.Remove(("Газ", 5m)); // своё пользовательское исключение
            }
            catch (ItemNotFoundException ex)
            {
                Console.WriteLine($"[Ошибка коллекции] {ex.Message}");
            }

            // 5. Вывод итогов
            Console.WriteLine("\n=== Итоговые данные ===");
            Console.WriteLine($"Общая стоимость услуг: {housingService.GetTotalServicesCost()}");
            Console.WriteLine($"Заказы на воду: {housingService.GetOrdersCountForService("Вода")}");

            // 6. Вывод журнала событий
            Console.WriteLine();
            journal.PrintJournal();

            Console.WriteLine("\n=== Программа завершена ===");
        }
    }
}

