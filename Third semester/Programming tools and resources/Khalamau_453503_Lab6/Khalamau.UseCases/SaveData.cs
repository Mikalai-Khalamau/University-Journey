using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using Khalamau.Domain;
using Khalamau.Mediator;

namespace Khalamau.UseCases
{
    // Запрос на сохранение коллекции в файл
    // <param name="Data">Коллекция объектов</param>
    // <param name="FileName">Имя файла</param>
    public sealed record SaveData(IEnumerable<MenuItem> Data, string FileName) : IRequest;

    // Обработчик запроса на сохранение
    public class SaveDataHandler : IRequestHandler<SaveData>
    {
        public void Handle(SaveData request)
        {
            try
            {
                // Настройки сериализации JSON
                var options = new JsonSerializerOptions
                {
                    WriteIndented = true,  // Красивое форматирование
                    PropertyNamingPolicy = JsonNamingPolicy.CamelCase
                };

                // Сериализация в JSON
                string jsonString = JsonSerializer.Serialize(request.Data, options);

                // Запись в файл
                File.WriteAllText(request.FileName, jsonString);

                Console.WriteLine($"Данные сохранены в файл: {request.FileName}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Ошибка сохранения: {ex.Message}");
                throw;
            }
        }
    }
}
