using _453503_Khalamau_Lab2.Collections;

namespace _453503_Khalamau_Lab2.Entities
{
    public class Resident
    {
        public string Surname
        {
            get;
        }
        public MyCustomCollection<Consumption> Consumptions
        {
            get;
        }
        public Resident(string surname)
        {
            if (string.IsNullOrEmpty(surname))
            {
                throw new ArgumentException("Surname can not be empty");
            }
            Surname = surname;
            Consumptions = new MyCustomCollection<Consumption>();
        }

        public decimal GetTotalCost(MyCustomCollection<Tariff> tariffs)
        {
            decimal total = 0;
            Consumptions.Reset();
            while (Consumptions.HasCurrent)
            {
                var c = Consumptions.Current();
                var tariff = FindTariff(tariffs, c.ServiceName);
                if (tariff != null)
                {
                    total += tariff.CalculateCost(c.Amount);
                }
                Consumptions.Next();
            }
            return total;
        }

        private Tariff FindTariff(MyCustomCollection<Tariff> tariffs, string serviceName)
        {
            tariffs.Reset();
            while (tariffs.HasCurrent)
            {
                var t = tariffs.Current();
                if (t.ServiceName == serviceName)
                    return t;
                tariffs.Next();
            }
            return null;
        }

        public int CountConsumptionsForService(string serviceName)
        {
            int count = 0;
            Consumptions.Reset();
            while (Consumptions.HasCurrent)
            {
                if (Consumptions.Current().ServiceName == serviceName)
                    count++;
                Consumptions.Next();
            }
            return count;
        }
        public override string ToString()
        {
            return $"Surname: {Surname}";
        }
    }
}
