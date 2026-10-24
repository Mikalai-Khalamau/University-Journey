using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace _453503_Халамов.Task3
{
    internal class Task
    {
        public static void DayOfWeek()
        {
            
            while (true)
            {
                Console.WriteLine("Введите дату в формате гггг-мм-дд:");
                string sdate = Console.ReadLine();

                if (Input.IsValidDate(sdate))
                {
                    string dayOfWeek = DataService.GetDayOfWeek(sdate);
                    Console.WriteLine($"День недели: {dayOfWeek}");
                    break; 
                }
            }
        }

        public static void Difference()
        {

            while (true)
            {
                int year = Input.GetNumber("год");
                int month = Input.GetNumber("месяц");
                int day = Input.GetNumber("день");

                try
                {
                    DateTime date = new DateTime(year, month, day); // Если дата неверная, вызовет исключение
                    int daysDifference = DataService.GetDaysSpan(date);
                    Console.WriteLine($"Разница между датами: {daysDifference} дней.");
                    break;
                }
                catch (ArgumentOutOfRangeException)
                {
                    Console.WriteLine("Введена некорректная дата. Попробуйте еще раз.");
                }
            }

        }
    }
}
