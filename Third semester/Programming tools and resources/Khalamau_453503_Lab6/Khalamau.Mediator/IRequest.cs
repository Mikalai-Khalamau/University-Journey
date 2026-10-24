using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Khalamau.Mediator
{
    public interface IRequest
    {
        /// <summary>
        /// Запрос, не возвращающий данные
        /// </summary>
        public interface IRequest { }
        /// <summary>
        /// Запрос, возвращающий данные
        /// </summary>
        /// <typeparam name="TResponse">Тип возвращаемых данных</typeparam>
        public interface IRequest<out TResponse> { }
    }
}
