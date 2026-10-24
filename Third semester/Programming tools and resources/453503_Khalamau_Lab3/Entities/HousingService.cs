using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using _453503_Khalamau_Lab3.Contracts;

namespace _453503_Khalamau_Lab3.Entities
{
    // Управляющий класс ЖЭС: хранит тарифы, жильцов и их потребления
    // генерирует события и предоставляет набор LINQ-методов для запросов
    // Обобщён по типу T (числовой тип), где T : INumber<T> 
 
    public class HousingService<T> : IHousingService<T> where T : INumber<T>
    {
        // Событие, вызываемое при изменении данных (добавлении тарифа или жильца).
        public event EventHandler<string>? DataChanged;

        // Событие, вызываемое при покупке/регистрации услуги жильцом.
        public event EventHandler<string>? ServicePurchased;

        // Словарь тарифов: имя услуги -> цена (типа T).
        public Dictionary<string, T> Tariffs { get; } = new();

        // Список жильцов; у каждого есть List<Consumption<T>> Consumptions.
        public List<Resident<T>> Residents { get; } = new();

        /// Добавляет новый тариф в словарь Tariffs.
        // - Проверяет уникальность по имени (бросает ArgumentException при дубликате).
        // - Добавляет запись Tariffs[name] = price.
        // - Вызывает событие DataChanged с текстовой информацией.
        // Примечание: изменение Tariffs повлияет на результаты отложенных LINQ-запросов,
        // возвращающих IEnumerable, если они ещё не были материализованы.
        public void AddTariff(string name, T price)
        {
            if (Tariffs.ContainsKey(name)) throw new ArgumentException("Tariff exists");
            Tariffs[name] = price;
            DataChanged?.Invoke(this, $"Added tariff {name} ({price})");
        }

        // Добавляет нового жильца (по фамилии).
        // - Проверяет наличие жильца с той же фамилией (по условию — фамилия уникальна).
        // - Создаёт Resident<T> и добавляет в Residents.
        // - Генерирует событие DataChanged.
        public void AddResident(string surname)
        {
            if (Residents.Any(r => r.Surname == surname)) throw new ArgumentException("Resident exists");
            Residents.Add(new Resident<T>(surname));
            DataChanged?.Invoke(this, $"Added resident {surname}");
        }

        // Добавляет запись о потреблении услуги жильцом:
        // - Находит жильца по фамилии (если не найден — ArgumentException).
        // - Проверяет, что тариф на услугу существует (иначе — ArgumentException).
        // - Добавляет Consumption<T> в Consumptions жильца.
        // - Генерирует событие ServicePurchased, передавая строковое описание.
        public void AddConsumption(string surname, string service, T amount)
        {
            var resident = Residents.FirstOrDefault(r => r.Surname == surname)
                          ?? throw new ArgumentException("Resident not found");
            if (!Tariffs.ContainsKey(service)) throw new ArgumentException("Service not found");
            resident.Consumptions.Add(new Consumption<T>(service, amount));
            ServicePurchased?.Invoke(this, $"Resident {surname} purchased {service} ({amount})");
        }

        // Возвращает перечисление имён всех услуг, отсортированных по стоимости (по возрастанию).
        // Реализация:
        // - Tariffs.OrderBy(t => t.Value) -- сортирует пары KeyValuePair<string, T> по цене;
        // - .Select(t => t.Key) -- выбирает имя услуги.
        public IEnumerable<string> GetSortedServices() =>
            Tariffs.OrderBy(t => t.Value).Select(t => t.Key);

        // Вычисляет общую (совокупную) стоимость всех услуг по всем жильцам.
        // Логика:
        // - Для каждого жильца r: вычисляем сумму стоимости его Consumptions:
        //     r.Consumptions.Aggregate(T.Zero, (a, c) => a + c.CalculateCost(Tariffs))
        // - Затем суммируем все эти суммы через внешний Aggregate (seed = T.Zero).
        // Использование Aggregate удобно для обобщённого типа T (INumber).
        // Этот метод выполняется немедленно и возвращает итоговое значение типа T.
        public T GetTotalCost() =>
            Residents.Aggregate(T.Zero, (acc, r) =>
                acc + r.Consumptions.Aggregate(T.Zero, (a, c) => a + c.CalculateCost(Tariffs)));

        // Вычисляет общую стоимость всех услуг, заказанных жильцом с фамилией surname.
        // - Сначала фильтруем жильцов: Where(r => r.Surname == surname).
        // - По результату применяем Aggregate, суммируя расходы найденных жильцов.
        // Если жильцов с этой фамилией нет, возвращается T.Zero.
        public T GetTotalCostForResident(string surname) =>
            Residents.Where(r => r.Surname == surname)
                     .Aggregate(T.Zero, (acc, r) =>
                         acc + r.Consumptions.Aggregate(T.Zero, (a, c) => a + c.CalculateCost(Tariffs)));

        // Находит фамилию жильца, заплатившего максимальную сумму:
        // - Для каждого жильца вычисляем сумму его расходов (внутренний Aggregate).
        // - Сортируем жильцов по убыванию суммы: OrderByDescending(...).
        // - Берём фамилию первого (Select(r => r.Surname).FirstOrDefault()).
        // Если жильцов нет — возвращаем "No data".
        // Замечание: при равных значениях максимума возвращается тот, кто окажется первым после сортировки 
        public string GetRichestResident() =>
            Residents.OrderByDescending(r => r.Consumptions.Aggregate(T.Zero, (a, c) => a + c.CalculateCost(Tariffs)))
                     .Select(r => r.Surname).FirstOrDefault() ?? "No data";

        // Возвращает количество жильцов, сумма оплат которых превышает заданный threshold.
        // Реализовано через Aggregate:
        // - Начальное значение (seed) = 0 (счётчик).
        // - Для каждого жильца вычисляем его суммарный платёж (внутренний Aggregate).
        // - Сравниваем сумму с threshold при помощи CompareTo (т.к. T обобщённый).
        // - Если sum > threshold, добавляем 1 к аккумулятору, иначе 0.
        // Метод возвращает int — количество жильцов, превысивших порог.
        public int CountResidentsAbove(T threshold) =>
            Residents.Aggregate(0, (acc, r) =>
            {
                var sum = r.Consumptions.Aggregate(T.Zero, (a, c) => a + c.CalculateCost(Tariffs));
                // сравнить sum > threshold: используем CompareTo
                return acc + (sum.CompareTo(threshold) > 0 ? 1 : 0);
            });

        // Для каждого жильца возвращает структуру (анонимную) с фамилией и списком оплат по услугам:
        // - Для каждого проживания группируем его Consumptions по ServiceName (GroupBy).
        // - В каждой группе считаем Total = сумма (Aggregate) стоимости данной услуги.
        // Возвращается IEnumerable<object>, где каждый объект имеет поля:
        // { Resident = string, Services = IEnumerable<{ Service: string, Total: T }> }.
        // Примечание: метод возвращает объекты анонимного типа => сигнатура IEnumerable<object>
        public IEnumerable<object> GetGroupedPayments()
        {
            return Residents.Select(r => new
            {
                Resident = r.Surname,
                Services = r.Consumptions
                    .GroupBy(c => c.ServiceName)
                    .Select(g => new
                    {
                        Service = g.Key,
                        Total = g.Aggregate(T.Zero, (a, c) => a + c.CalculateCost(Tariffs))
                    })
            });
        }
    }
}
