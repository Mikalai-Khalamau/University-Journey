namespace Inheritance
{
    //Класс, закрытый для наследования
    sealed class Wine : Alcohol
    {
        private double berrySize;
        public double BerrySize
        {
            get;
            set;
        }
        public int AgingYears
        {
            get;
            set;
        }
        public Wine(double strength, double price, string name,string brand,int agingYears,double berrySize) : base(strength, price, name,brand)
        {
            AgingYears=agingYears;
            this.berrySize=berrySize;
        }

        public override void ChangeBrand(string newBrand)
        {
            Brand="Premium "+ newBrand;
        }

        public override double CalculateQualityRating()
        {
            // Базовый рейтинг (крепость и выдержка)
            double baseRating = 4.0 + (Strength / 20) + Math.Min(AgingYears * 0.3, 4);

            // Влияние размера ягод:
            // - Мелкие ягоды (8-10мм) = +2 балла (более концентрированный сок)
            // - Средние (10-12мм) = +1 балл
            // - Крупные (12-15мм) = -0.5 балла (разбавленный вкус)
            double berryImpact = berrySize switch
            {
                < 10 => 2.0,
                < 12 => 1.0,
                _ => -0.5
            };

            // Дополнительный бонус для идеального сочетания:
            // Мелкие ягоды + высокая крепость = +1.5
            if (berrySize < 10 && Strength > 13.5)
                berryImpact += 1.5;

            return Math.Round(baseRating + berryImpact, 1);
        }

        // Рассчитывает оптимальный срок выдержки
        public int CalculateOptimalAging()
            => (int)(AgingYears * 1.5); // Например, для молодого вина
    }
}
