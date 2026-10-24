using System;
using System.Collections.Generic;
using System.Reflection;

namespace _453503_Khalamau_Lab4
{
    // Generic-компаратор, сравнивающий объекты T по строковому свойству "Name".
    // Реализован через reflection, т.к. T задан как произвольный класс предметной области.
    // name="T" Класс предметной области, имеющий свойство Name (string)
    public class MyCustomComparer<T> : IComparer<T> where T : class
    {
        private readonly PropertyInfo? _nameProp;

        public MyCustomComparer()
        {
            _nameProp = typeof(T).GetProperty("Name", BindingFlags.Public | BindingFlags.Instance);
            if (_nameProp == null || _nameProp.PropertyType != typeof(string))
            {
                throw new InvalidOperationException($"Type {typeof(T).Name} does not have a public string Name property.");
            }
        }

        public int Compare(T? x, T? y)
        {
            if (ReferenceEquals(x, y)) return 0;
            if (x is null) return -1;
            if (y is null) return 1;

            string? nx = (string?)_nameProp!.GetValue(x);
            string? ny = (string?)_nameProp!.GetValue(y);

            nx ??= string.Empty;
            ny ??= string.Empty;

            return string.Compare(nx, ny, StringComparison.CurrentCulture);
        }
    }
}
