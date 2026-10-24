using System;

namespace _453503_Халамов
{
    class Program
    {
        static void Main(string[] args)
        {
            bool working = true;

            while (working)
            {
                Functions.MainFunction();

                Console.WriteLine("Введите цифру 1 для продолжения, иначе выполнение программы завершится");

                int check;

                while (true)
                {
                    string input = Console.ReadLine();

                    if (int.TryParse(input, out check))
                    {
                        break;
                    }
                    else
                    {
                        Console.WriteLine("Некорректный ввод. Пожалуйста, введите целое положительное число.");
                    }
                }

                switch (check)
                {
                    case 1:
                        working = true;
                        break;
                    default:
                        working = false;
                        break;
                }
            }
        }
    }
}