using System;
using System.Collections.Generic;
using System.IO;

namespace _453503_Khalamau_Lab4
{
    // Реализация IFileService для чтения и записи объектов Mammal в бинарный файл.
    // Запись и чтение выполняются через BinaryWriter / BinaryReader.
    // ReadFile реализован как именованный итератор (yield return).
    public class FileService : IFileService<Mammal>
    {
        // Сохраняет коллекцию data в бинарный файл с именем fileName.
        // Если файл существует — удаляет его предварительно.
        // Запись выполняется в порядке полей: Name (string), Age (int), IsNocturnal (bool).
        // Обрабатываются исключения, генерируемые BinaryWriter (IOException).
        public void SaveData(IEnumerable<Mammal> data, string fileName)
        {
            try
            {
                // Если файл существует — удаляем (по условию задания)
                if (File.Exists(fileName))
                    File.Delete(fileName);

                // Создаем поток и BinaryWriter; using гарантирует закрытие/удаление ресурса
                using (var fs = new FileStream(fileName, FileMode.CreateNew, FileAccess.Write, FileShare.None))
                using (var bw = new BinaryWriter(fs))
                {
                    foreach (var item in data)
                    {
                        // Запись полей в заранее оговорённом порядке
                        bw.Write(item.Name ?? string.Empty);
                        bw.Write(item.Age);
                        bw.Write(item.IsNocturnal);
                    }
                }
            }
            catch (IOException ioEx) // обработка исключений BinaryWriter/Stream
            {
                Console.WriteLine($"[SaveData] IO error: {ioEx.Message}");
            }
        }

        // Читает объекты Mammal из бинарного файла fileName.
        // Реализован как именованный итератор (yield return).
        // Чтение осуществляется в том же порядке, в котором данные были записаны:
        // Name (string), Age (int), IsNocturnal (bool).
        // При достижении конца файла цикл корректно завершится.
        // Обрабатываются исключения BinaryReader (IOException, EndOfStreamException).
        public IEnumerable<Mammal> ReadFile(string fileName)
{
            if (!File.Exists(fileName))
                yield break;

            // try/finally допустим, catch — нет
            using (var fs = new FileStream(fileName, FileMode.Open, FileAccess.Read, FileShare.Read))
            using (var br = new BinaryReader(fs))
            {
                bool errorOccurred = false;

                while (fs.Position < fs.Length)
                {
                    Mammal? mammal = null;
                    try
                    {
                        string name = br.ReadString();
                        int age = br.ReadInt32();
                        bool nocturnal = br.ReadBoolean();
                        mammal = new Mammal(name, age, nocturnal);
                    }
                    catch (EndOfStreamException)
                    {
                        // Достигнут конец файла — выходим корректно
                        yield break;
                    }
                    catch (IOException ioEx)
                    {
                        Console.WriteLine($"[ReadFile] Ошибка ввода-вывода: {ioEx.Message}");
                        errorOccurred = true;
                    }

                    if (errorOccurred)
                        yield break;

                    if (mammal != null)
                        yield return mammal;
                }
            }
        }

    }
}
