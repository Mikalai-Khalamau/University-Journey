using System;
using System.Globalization;
namespace _453503_Халамов.Task3
{ 
    internal class Input
    {
        public static int GetNumber(string prompt) {
            int number;
            while (true)
            {
                Console.WriteLine($"Введите {prompt}:");
                if (int.TryParse(Console.ReadLine(), out number))
                {
                    return number;
                }
                Console.WriteLine("Некорректный ввод. Пожалуйста, введите целое число.");
            }
        }
       
    

    public static bool IsValidDate(string sdate)
    {
        if (DateTime.TryParseExact(sdate, "yyyy-MM-dd", null, System.Globalization.DateTimeStyles.None, out _))
        {
            return true;
        }

        Console.WriteLine("Дата некорректна. Дата должна существовать в календаре (с учетом високосных годов).");
        return false;
    }
}
}