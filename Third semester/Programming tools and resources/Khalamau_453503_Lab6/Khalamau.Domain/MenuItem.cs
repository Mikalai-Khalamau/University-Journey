using System;

namespace Khalamau.Domain
{
    // Класс предметной области: Позиция меню пиццерии
    public class MenuItem : IEquatable<MenuItem>
    {
        public string Name { get; set; } = string.Empty;
        public int Price { get; set; }

        public bool IsAvailable { get; set; }

        // Конструктор без параметров (необходим для сериализации)
        public MenuItem() { }

        // Конструктор с параметрами
        public MenuItem(string name, int price, bool isAvailable)
        {
            Name = name ?? string.Empty;
            Price = price;
            IsAvailable = isAvailable;
        }

        public override string ToString()
        {
            string availability = IsAvailable ? "В наличии" : "Нет в наличии";
            return $"{Name} - {Price}₽ [{availability}]";
        }
        public bool Equals(MenuItem? other)
        {
            if (other == null) return false;

            return Name == other.Name &&
                   Price == other.Price &&
                   IsAvailable == other.IsAvailable;
        }
        public override bool Equals(object? obj)
        {
            return Equals(obj as MenuItem);
        }
        public override int GetHashCode()
        {
            return HashCode.Combine(Name, Price, IsAvailable);
        }
    }
}
