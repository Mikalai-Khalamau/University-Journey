using System.Numerics;
using _453503_Khalamau_Lab1.Collections;

namespace _453503_Khalamau_Lab1.Contracts
{
    public interface IHousingService<T> where T : INumber<T>
    {
        void AddTariff(string serviceName, T unitPrice);
        void AddResident(string surname);
        void AddConsumption(string surname, string serviceName, T amount);
        T GetTotalCostForResident(string surname);
        T GetTotalServicesCost();
        int GetOrdersCountForService(string serviceName);

        MyCustomCollection<(string ServiceName, T UnitPrice)> GetTariffs();

        MyCustomCollection<string> GetResidents();

    }
}
