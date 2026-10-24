namespace _453503_Халамов
{
    internal class Input
    {
        public static double GetSizeLength(string axis)
        {
            bool isValidInput = false;
            double coordinate = 0;

            while (!isValidInput)
            {
                Console.WriteLine($"Пожалуйста, введите координату по оси {axis}");
                string input = Console.ReadLine();

                isValidInput = double.TryParse(input, out coordinate);

                if (!isValidInput)
                {
                    Console.WriteLine("Некорректный ввод. Пожалуйста, введите число.");
                    isValidInput = false;
                }
            }
            return coordinate;
        }
    }
}