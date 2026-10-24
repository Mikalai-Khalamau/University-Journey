namespace _453503_Халамов.Services
{
    internal class Input
    {
        public static double GetNumber(string x)
        {
            double number = 0;
            bool isValidInput = false;

            while (!isValidInput)
            {
                Console.WriteLine($"Пожалуйста, введите число {x}:");
                string input = Console.ReadLine();

                isValidInput = double.TryParse(input, out number);

                if (!isValidInput)
                {
                    Console.WriteLine("Некорректный ввод. Пожалуйста, введите число.");
                    isValidInput = false;
                }
            }

            return number;
        }
    }
}
