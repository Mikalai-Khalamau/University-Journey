using System;

namespace Lab4
{
    internal class HousingService
    {
        private static HousingService? instance;

        public string District { get; private set; }
        public int NumberOfService { get; private set; }
        public int NumberOfRoomers { get; private set; }
        public int NumberOfPayers { get; private set; }
        public Tariff tariff { get; private set; }

        private HousingService(string district, int numberOfService, int numberOfRoomers, int numberOfPayers, double costOfTariff)
        {
            this.District = district;
            this.NumberOfService = numberOfService;
            this.NumberOfRoomers = numberOfRoomers;
            this.NumberOfPayers = numberOfPayers;
            this.tariff = new Tariff(costOfTariff);
        }

        public static void Initialize(string district, int numberOfService, int numberOfRoomers, int numberOfPayers, double costOfTariff)
        {
            if (instance == null)
            {
                instance = new HousingService(district, numberOfService, numberOfRoomers, numberOfPayers, costOfTariff);
            }
            else
            {
                instance.District = district;
                instance.NumberOfService = numberOfService;
                instance.NumberOfRoomers = numberOfRoomers;
                instance.NumberOfPayers = numberOfPayers;
                instance.tariff.SetCostOfTariff(costOfTariff);  // Обновление стоимости тарифа
            }
        }

        public static HousingService GetInstance()
        {
            if (instance == null)
            {
                throw new InvalidOperationException("Экземпляр не был инициализирован. Вызовите Initialize() перед использованием.");
            }
            return instance;
        }

        public void IncreaseCost(double value)
        {
            tariff.IncreaseCost(value);
        }

        public void DecreaseCost(double value)
        {
            tariff.DecreaseCost(value);
        }

        public double Arrear()
        {
            return tariff.CostOfTariff * (NumberOfRoomers - NumberOfPayers);
        }

        public void UpdateRoomersAndPayers(int newRoomers, int newPayers)
        {
            NumberOfRoomers = newRoomers;
            NumberOfPayers = newPayers;
        }
    }
}
