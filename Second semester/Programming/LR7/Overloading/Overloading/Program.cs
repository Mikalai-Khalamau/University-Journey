using System;

namespace Overloading
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Демонстрация работы класса QuadraticEquation ===");

            // 1. Создание объектов (демонстрация конструкторов)
            Console.WriteLine("\n1. Создание объектов:");
            var eq1 = new QuadraticEquation(1, -5, 6); // Конструктор с параметрами
            var eq2 = new QuadraticEquation();         // Конструктор по умолчанию (x^2 -2x +1 =0)
            var eq3 = (QuadraticEquation)3;            // Явное преобразование (3x^2 =0)

            Console.WriteLine($"eq1: {eq1}");
            Console.WriteLine($"eq2: {eq2}");
            Console.WriteLine($"eq3: {eq3}");

            // 2. Демонстрация свойств
            Console.WriteLine("\n2. Работа свойств:");
            eq1.B = -3; // Изменение коэффициента b
            try
            {
                eq1.A = 0; // Попытка задать a=0 (выбросит исключение)
            }
            catch (ArgumentException ex)
            {
                Console.WriteLine($"Ошибка: {ex.Message}");
            }
            Console.WriteLine($"Изменённое eq1: {eq1}");

            // 3. Демонстрация индексатора
            Console.WriteLine("\n3. Работа индексатора:");
            Console.WriteLine($"eq1[0] (коэф. a): {eq1[0]}");
            Console.WriteLine($"eq1[1] (коэф. b): {eq1[1]}");
            Console.WriteLine($"eq1[2] (коэф. c): {eq1[2]}");
            eq1[2] = 10; // Изменение коэффициента c через индексатор
            Console.WriteLine($"Изменённое eq1: {eq1}");

            // 4. Демонстрация методов
            Console.WriteLine("\n4. Работа методов:");
            Console.WriteLine($"Корни eq1: [{string.Join(", ", eq1.FindRoots())}]");
            Console.WriteLine($"Корни eq2: [{string.Join(", ", eq2.FindRoots())}]");
            Console.WriteLine($"Корни eq3: [{string.Join(", ", eq3.FindRoots())}]");

            // 5. Демонстрация операторов
            Console.WriteLine("\n5. Работа операторов:");
            // Математические операторы
            Console.WriteLine($"eq1 + eq2: {eq1 + eq2}");
            Console.WriteLine($"eq1 - eq2: {eq1 - eq2}");
            Console.WriteLine($"eq1 * 2: {eq1 * 2}");
            Console.WriteLine($"eq1 / 2: {eq1 / 2}");
            // Инкремент и декремент 
            Console.WriteLine($"++eq1: {++eq1}");
            Console.WriteLine($"--eq1: {--eq1}");
            // Операторы сравнения
            Console.WriteLine($"eq1 == eq2: {eq1 == eq2}");
            Console.WriteLine($"eq1 != eq2: {eq1 != eq2}");
            // true/false
            Console.WriteLine($"if(eq1): {(eq1 ? "Есть корни" : "Нет корней")}");
            Console.WriteLine($"if(eq2): {(eq2 ? "Есть корни" : "Нет корней")}");
            // Преобразование типов
            Console.WriteLine($"(int)eq1: {(int)eq1}");
            Console.WriteLine($"(int)eq2: {(int)eq2}");
            Console.WriteLine($"(int)eq3: {(int)eq3}");
        }
    }
}