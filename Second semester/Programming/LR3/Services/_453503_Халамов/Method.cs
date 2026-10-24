namespace _453503_Халамов.Services
{
    internal class Method
    {
        public static void Function(double k, double z)
        {
            double x;
            if (k < 1)
            {
                Console.WriteLine("Вычисление производилось по первой ветке");
                 x = k * Math.Pow(z, 3);
            }
            else
            {
                Console.WriteLine("Вычисление производилось по второй ветке");
                 x = z * (z + 1);
            }

            double a = Math.Log(1 + x * x)+Math.Cos(1+x);
            double b = Math.Exp(k * x);

            double y = Math.Pow(a, b);
            Console.WriteLine($"Значение функции равно {y}");
        }
    }
}
