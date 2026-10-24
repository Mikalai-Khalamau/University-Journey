using System.Collections.Generic;
using System.Numerics;

namespace _453503_Khalamau_Lab3.Contracts
{
    public interface IHousingService<T> where T : INumber<T>
    {
        Dictionary<string, T> Tariffs { get; }
        List<Entities.Resident<T>> Residents { get; }

        void AddTariff(string name, T price);
        void AddResident(string surname);
        void AddConsumption(string surname, string service, T amount);

        IEnumerable<string> GetSortedServices();
        T GetTotalCost();
        T GetTotalCostForResident(string surname);
        string GetRichestResident();
        int CountResidentsAbove(T threshold);
        IEnumerable<object> GetGroupedPayments();
    }
}
