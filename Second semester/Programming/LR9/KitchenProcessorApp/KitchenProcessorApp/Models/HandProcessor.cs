using KitchenProcessorApp.Abstract;

namespace KitchenProcessorApp.Models
{
    public class HandProcessor : KitchenProcessor, IDoughKneader
    {
        public HandProcessor(string name, IProcessorFunction function)
            : base(name, "Ручной", function) { }

        public override void GetInfo() =>
            Console.WriteLine($"[{Name}] Тип: {Type}, Поддерживает тестомешалку");

        public void KneadDough() => Console.WriteLine($"{Name} замешивает тесто.");
    }
}
