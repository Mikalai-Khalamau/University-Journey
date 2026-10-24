namespace Inheritance
{
    internal class Beer : Alcohol
    {
        // Горечь пива
        public double Ibu
        {
            get;
            set;
        }
    public bool IsCraft
        {
            get;
            set;
        }
        public Beer(double ibu,double strength, double price, string name,string brand,bool isCraft) : base(strength, price, name,brand)
        {
            Ibu = ibu;
            IsCraft = isCraft;
        }

        // Перегрузка метода IncreasePrice
        public void IncreasePrice(double amount, string reason, out string operationDetails)
        {
            base.IncreasePrice(amount);
            operationDetails = $"Перегрузка метода.Цена увеличена на {amount} по причине: {reason}";
        }

        // Скрытие метода MultiplyPrice
        public new void MultiplyPrice(double multiplier,out string operationDetails)
        {
            double oldPrice = Price;
            base.MultiplyPrice(multiplier); // Вызов родительского метода
             operationDetails = $"Цена изменена: {oldPrice} -> {Price} (x{multiplier})";
        }

        public override double CalculateQualityRating()
        {
            // Формула: базовая оценка + бонусы за крафт и горечь
            double baseRating = 3.0 + (Strength / 10); // 3-6 баллов за крепость
            double craftBonus = IsCraft ? 2.5 : 0;
            double ibuBonus = Math.Min(Ibu / 20, 3); // + до 3 баллов за горечь
            return Math.Round(baseRating + craftBonus + ibuBonus, 1);
        }

        // Расчёт времени ферментации
        public int GetFermentationTime() => IsCraft ? 14 : 7; // недели
    }
}
