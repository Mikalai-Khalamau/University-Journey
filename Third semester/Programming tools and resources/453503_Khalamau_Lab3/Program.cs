using System;
using System.Linq;
using _453503_Khalamau_Lab3.Entities;

namespace _453503_Khalamau_Lab3
{
    class Program
    {
        static void Main()
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;

            // Используем обобщённую реализацию с decimal для демонстрации финансовых расчётов
            var service = new HousingService<decimal>();
            var journal = new Journal();

            // Подписываем журнал на события (DataChanged и ServicePurchased)
            service.DataChanged += journal.RecordEvent;
            service.ServicePurchased += journal.RecordEvent;

            // Подписка-лямбда: дополнительно печатаем события в консоль
            service.ServicePurchased += (s, e) => Console.WriteLine($"[Event] {e}");

            // 1) Добавляем тарифы
            Console.WriteLine("=== Добавляем тарифы ===");
            service.AddTariff("Вода", 2.5m);
            service.AddTariff("Электричество", 1.2m);
            service.AddTariff("Газ", 3.1m);

            // 2) Добавляем жильцов
            Console.WriteLine("\n=== Добавляем жильцов ===");
            service.AddResident("Иванов");
            service.AddResident("Петров");
            service.AddResident("Сидоров");

            // 3) Регистрируем потребления (услуги)
            Console.WriteLine("\n=== Регистрируем потребления ===");
            service.AddConsumption("Иванов", "Вода", 100m);          // 100 * 2.5 = 250
            service.AddConsumption("Иванов", "Газ", 30m);            // 30 * 3.1  = 93
            service.AddConsumption("Петров", "Электричество", 80m);  // 80 * 1.2  = 96
            service.AddConsumption("Сидоров", "Вода", 40m);          // 40 * 2.5  = 100
            service.AddConsumption("Сидоров", "Газ", 10m);           // 10 * 3.1  = 31

            // 4) Демонстрация GetSortedServices() и отложенного выполнения
            Console.WriteLine("\n=== Сервисы, отсортированные по цене (DEFERRED) ===");
            // Возвращается IEnumerable<string> — отложенный запрос
            var sorted = service.GetSortedServices();

            Console.WriteLine("Список (не материализированный) перед изменением тарифов:");
            foreach (var s in sorted) Console.WriteLine($" - {s}");

            // Изменим тариф после создания перечисления (но до материализации)
            service.AddTariff("Интернет", 2.0m); // добавим новый тариф по цене 2.0

            Console.WriteLine("\nСписок после добавления нового тарифа (при итерации повторно покажет обновлённые данные):");
            foreach (var s in sorted) Console.WriteLine($" - {s}");

            // Чтобы получить снимок на момент создания — материализуем
            var snapshot = service.GetSortedServices().ToList();
            // поменяем цену
            service.AddTariff("Телефон", 0.5m);
            Console.WriteLine("\nСнимок (ToList) уже не изменится, даже если добавлять новые тарифы:");
            foreach (var s in snapshot) Console.WriteLine($" * {s}");
            Console.WriteLine("А текущее динамическое перечисление показывает новые элементы:");

            foreach (var s in service.GetSortedServices()) Console.WriteLine($"   {s}");

            // 5) Полные агрегаты: общая стоимость всех услуг
            Console.WriteLine($"\n=== Общая стоимость всех услуг: {service.GetTotalCost()} ===");
            Console.WriteLine($"=== Стоимость для Иванова: {service.GetTotalCostForResident("Иванов")} ===");
            Console.WriteLine($"=== Стоимость для Петрова: {service.GetTotalCostForResident("Петров")} ===");
            Console.WriteLine($"=== Самый большой плательщик: {service.GetRichestResident()} ===");

            // 6) CountResidentsAbove (использует Aggregate)
            decimal threshold = 120m;
            Console.WriteLine($"\nЖильцы, заплатившие больше {threshold}: {service.CountResidentsAbove(threshold)}");

            // 7) GetGroupedPayments() — вывод подробной разбивки по услугам для каждого жильца
            Console.WriteLine("\n=== Подробная разбивка оплат по жильцам и услугам ===");
            var grouped = service.GetGroupedPayments();
            foreach (var res in grouped)
            {
                // res — анонимный тип: { Resident = string, Services = IEnumerable<{ Service, Total }> }
                var residentName = res.GetType().GetProperty("Resident")?.GetValue(res);
                Console.WriteLine($"\nЖилец: {residentName}");
                var services = (System.Collections.IEnumerable?)res.GetType().GetProperty("Services")?.GetValue(res);
                if (services != null)
                {
                    foreach (var svc in services)
                    {
                        var svcName = svc.GetType().GetProperty("Service")?.GetValue(svc);
                        var svcTotal = svc.GetType().GetProperty("Total")?.GetValue(svc);
                        Console.WriteLine($"  {svcName} — {svcTotal}");
                    }
                }
            }

            // 8) Обработка ошибок (демонстрация исключений)
            Console.WriteLine("\n=== Демонстрация обработки ошибок ===");
            try
            {
                service.AddConsumption("Иванов", "НеСуществующаяУслуга", 5m);
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"[Ошибка] {ex.Message}");
            }

            try
            {
                service.AddResident("Иванов"); // дубль по фамилии
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"[Ошибка] {ex.Message}");
            }

            // 9) Печать журнала событий
            Console.WriteLine("\n=== Журнал событий ===");
            journal.PrintJournal();

            // 10) Заключение / дополнительные проверки
            Console.WriteLine("\n=== Дополнительные проверки ===");
            Console.WriteLine($"Текущее количество жильцов: {service.Residents.Count}");
            Console.WriteLine($"Текущее количество тарифов: {service.Tariffs.Count}");

            Console.WriteLine("\n=== Конец демонстрации ===");
        }
    }
}
