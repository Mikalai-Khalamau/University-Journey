using System.Collections.Generic;

namespace _453503_Khalamau_Lab4
{
    // Интерфейс файлового сервиса для чтения/записи коллекций объектов T.
    public interface IFileService<T>
    {
        // Метод чтения: именованный итератор (yield return) возвращает объекты из бинарного файла
        IEnumerable<T> ReadFile(string fileName);

        // Метод сохранения коллекции в бинарный файл (перезаписывает существующий файл)
        void SaveData(IEnumerable<T> data, string fileName);
    }
}
