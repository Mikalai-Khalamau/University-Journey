using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Principal;
using System.Text;
using System.Threading.Tasks;

namespace Polymorphism
{
    internal class NoDiscount : IPrice 
    {
        private decimal _price;

        public decimal Price
        {
            get
            { 
                return _price; 
            }
            set 
            {
                if (value < 0)
                    throw new ArgumentException("Цена не может быть отрицательной");
                _price = value;
            }
        }
        public NoDiscount(decimal price)
        {
            Price = price;
        }

        decimal IPrice.GetPrice()
        {
            return _price;
        }
    }
}
