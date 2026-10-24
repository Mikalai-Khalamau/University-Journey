namespace _453503_Халамов
{
    internal class Triangle
    {
        public static void IsEquilateral(int a, int b, int c)
        {
            if (a+b<=c || a+c<=b || b+c<=a)
            {
                Console.WriteLine("Фигура не является треугольником");
            }
            else if (a == b && b == c)
            {
                Console.WriteLine($"Треугольник является равносторонним, длина сторон: {a}");
            }
            else
            {
                Console.WriteLine($"Треугольник с длинами сторон {a} {b} {c} не является равносторонним");
            }
        }
    }
}