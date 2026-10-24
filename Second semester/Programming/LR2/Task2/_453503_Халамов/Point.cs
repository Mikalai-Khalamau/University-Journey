namespace _453503_Халамов
{
    internal class Point
    {
        public static void Check(double x, double y)
        {
            if (x * x + y * y == 9 || x * x + y * y == 49)
            {
                Console.WriteLine("Точка лежит на границе заштрихованной области\n");
            }
            else if (x * x + y * y > 9 && x * x + y * y < 49)
            {
                Console.WriteLine("Точка лежит внутри заштрихованной области\n");
            }
            else if (x * x + y * y < 9 || x * x + y * y > 49)
            {
                Console.WriteLine("Точка лежит вне заштрихованной области\n");
            }
        }
    }
}