using System;
using _453503_Khalamau_Lab1.Entities;
using _453503_Khalamau_Lab1.Collections;

namespace _453503_Khalamau_Lab1
{
    class Program
    {
        static void Main(string[] args)
        {
            var housingService = new HousingService<decimal>();

            housingService.AddTariff("Вода", 2.5m);
            housingService.AddTariff("Свет", 1.2m);

            housingService.AddResident("Матвей Денисович");
            housingService.AddResident("Евгений Васильевич");

            housingService.AddConsumption("Матвей Денисович", "Вода", 100m); 
            housingService.AddConsumption("Евгений Васильевич", "Свет", 50m);  
            housingService.AddConsumption("Матвей Денисович", "Вода", 200m); 

            Console.WriteLine("Тарифы:");
            var tariffs = housingService.GetTariffs();
            for (int i = 0; i < tariffs.Count; i++)
            {
                var tariff = tariffs[i]; 
                Console.WriteLine($"Service: {tariff.ServiceName}, Price: {tariff.UnitPrice}");
            }

            Console.WriteLine("\nЖильцы:");
            var residents = housingService.GetResidents();
            for (int i = 0; i < residents.Count; i++)
            {
                Console.WriteLine(residents[i]); 
            }

            Console.WriteLine($"\nСтоимость для Матвея Денисовича: {housingService.GetTotalCostForResident("Матвей Денисович")}"); 
            Console.WriteLine($"Общая стоимость услуг: {housingService.GetTotalServicesCost()}"); 
            Console.WriteLine($"Заказы на воду: {housingService.GetOrdersCountForService("Вода")}"); 
        }
    }
}
