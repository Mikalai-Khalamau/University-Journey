using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml.Linq;

namespace Polymorphism
{
    internal class Tariff
    {
        private IPrice _ip;
        string _name;
        public string Name {
            get 
            { 
                return _name;
            }
            set 
            {
                if (string.IsNullOrWhiteSpace(value))
                    throw new ArgumentException("Название не может быть пустым");
                _name = value; 
            } 
        }
        public decimal Price {
            get
            {
                return _ip.GetPrice();
            }
        }
        public Tariff(string name, decimal price, decimal discount = 0)
        {
            if (price < 0)
                throw new ArgumentException("Цена не может быть отрицательной");
            if (discount == 0)
            {
                _ip = new NoDiscount(price);
            }
            else
            {
                _ip = new Discount(price, discount);
            }

            Name = name;
        }

    }
}
