using System;
using System.Globalization;

namespace _453503_Халамов.Task3
{
    internal class Program
    {
        static void Main(string[] args)
        {
            bool working = true;

            while (working)
            {
                
                Console.WriteLine("Выберите действие:");
                Console.WriteLine("1. Определить день недели для даты");
                Console.WriteLine("2. Рассчитать разницу между датами");
                Console.WriteLine("0. Завершить программу");

                int action;

                while (true)
                {
                    if (int.TryParse(Console.ReadLine(), out action) && action >= 0 && action <= 2)
                    {
                        break;
                    }
                    Console.WriteLine("Некорректный ввод. Пожалуйста, выберите 1, 2 или 0.");
                }

                switch (action)
                {
                    case 1:
                        Task.DayOfWeek();
                        break;

                    case 2:
                        Task.Difference();
                        break;

                    case 0:
                        working = false;
                        break;
                }

                if (working)
                {
                    Console.WriteLine("Введите 1 для продолжения, любую другую цифру для выхода:");
                    int check;
                    while (!int.TryParse(Console.ReadLine(), out check))
                    {
                        Console.WriteLine("Некорректный ввод. Введите целое число.");
                    }

                    if (check != 1)
                    {
                        working = false;
                    }
                }
            }

            Console.WriteLine("Программа завершена.");
        }
    }
}