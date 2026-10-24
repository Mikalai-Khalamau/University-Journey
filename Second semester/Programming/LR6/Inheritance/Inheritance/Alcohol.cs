namespace Inheritance
{
    public abstract class Alcohol
    {
        // Поля с protected доступом (видны наследникам)
        protected double _strength;
        protected double _price;
        protected string _name;

        // Публичные свойства для контролируемого доступа
        public string Brand 
        {
            get;
            set;
        }
        public double Strength
        {
            get;
            set;
        }

        public string Name
        {
            get;
            set;
        }

        public double Price
        {
            get;
            set;
        }

        //Конструктор родительского класса 
        public Alcohol(double strength,double price, string name,string brand) 
        {
            Strength = strength;
            Price = price; 
            Name = name;
            Brand = brand;
        }

        //Перегрузим в Beer и оставим в Wine
        public void IncreasePrice(double amount)
        {
            Price+=amount;
        }

        //Виртуальный метод, который переопределим в Wine и оставим в Beer
        public virtual void ChangeBrand(string newBrand)
        {
            Brand = newBrand;
        }

        //Абстрактный метод, которые реализуем в наследниках по отдельности
        public abstract double CalculateQualityRating();

        //Метод, с помощью которого продемонстрируем скрытие
        public void MultiplyPrice(double multiplier)
        {
            Price *= multiplier;
        }
    }
}
