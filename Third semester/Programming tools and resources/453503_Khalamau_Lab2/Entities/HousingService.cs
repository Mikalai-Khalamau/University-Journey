using System;
using System.Collections.Generic;
using System.Linq;
using System.Numerics;
using _453503_Khalamau_Lab2.Collections;
using _453503_Khalamau_Lab2.Contracts;
using _453503_Khalamau_Lab2.Entities;

namespace _453503_Khalamau_Lab2.Entities
{
    // Сервис управления жильцами, тарифами и потреблением коммунальных услуг.
    // Обобщённый тип T позволяет работать с любыми числовыми типами (int, double, decimal и т.д.)

    public class HousingService<T> : IHousingService<T> where T : INumber<T>
    {
        // События
        public event EventHandler<string>? TariffsOrResidentsChanged;
        public event EventHandler<string>? ServicePurchased;

        // Основные коллекции данных
        private readonly MyCustomCollection<Tariff> tariffs = new();
        private readonly MyCustomCollection<Resident> residents = new();

        // Быстрые словари для мгновенного поиска по имени
        private readonly Dictionary<string, Tariff> tariffLookup = new();
        private readonly Dictionary<string, Resident> residentLookup = new();

        // Добавляет новый тариф (услугу) в систему.
        public void AddTariff(string serviceName, T unitPrice)
        {
            if (string.IsNullOrWhiteSpace(serviceName))
                throw new ArgumentException("Service name cannot be empty.");
            if (unitPrice.CompareTo(T.Zero) < 0)
                throw new ArgumentException("Unit price cannot be negative.");
            if (tariffLookup.ContainsKey(serviceName))
                throw new ArgumentException("Tariff already exists.");

            var tariff = new Tariff(serviceName, Convert.ToDecimal(unitPrice));
            tariffs.Add(tariff);
            tariffLookup[serviceName] = tariff;

            TariffsOrResidentsChanged?.Invoke(this, $"Добавлен тариф: {serviceName}");
        }

        // Добавляет нового жильца.
        public void AddResident(string surname)
        {
            if (string.IsNullOrWhiteSpace(surname))
                throw new ArgumentException("Surname cannot be empty.");
            if (residentLookup.ContainsKey(surname))
                throw new ArgumentException("Resident already exists.");

            var resident = new Resident(surname);
            residents.Add(resident);
            residentLookup[surname] = resident;

            TariffsOrResidentsChanged.Invoke(this, $"Добавлен жилец: {surname}");
        }

        // Добавляет запись о потреблении услуги жильцом.
        public void AddConsumption(string surname, string serviceName, T amount)
        {
            if (string.IsNullOrWhiteSpace(surname) || string.IsNullOrWhiteSpace(serviceName))
                throw new ArgumentException("Surname or service name cannot be empty.");
            if (amount.CompareTo(T.Zero) < 0)
                throw new ArgumentException("Amount cannot be negative.");

            // Быстрый поиск жильца и тарифа через словари (O(1))
            if (!residentLookup.TryGetValue(surname, out var resident))
                throw new ArgumentException("Resident not found.");
            if (!tariffLookup.ContainsKey(serviceName))
                throw new ArgumentException("Service not found.");

            resident.Consumptions.Add(new Consumption(serviceName, Convert.ToDecimal(amount)));

            ServicePurchased?.Invoke(this, $"Жилец '{surname}' купил услугу '{serviceName}' ({amount})");
        }

        // Возвращает общую сумму по всем услугам конкретного жильца.
        public T GetTotalCostForResident(string surname)
        {
            if (!residentLookup.TryGetValue(surname, out var resident))
                throw new ArgumentException("Resident not found.");

            return T.CreateChecked(resident.GetTotalCost(tariffs));
        }

        // Возвращает суммарную стоимость всех услуг по всем жильцам.
        public T GetTotalServicesCost()
            => T.CreateChecked(EnumerateResidents().Sum(r => r.GetTotalCost(tariffs)));

        // Возвращает общее количество заказов по конкретной услуге.
        public int GetOrdersCountForService(string serviceName)
            => EnumerateResidents().Sum(r => r.CountConsumptionsForService(serviceName));

        // Возвращает список всех тарифов в виде (Имя услуги, Цена).
        public MyCustomCollection<(string ServiceName, T UnitPrice)> GetTariffs()
        {
            var result = new MyCustomCollection<(string, T)>();
            foreach (var t in EnumerateTariffs())
                result.Add((t.ServiceName, T.CreateChecked(t.UnitPrice)));
            return result;
        }

        // Возвращает список всех жильцов (только фамилии).
        public MyCustomCollection<string> GetResidents()
        {
            var result = new MyCustomCollection<string>();
            foreach (var r in EnumerateResidents())
                result.Add(r.Surname);
            return result;
        }

        // Итератор для обхода всех жильцов (замена ручного while + Reset/Next).
        private IEnumerable<Resident> EnumerateResidents()
        {
            residents.Reset();
            while (residents.HasCurrent)
            {
                yield return residents.Current();
                residents.Next();
            }
        }

        // Итератор для обхода всех тарифов.
        private IEnumerable<Tariff> EnumerateTariffs()
        {
            tariffs.Reset();
            while (tariffs.HasCurrent)
            {
                yield return tariffs.Current();
                tariffs.Next();
            }
        }
    }
}
