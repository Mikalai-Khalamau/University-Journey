using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Polymorphism
{
    internal class Discount : IPrice
    {
        private decimal _originalPrice;
        private decimal _discount;
        public decimal OriginalPrice
        {
            get { return _originalPrice; }
            set
            {
                if (value < 0)
                    throw new ArgumentException("Цена не может быть отрицательной");
                _originalPrice = value;
            }
        }

        public decimal DiscountPercent
        {
            get { return _discount; }
            set
            {
                if (value < 0 || value > 100)
                    throw new ArgumentException("Скидка должна быть в пределах 0 - 100 ");
                _discount = value;
            }
        }

        public Discount(decimal price, decimal discount)
        {
            OriginalPrice = price;   
            DiscountPercent = discount; 
        }

        decimal IPrice.GetPrice()
        {
            return OriginalPrice * (100 - DiscountPercent) / 100;
        }
    }
}
