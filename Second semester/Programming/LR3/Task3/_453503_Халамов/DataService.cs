using System.Globalization;

namespace _453503_Халамов.Task3
{
    internal class DataService
    {
        public static int GetDaysSpan(DateTime date)
        {
            DateTime currentDate = DateTime.Now;
            return (date - currentDate).Days;
        }

        public static string GetDayOfWeek(string sdate)
        {
            DateTime dateTime = DateTime.ParseExact(sdate, "yyyy-MM-dd", CultureInfo.InvariantCulture);
            return dateTime.ToString("dddd", new CultureInfo("ru-RU"));
        }
    }
}