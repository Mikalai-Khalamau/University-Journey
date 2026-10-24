using System;
using System.Collections.Generic;
using System.Linq;

namespace Collections
{
    internal class HousingOffice
    {
        private static HousingOffice _instance;
        private static readonly object _lock = new object();

        public List<Tariff> listTariff { get; set; }
        public List<Resident> listResident { get; set; }

        private HousingOffice()
        {
            listTariff = new List<Tariff>();
            listResident = new List<Resident>();
        }

        public static HousingOffice GetInstance()
        {
            if (_instance == null)
            {
                lock (_lock)
                {
                    if (_instance == null)
                    {
                        _instance = new HousingOffice();
                    }
                }
            }
            return _instance;
        }

        public void AddResident(Resident resident)
        {
            if (listResident.Any(r => r.Name.Equals(resident.Name, StringComparison.OrdinalIgnoreCase)))
            {
                throw new ArgumentException($"Жилец с именем '{resident.Name}' уже существует");
            }
            listResident.Add(resident);
        }

        public void AddTariff(Tariff tariff)
        {
            if (listTariff.Any(t => t.Title.Equals(tariff.Title, StringComparison.OrdinalIgnoreCase)))
            {
                throw new ArgumentException($"Тариф с названием '{tariff.Title}' уже существует");
            }
            listTariff.Add(tariff);
        }

        public double CalculateResidentSum(string residentName)
        {
            var resident = listResident.FirstOrDefault(r =>
                r.Name.Equals(residentName, StringComparison.OrdinalIgnoreCase));
            return resident?.UsedTariffs.Sum(t => t.Cost) ?? 0;
        }

        public double CalculateTotalSum()
        {
            return listResident.Sum(r => r.UsedTariffs.Sum(t => t.Cost));
        }

        public Tariff GetTariffByName(string name)
        {
            return listTariff.FirstOrDefault(t =>t.Title.Equals(name, StringComparison.OrdinalIgnoreCase));
        }
    }
}