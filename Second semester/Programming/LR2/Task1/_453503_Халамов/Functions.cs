namespace _453503_Халамов
{
    internal class Functions
    {
        public static void MainFunction()
        {
            
            Display.ConsoleMenu();

            int a = Input.GetSizeLength("первой стороны");

            int b = Input.GetSizeLength("второй стороны");

            int c = Input.GetSizeLength("третьей стороны");

            Triangle.IsEquilateral(a, b, c);
        }
    }
}
