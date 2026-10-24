using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using Khalamau.Domain;
using Khalamau.Mediator;
using static Khalamau.Mediator.IRequest;

namespace Khalamau.UseCases
{
    // Запрос на чтение файла
    // <param name="FileName">Имя файла</param>
    public sealed record ReadFile(string FileName) : IRequest<IEnumerable<MenuItem>>;

    // Обработчик запроса чтения файла
    public class ReadFileHandler : IRequestHandler<ReadFile, IEnumerable<MenuItem>>
    {
        public IEnumerable<MenuItem> Handle(ReadFile request)
        {
            try
            {
                // Проверка существования файла
                if (!File.Exists(request.FileName))
                {
                    throw new FileNotFoundException($"Файл {request.FileName} не найден!");
                }

                // Чтение JSON из файла
                string jsonString = File.ReadAllText(request.FileName);

                // Настройки десериализации
                var options = new JsonSerializerOptions
                {
                    PropertyNamingPolicy = JsonNamingPolicy.CamelCase
                };

                // Десериализация
                var menuItems = JsonSerializer.Deserialize<List<MenuItem>>(jsonString, options);

                Console.WriteLine($"Данные прочитаны из файла: {request.FileName}");

                return menuItems ?? new List<MenuItem>();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Ошибка чтения: {ex.Message}");
                throw;
            }
        }
    }
}
