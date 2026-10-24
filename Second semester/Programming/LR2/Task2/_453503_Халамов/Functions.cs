namespace _453503_Халамов
{
    internal class Functions
    {
        public static void MainFunction()
        {
            Display.ConsoleMenu();

            double x = Input.GetSizeLength("Ox");
            double y = Input.GetSizeLength("Oy");

            Point.Check(x,y);
        }
    }
}
