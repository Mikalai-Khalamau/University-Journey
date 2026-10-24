using System.Collections.Generic;

namespace _453503_Khalamau_Lab3.Entities
{
    public class Resident<T> where T : System.Numerics.INumber<T>
    {
        public string Surname { get; set; }
        public List<Consumption<T>> Consumptions { get; set; } = new();
        public Resident(string surname) { Surname = surname; }
    }
}
