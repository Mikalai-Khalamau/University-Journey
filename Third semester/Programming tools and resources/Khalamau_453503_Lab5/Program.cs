using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Microsoft.Extensions.Configuration;
using Khalamau_453503_Lab5.Domain;
using SerializerLib;

namespace Khalamau_453503_Lab5
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;
            Console.WriteLine("Лабораторная работа №5: Сериализация\n");

            try
            {
                // 1. Чтение имени файла из appsettings.json
                string fileName = GetFileNameFromConfig();
                Console.WriteLine($"Имя файла из конфигурации: {fileName}\n");

                // 2. Создание коллекции билетов
                List<Ticket> tickets = CreateTickets();
                Console.WriteLine("Создана коллекция билетов:");
                PrintTickets(tickets);

                // 3. Создание объекта сериализатора
                Serializer serializer = new Serializer();

                // 4. Сериализация в три разных файла
                Console.WriteLine("\nСЕРИАЛИЗАЦИЯ");
                serializer.SerializeByLINQ(tickets, fileName);
                serializer.SerializeXML(tickets, fileName);
                serializer.SerializeJSON(tickets, fileName);

                // 5. Десериализация из трёх файлов
                Console.WriteLine("\nДЕСЕРИАЛИЗАЦИЯ");

                var ticketsFromLINQ = serializer.DeSerializeByLINQ(fileName);
                var ticketsFromXML = serializer.DeSerializeXML(fileName);
                var ticketsFromJSON = serializer.DeSerializeJSON(fileName);

                // 6. Проверка совпадения данных
                Console.WriteLine("\nПРОВЕРКА ДАННЫХ");

                bool linqMatch = CompareTickets(tickets, ticketsFromLINQ, "LINQ to XML");
                bool xmlMatch = CompareTickets(tickets, ticketsFromXML, "XmlSerializer");
                bool jsonMatch = CompareTickets(tickets, ticketsFromJSON, "JSON");

                // 7. Итоговый результат
                Console.WriteLine("\nИТОГИ");
                Console.WriteLine($"LINQ to XML:    {(linqMatch ? "Данные совпадают" : "Данные не совпадают")}");
                Console.WriteLine($"XmlSerializer:  {(xmlMatch ? "Данные совпадают" : "Данные не совпадают")}");
                Console.WriteLine($"JSON:           {(jsonMatch ? "Данные совпадают" : "Данные не совпадают")}");

                Console.WriteLine("\nЛабораторная работа выполнена успешно!");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\nОшибка: {ex.Message}");
                Console.WriteLine($"Тип исключения: {ex.GetType().Name}");
            }

            Console.WriteLine("\nНажмите любую клавишу для выхода...");
            Console.ReadKey();
        }

        // Чтение имени файла из appsettings.json
        static string GetFileNameFromConfig()
        {
            var configuration = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
                .Build();

            string? fileName = configuration["FileSettings:FileName"];

            if (string.IsNullOrEmpty(fileName))
            {
                throw new Exception("Не удалось прочитать имя файла из конфигурации!");
            }

            return fileName;
        }

        // Создание коллекции билетов с тестовыми данными
        static List<Ticket> CreateTickets()
        {
            List<Ticket> tickets = new List<Ticket>
            {
                new Ticket(
                    "T001",
                    new DateTime(2025, 11, 25, 14, 30, 0),
                    "Минск",
                    "Москва",
                    150.50m,
                    new Passenger("Иванов Иван Иванович", "AB1234567", 35, "+375-29-123-45-67")
                ),
                new Ticket(
                    "T002",
                    new DateTime(2025, 11, 26, 10, 15, 0),
                    "Минск",
                    "Санкт-Петербург",
                    180.00m,
                    new Passenger("Петрова Анна Сергеевна", "CD9876543", 28, "+375-29-987-65-43")
                ),
                new Ticket(
                    "T003",
                    new DateTime(2025, 11, 27, 18, 45, 0),
                    "Москва",
                    "Казань",
                    95.75m,
                    new Passenger("Сидоров Петр Александрович", "EF5551234", 42, "+7-916-555-12-34")
                ),
                new Ticket(
                    "T004",
                    new DateTime(2025, 11, 28, 08, 00, 0),
                    "Минск",
                    "Варшава",
                    220.00m,
                    new Passenger("Козлова Мария Дмитриевна", "GH7778899", 31, "+375-44-777-88-99")
                ),
                new Ticket(
                    "T005",
                    new DateTime(2025, 11, 29, 16, 20, 0),
                    "Гомель",
                    "Минск",
                    45.50m,
                    new Passenger("Морозов Алексей Викторович", "IJ3334455", 25, "+375-33-333-44-55")
                )
            };

            return tickets;
        }

        // Вывод коллекции билетов на экран
        static void PrintTickets(IEnumerable<Ticket> tickets)
        {
            int count = 1;
            foreach (var ticket in tickets)
            {
                Console.WriteLine($"{count}. {ticket}");
                count++;
            }
        }

        // Сравнение двух коллекций билетов
        static bool CompareTickets(IEnumerable<Ticket> original, IEnumerable<Ticket> deserialized, string method)
        {
            var originalList = original.ToList();
            var deserializedList = deserialized.ToList();

            if (originalList.Count != deserializedList.Count)
            {
                Console.WriteLine($"{method}: Количество билетов не совпадает!");
                return false;
            }

            // Используем SequenceEqual - он использует Equals из IEquatable
            bool isEqual = originalList.SequenceEqual(deserializedList);

            if (isEqual)
            {
                Console.WriteLine($"{method}: Все данные совпадают!");
            }
            else
            {
                Console.WriteLine($"{method}: Данные не совпадают!");

                // Найдём, какой именно билет отличается
                for (int i = 0; i < originalList.Count; i++)
                {
                    if (!originalList[i].Equals(deserializedList[i]))
                    {
                        Console.WriteLine($"  Отличие в билете #{i + 1}:");
                        Console.WriteLine($"  Оригинал:        {originalList[i]}");
                        Console.WriteLine($"  Десериализован:  {deserializedList[i]}");
                    }
                }
            }

            return isEqual;
        }
    }
}
