using System;

namespace _453503_Khalamau_Lab4
{
    // Сущность "млекопитающее" 
    // Содержит: Name (string), Age (int) и IsNocturnal (bool) — пример булева свойства.
    public class Mammal
    {
        public string Name { get; set; }         // имя (строка)
        public int Age { get; set; }             // целочисленное свойство
        public bool IsNocturnal { get; set; }    // булево свойство

        public Mammal() { }

        public Mammal(string name, int age, bool isNocturnal)
        {
            Name = name ?? throw new ArgumentNullException(nameof(name));
            Age = age;
            IsNocturnal = isNocturnal;
        }

        public override string ToString()
            => $"Name: {Name}, Age: {Age}, IsNocturnal: {IsNocturnal}";
    }
}
