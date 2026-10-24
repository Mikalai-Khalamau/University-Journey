using System;
using System.Collections.Generic;
using System.Linq;

namespace Collections
{
    internal class Demonstration
    {
        static void Main(string[] args)
        {
            var housingOffice = HousingOffice.GetInstance();


            while (true)
            {
                Console.Clear();
                Console.WriteLine("Меню:");
                Console.WriteLine("0 - Информация о задании");
                Console.WriteLine("1 - Добавить услугу");
                Console.WriteLine("2 - Добавить жильца");
                Console.WriteLine("3 - Стоимость услуг жильца");
                Console.WriteLine("4 - Общая сумма услуг");
                Console.WriteLine("5 - Список услуг с ценами");
                Console.WriteLine("6 - Список жильцов с их углугами");
                Console.WriteLine("7 - Секрет");
                Console.WriteLine("8 - Выход");

                var choice = GetMenuChoice();

                switch (choice)
                {
                    case 0: ShowTaskInfo(); break;
                    case 1: AddTariff(housingOffice); break;
                    case 2: AddResident(housingOffice); break;
                    case 3: ShowResidentSum(housingOffice); break;
                    case 4: ShowTotalSum(housingOffice); break;
                    case 5: ShowTariffs(housingOffice); break;
                    case 6: ShowResidents(housingOffice); break;
                    case 7: ShowSecret(); break;
                    case 8: return;
                }

                Console.WriteLine("\nНажмите любую клавишу для продолжения...");
                Console.ReadKey();
            }
        }

        static int GetMenuChoice()
        {
            while (true)
            {
                Console.Write("\nВыберите пункт (0-8): ");
                if (int.TryParse(Console.ReadLine(), out int choice) && choice >= 0 && choice <= 8)
                    return choice;
                Console.WriteLine("Ошибка: введите число от 0 до 8");
            }
        }

        static void ShowTaskInfo()
        {
            Console.WriteLine("Предметная область: ЖЭС.\n" +
                            "В ЖЭС хранятся тарифы на коммунальные услуги.\n" +
                            "Система позволяет:\n" +
                            "- Вводить тарифы\n" +
                            "- Добавлять жильцов\n" +
                            "- Рассчитывать суммы платежей\n\n" +
                            "Лабораторная работа №5. Выполнил студент группы 453503 Халамов Н.");
        }

        static void AddTariff(HousingOffice housingOffice)
        {
            string title;
            while (true)
            {
                try
                {
                    Console.Write("Введите название услуги: ");
                    title = Console.ReadLine().Trim();
                    var tempTariff = new Tariff(0, title);
                    break;
                }
                catch (ArgumentException ex)
                {
                    Console.WriteLine($"Ошибка: {ex.Message}");
                }
            }

            double cost;
            while (true)
            {
                try
                {
                    Console.Write("Введите стоимость: ");
                    string input = Console.ReadLine();
                    var tempTariff = new Tariff(double.Parse(input), "temp");
                    cost = tempTariff.Cost;
                    break;
                }
                catch (Exception ex) when (ex is FormatException || ex is ArgumentOutOfRangeException)
                {
                    Console.WriteLine($"Ошибка: {ex.Message}");
                }
            }

            try
            {
                housingOffice.AddTariff(new Tariff(cost, title));
                Console.WriteLine($"Услуга '{title}' успешно добавлена");
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"Ошибка: {ex.Message}");

                Console.WriteLine("Попробуйте ввести другое название услуги");
            }
        }


