using System;

namespace Lab4
{
    internal class Tariff
    {
        public double CostOfTariff { get; private set; }

        public Tariff(double cost)
        {
            CostOfTariff = cost;
        }

        // Увеличение стоимости тарифа
        public void IncreaseCost(double value)
        {
            CostOfTariff += value;
        }

        // Уменьшение стоимости тарифа с проверкой, чтобы не стало отрицательным
        public void DecreaseCost(double value)
        {
            if (CostOfTariff - value < 0)
            {
                CostOfTariff = 0;  // Если уменьшить до отрицательного значения, то ставим 0
            }
            else
            {
                CostOfTariff -= value;
            }
        }

        // Метод для обновления стоимости тарифа напрямую
        public void SetCostOfTariff(double value)
        {
            CostOfTariff = value;
        }
    }
}
