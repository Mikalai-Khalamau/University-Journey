using System.Collections.Generic;

namespace Collections
{
    public enum ResidentType
    {
        Regular,
        WithFamily,
    }

    internal class Resident
    {
        private string _name;
        public string Name {
            get=>_name; 
            private set
            {
                if (string.IsNullOrWhiteSpace(value))
                {
                    throw new ArgumentException("Фамилия не может быть пустой или null", nameof(value));
                }
                _name = value;
            }
        }

        public ResidentType Type {
            get;
            
        }
        public List<Tariff> UsedTariffs { get; } = new List<Tariff>();

        public Resident(string name, ResidentType type)
        {
            Name = name;
            Type = type;
        }
    }
}