using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using _453503_Khalamau_Lab4;

namespace _453503_Khalamau_Lab4
{
    class Program
    {
        static void Main()
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;

            string surname = "Khalamau"; 
            string folderName = $"{surname}_Lab4";
            string baseFolder = Path.Combine(Directory.GetCurrentDirectory(), folderName);

            // 1) Создать папку Khalamau_Lab4 (или очистить её)
            if (Directory.Exists(baseFolder))
            {
                Console.WriteLine($"Папка {baseFolder} уже существует. Удаляем всё содержимое...");
                // удаляем файлы
                foreach (var file in Directory.GetFiles(baseFolder))
                    File.Delete(file);

                // удаляем подкаталоги
                foreach (var dir in Directory.GetDirectories(baseFolder))
                    Directory.Delete(dir, true);

                Console.WriteLine("Содержимое папки удалено.");
            }
            else
            {
                Directory.CreateDirectory(baseFolder);
                Console.WriteLine($"Папка {baseFolder} создана.");
            }

            // 2) Заполнить папку 10-ю пустыми файлами с расширениями .txt, .rtf, .dat, .inf (случайно)
            var rnd = new Random();
            var exts = new[] { ".txt", ".rtf", ".dat", ".inf" };
            Console.WriteLine("\nГенерируем 10 случайных файлов:");
            for (int i = 0; i < 10; i++)
            {
                // генерируем случайное имя и выбираем случайное расширение
                string name = Path.GetRandomFileName(); // возвращает что-то вроде "v5yz3.tmp"
                string ext = exts[rnd.Next(exts.Length)];
                string fileName = Path.ChangeExtension(name, ext);
                string fullPath = Path.Combine(baseFolder, fileName);

                // создаём пустой файл
                using (File.Create(fullPath)) { } // сразу закрываем
                Console.WriteLine($"  Создан файл: {fileName}");
            }

            // 3) Прочитать содержимое папки и вывести список файлов
            Console.WriteLine("\nСодержимое каталогa:");
            var filesInFolder = Directory.GetFiles(baseFolder);
            foreach (var f in filesInFolder)
            {
                string fn = Path.GetFileName(f);
                string ext = Path.GetExtension(f);
                Console.WriteLine($"Файл: {fn} имеет расширение {ext}");
            }

            // 4) Создать коллекцию объектов Mammal (5-6 объектов)
            var mammals = new List<Mammal>
            {
                new Mammal("Ленивец", 2, true),
                new Mammal("Тигр", 5, false),
                new Mammal("Кит", 12, false),
                new Mammal("Лиса", 4, true),
                new Mammal("Слон", 25, false)
            };

            Console.WriteLine("\nИсходная коллекция (не записанная):");
            foreach (var m in mammals) Console.WriteLine("  " + m);

            // 5) Записать коллекцию в бинарный файл с помощью FileService
            var fileService = new FileService();
            string dataFile = Path.Combine(baseFolder, "mammals.dat");
            Console.WriteLine($"\nСохраняем коллекцию в файл: {dataFile}");
            fileService.SaveData(mammals, dataFile);
            Console.WriteLine("Сохранение завершено.");

            // 6) Переименовать файл
            string renamedFile = Path.Combine(baseFolder, "mammals_renamed.dat");
            if (File.Exists(renamedFile)) File.Delete(renamedFile); // на всякий случай
            File.Move(dataFile, renamedFile);
            Console.WriteLine($"\nФайл переименован: {Path.GetFileName(dataFile)} -> {Path.GetFileName(renamedFile)}");

            // 7) Создать пустую коллекцию и прочитать из переименованного файла
            var loaded = new List<Mammal>();
            Console.WriteLine("\nЧитаем объекты из переименованного файла (через FileService.ReadFile):");
            foreach (var m in fileService.ReadFile(renamedFile))
            {
                loaded.Add(m);
                Console.WriteLine("  прочитано: " + m);
            }

            // 8) Отсортировать полученную коллекцию с помощью LINQ, используя MyCustomComparer по Name
            Console.WriteLine("\nСортируем считанную коллекцию по Name с использованием MyCustomComparer<Mammal>:");
            var nameComparer = new MyCustomComparer<Mammal>();
            var sortedByName = loaded.OrderBy(x => x, nameComparer).ToList(); // keySelector возвращает сам объект
            Console.WriteLine("Отсортированная коллекция по имени:");
            foreach (var m in sortedByName) Console.WriteLine("  " + m);

            // 9) Отсортировать коллекцию по свойству отличному от Name (например Age)
            // Используем лямбда-выражение для сравнения (через Comparer<T>.Create)
            Console.WriteLine("\nСортируем по возрасту (Age) — используем лямбда для сравнения через Comparer<int>.Create:");
            var ageComparer = Comparer<int>.Create((a, b) => a.CompareTo(b)); // по возрастанию
            var sortedByAge = loaded.OrderBy(m => m.Age, ageComparer).ToList();
            Console.WriteLine("Отсортированная коллекция по возрасту:");
            foreach (var m in sortedByAge) Console.WriteLine("  " + m);

            // 10) Вывод исходной и итоговых коллекций
            Console.WriteLine("\n--- Сводный вывод ---");
            Console.WriteLine("Исходная коллекция (до записи):");
            foreach (var m in mammals) Console.WriteLine("  " + m);

            Console.WriteLine("\nПрочитанная коллекция:");
            foreach (var m in loaded) Console.WriteLine("  " + m);

            Console.WriteLine("\nОтсортировано по Name:");
            foreach (var m in sortedByName) Console.WriteLine("  " + m);

            Console.WriteLine("\nОтсортировано по Age:");
            foreach (var m in sortedByAge) Console.WriteLine("  " + m);

        }
    }
}
