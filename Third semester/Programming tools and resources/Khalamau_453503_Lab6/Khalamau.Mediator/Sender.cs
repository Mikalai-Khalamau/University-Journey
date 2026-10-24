using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using static Khalamau.Mediator.IRequest;

namespace Khalamau.Mediator
{
    // Реализация медиатора
    public class Sender : ISender
    {
        // Сборка для поиска обработчиков
        private readonly Assembly? _assembly;

        // Словарь соответствия типа интерфейса обработчика
        // и типа (класса) реализации интерфейса обработчика
        private readonly Dictionary<Type, Type?> _handlerImplementations = new();

        public Sender(Assembly? assembly = null)
        {
            _assembly = assembly ?? Assembly.GetCallingAssembly();
            RegisterHandlers(_assembly);
        }

        // Запись в словарь всех типов интерфейсов обработчиков
        // и их реализаций, имеющихся в сборке
        // <param name="assembly">Сборка для поиска обработчиков</param>
        private void RegisterHandlers(Assembly assembly)
        {
            // Находим все неабстрактные классы в сборке
            var handlers = assembly.GetTypes()
                .Where(t => t.IsClass && !t.IsAbstract)
                .SelectMany(t => t.GetInterfaces(), (type, interfaceType) => new { type, interfaceType })
                .Where(x => x.interfaceType.IsGenericType &&
                           (x.interfaceType.GetGenericTypeDefinition() == typeof(IRequestHandler<>) ||
                            x.interfaceType.GetGenericTypeDefinition() == typeof(IRequestHandler<,>)))
                .ToList();

            // Заполняем словарь
            foreach (var handler in handlers)
            {
                _handlerImplementations[handler.interfaceType] = handler.type;
            }

            Console.WriteLine($"✓ Зарегистрировано обработчиков: {_handlerImplementations.Count}");
        }

        // Обработка запроса без возврата данных
        public void Send<TRequest>(TRequest request)
            where TRequest : IRequest
        {
            Type handlerType = typeof(IRequestHandler<>).MakeGenericType(request.GetType());

            try
            {
                var handler = CreateHandler(handlerType);
                handler.Handle((dynamic)request);
            }
            catch (Exception e)
            {
                Console.WriteLine($"Ошибка: {e.Message}");
                throw;
            }
        }

        // Обработка запроса с возвратом данных
        public TResponse Send<TResponse>(IRequest<TResponse> request)
        {
            Type handlerType = typeof(IRequestHandler<,>)
                .MakeGenericType(request.GetType(), typeof(TResponse));

            try
            {
                var handler = CreateHandler(handlerType);
                return handler.Handle((dynamic)request);
            }
            catch (Exception e)
            {
                Console.WriteLine($"❌ Ошибка: {e.Message}");
                throw;
            }
        }

        // Получить объект обработчика
        // <param name="handlerType">Искомый тип</param>
        // <returns>Объект обработчика</returns>
        private dynamic CreateHandler(Type handlerType)
        {
            var implementationType = _handlerImplementations[handlerType];

            if (implementationType is not null)
            {
                return Activator.CreateInstance(implementationType)!;
            }

            throw new NotImplementedException($"Обработчик не найден для типа {handlerType.Name}");
        }
    }
}
