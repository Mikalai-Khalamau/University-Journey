using System;
using System.Collections.Generic;
using System.Numerics;

namespace _453503_Khalamau_Lab3.Entities
{
    public class Consumption<T> where T : INumber<T>
    {
        public string ServiceName { get; set; }
        public T Amount { get; set; }

        public Consumption(string serviceName, T amount)
        {
            if (string.IsNullOrWhiteSpace(serviceName))
                throw new ArgumentException("Service cannot be empty");
            ServiceName = serviceName;
            Amount = amount;
        }

        public T CalculateCost(Dictionary<string, T> tariffs)
        {
            if (!tariffs.TryGetValue(ServiceName, out var price))
                throw new ArgumentException($"No tariff for {ServiceName}");
            return price * Amount;
        }
    }
}
