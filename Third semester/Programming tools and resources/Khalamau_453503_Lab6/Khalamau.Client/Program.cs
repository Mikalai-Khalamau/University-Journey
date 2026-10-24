using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using Khalamau.Domain;
using Khalamau.Mediator;
using Khalamau.UseCases;

namespace Khalamau.Client
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;
            Console.WriteLine("Лабораторная работа №6: Сборки и метаданные\n");

            try
            {
                // a) Создание коллекции объектов MenuItem
                var menuItems = CreateMenu();
                Console.WriteLine("Создана коллекция позиций меню:");
                PrintMenu(menuItems);

                // b) Создание экземпляра ISender с указанием сборки UseCases
                Assembly useCasesAssembly = Assembly.GetAssembly(typeof(SaveData))!;
                ISender sender = new Sender(useCasesAssembly);
                Console.WriteLine();

                // c) Сохранение коллекции в файл через медиатор
                string fileName = "menu.json";
                Console.WriteLine("СОХРАНЕНИЕ ДАННЫХ");
                sender.Send(new SaveData(menuItems, fileName));

                // d) Чтение данных из файла через медиатор
                Console.WriteLine("\nЧТЕНИЕ ДАННЫХ");
                var loadedItems = sender.Send(new ReadFile(fileName));

                // e) Вывод прочитанной коллекции
                Console.WriteLine("\nПрочитанная коллекция:");
                PrintMenu(loadedItems);

                // f) Сравнение коллекций
                Console.WriteLine("\nПРОВЕРКА ДАННЫХ");
                bool isEqual = CompareCollections(menuItems, loadedItems);

                Console.WriteLine("\nИТОГИ");
                if (isEqual)
                {
                    Console.WriteLine("Коллекции полностью совпадают!");
                }
                else
                {
                    Console.WriteLine("Коллекции не совпадают!");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"\nОшибка: {ex.Message}");
                Console.WriteLine($"Тип исключения: {ex.GetType().Name}");
            }

            Console.WriteLine("\nНажмите любую клавишу для выхода...");
            Console.ReadKey();
        }

        // Создание тестовой коллекции позиций меню
        static List<MenuItem> CreateMenu()
        {
            return new List<MenuItem>
            {
                new MenuItem("Пицца Маргарита", 450, true),
                new MenuItem("Пицца Пепперони", 520, true),
                new MenuItem("Пицца 4 Сыра", 480, false),
                new MenuItem("Паста Карбонара", 380, true),
                new MenuItem("Ризотто с грибами", 420, false)
            };
        }

        // Вывод меню на экран
        static void PrintMenu(IEnumerable<MenuItem> items)
        {
            int count = 1;
            foreach (var item in items)
            {
                Console.WriteLine($"{count}. {item}");
                count++;
            }
        }

        // Сравнение двух коллекций с использованием IEquatable
        static bool CompareCollections(IEnumerable<MenuItem> original, IEnumerable<MenuItem> loaded)
        {
            var originalList = original.ToList();
            var loadedList = loaded.ToList();

            if (originalList.Count != loadedList.Count)
            {
                Console.WriteLine($"Количество элементов не совпадает: {originalList.Count} vs {loadedList.Count}");
                return false;
            }

            // Используем SequenceEqual - автоматически использует Equals из IEquatable
            bool isEqual = originalList.SequenceEqual(loadedList);

            if (isEqual)
            {
                Console.WriteLine($"Все элементы совпадают (проверено {originalList.Count} позиций)");
            }
            else
            {
                Console.WriteLine("Найдены различия:");
                for (int i = 0; i < originalList.Count; i++)
                {
                    if (!originalList[i].Equals(loadedList[i]))
                    {
                        Console.WriteLine($"  Позиция #{i + 1}:");
                        Console.WriteLine($"    Оригинал: {originalList[i]}");
                        Console.WriteLine($"    Загружено: {loadedList[i]}");
                    }
                }
            }

            return isEqual;
        }
    }
}
