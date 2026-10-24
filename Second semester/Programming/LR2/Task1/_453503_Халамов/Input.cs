namespace _453503_Халамов
{
    internal class Input
    {
        public static int GetSizeLength(string side)
        {
            int sideLength=0;
            bool isValidInput = false;

            while (!isValidInput)
            {
                Console.WriteLine($"Пожалуйста, введите длину {side}:");
                string input = Console.ReadLine();

                isValidInput = int.TryParse(input, out sideLength);

                if (!isValidInput || sideLength <= 0)
                {
                    Console.WriteLine("Некорректный ввод. Пожалуйста, введите положительное целое число.");
                    isValidInput = false; 
                }
            }

            return sideLength;
        }
    }
}