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
                int check = Convert.ToInt32(Console.ReadLine());

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