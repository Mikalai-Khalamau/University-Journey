using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Polymorphism
{
    internal class Airport
    {
        private List<Tariff> tariffs;

        public Airport()
        {
            tariffs = new List<Tariff>();
        }
        public void AddTariff(Tariff tariff)
        {
            tariffs.Add(tariff);
        }

        public Tariff GetMaxTariff()
        {
            if (tariffs.Count == 0)
                throw new InvalidOperationException("Нет добавленных тарифов");
            Tariff maxTariff = tariffs[0];
            for (int i = 1; i < tariffs.Count; i++)
            {
                if (maxTariff.Price < tariffs[i].Price)
                {
                    maxTariff = tariffs[i];
                }
            }
            return maxTariff;
        }

    }
}