        static void AddResident(HousingOffice housingOffice)
        {

            // 1. Ввод и валидация фамилии
            string name;
            while (true)
            {
                Console.Write("Введите фамилию жильца: ");
                name = Console.ReadLine()?.Trim();

                // Проверка через временный объект
                try
                {
                    var testResident = new Resident(name, ResidentType.Regular);
                    break;
                }
                catch (ArgumentException ex)
                {
                    Console.WriteLine($"Ошибка: {ex.Message}");
                }
            }

            // 3. Ввод типа жильца
            ResidentType type;
            while (true)
            {
                Console.Write("Тип жильца (1-Regular, 2-WithFamily): ");
                var input = Console.ReadLine();

                if (input == "1")
                {
                    type = ResidentType.Regular;
                    break;
                }
                else if (input == "2")
                {
                    type = ResidentType.WithFamily;
                    break;
                }
                else
                {
                    Console.WriteLine("Ошибка: введите 1 или 2");
                }
            }
            try
            {
                
                var newResident = new Resident(name, type);
                housingOffice.AddResident(newResident); // Явное добавление в список

               
                AddTariffsToResident(housingOffice, newResident);

                Console.WriteLine($"\nЖилец '{name}' успешно добавлен!");
                Console.WriteLine($"Тип: {type}, Количество услуг: {newResident.UsedTariffs.Count}");
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"Ошибка: {ex.Message}");

                Console.WriteLine("Попробуйте ввести другую фамилию жильца");
            }
            
        }







        static void AddTariffsToResident(HousingOffice housingOffice, Resident resident)
        {
            if (housingOffice.listTariff.Count == 0)
            {
                Console.WriteLine("Нет доступных услуг для добавления");
                return;
            }

            while (true)
            {
                Console.WriteLine("\nДоступные услуги:");
                housingOffice.listTariff.ForEach(t => Console.WriteLine($"- {t.Title}"));

                Console.Write("Добавить услугу? (1-Да, 2-Нет): ");
                var choice = Console.ReadLine();

                if (choice == "2") break;
                if (choice != "1")
                {
                    Console.WriteLine("Ошибка: введите 1 или 2");
                    continue;
                }

                try
                {
                    Console.Write("Введите название услуги: ");
                    var tariffName = Console.ReadLine()?.Trim();

                    // Проверяем, существует ли тариф
                    var tariff = housingOffice.GetTariffByName(tariffName);

                    if (tariff == null)
                    {
                        Console.WriteLine($"Ошибка: Услуга '{tariffName}' не найдена.");
                        continue; // Возвращаемся в цикл, а не выходим из метода
                    }

                    // Проверяем, не была ли эта услуга уже добавлена
                    if (resident.UsedTariffs.Contains(tariff))
                    {
                        Console.WriteLine($"Ошибка: Услуга '{tariff.Title}' уже добавлена.");
                        continue; // Возвращаемся в цикл, а не выходим из метода
                    }

                    // Добавляем услугу, если она прошла все проверки
                    resident.UsedTariffs.Add(tariff);
                    Console.WriteLine($"Услуга '{tariff.Title}' успешно добавлена.");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Ошибка: {ex.Message}");
                }
            }
        }



        static void ShowResidentSum(HousingOffice housingOffice)
        {
            try
            {
                Console.Write("Введите фамилию жильца: ");
                var name = Console.ReadLine()?.Trim();

                // Полностью доверяем проверке в сеттере Resident
                var resident = housingOffice.listResident
                    .FirstOrDefault(r => r.Name.Equals(name, StringComparison.OrdinalIgnoreCase));

                if (resident == null)
                    throw new KeyNotFoundException("Жилец не найден");

                double sum = resident.UsedTariffs.Sum(t => t.Cost);
                Console.WriteLine($"Сумма услуг для {name}: {sum} руб.");
            }
            catch (ArgumentException ex) // Ловим ошибки валидации из сеттера
            {
                Console.WriteLine($"Ошибка: {ex.Message}");
            }
            catch (KeyNotFoundException ex)
            {
                Console.WriteLine($"Ошибка: {ex.Message}");
            }
        }
        static void ShowTotalSum(HousingOffice housingOffice)
        {
            Console.WriteLine($"Общая сумма всех услуг: {housingOffice.CalculateTotalSum()} руб.");
        }

        static void ShowTariffs(HousingOffice housingOffice)
        {
            if (housingOffice.listTariff.Count == 0)
            {
                Console.WriteLine("Список услуг пуст");
                return;
            }

            Console.WriteLine("Список услуг:");
            housingOffice.listTariff.ForEach(t =>
                Console.WriteLine($"- {t.Title}: {t.Cost} руб."));
        }

        static void ShowResidents(HousingOffice housingOffice)
        {
            if (housingOffice.listResident.Count == 0)
            {
                Console.WriteLine("Список жильцов пуст");
                return;
            }

            Console.WriteLine("Список жильцов:");
            foreach (var r in housingOffice.listResident)
            {
                Console.WriteLine($"\n{r.Name} ({r.Type})");
                if (r.UsedTariffs.Count > 0)
                {
                    Console.WriteLine("Услуги:");
                    r.UsedTariffs.ForEach(t => Console.WriteLine($"  - {t.Title}: {t.Cost} руб."));
                }
                else
                {
                    Console.WriteLine("Нет назначенных услуг");
                }
            }
        }

        static void ShowSecret()
        {
            Console.WriteLine("1 апреля близко...");
        }
    }
}