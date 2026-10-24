namespace Collections
{
    internal class Tariff
    {

        private double _cost;  
        private string _title; 

        public double Cost
        {
            get => _cost;
            private set  
            {
                if (value < 0)
                {
                    throw new ArgumentOutOfRangeException(nameof(value), "Стоимость не может быть отрицательной");
                }
                _cost = value;
            }
        }
        public string Title
        {
            get => _title;
            set
            {
                while (string.IsNullOrWhiteSpace(value))
                {
                    throw new ArgumentException("Название тарифа не может быть пустым или null", nameof(value));
           
                }
                _title = value;
            }
        }

        public Tariff(double cost, string title)
        {
            Cost = cost;
            Title = title;
        }
    }
}