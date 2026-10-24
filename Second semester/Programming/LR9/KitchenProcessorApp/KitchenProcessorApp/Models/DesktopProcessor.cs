using KitchenProcessorApp.Abstract;

namespace KitchenProcessorApp.Models
{
    public class DesktopProcessor : KitchenProcessor, IMixer, IBlender
    {
        public DesktopProcessor(string name, IProcessorFunction function)
            : base(name, "Настольный", function) { }

        public override void GetInfo() =>
            Console.WriteLine($"[{Name}] Тип: {Type}, Поддерживает миксер и блендер");

        public void Mix() => Console.WriteLine($"{Name} взбивает тесто.");
        public void Blend() => Console.WriteLine($"{Name} делает смузи.");
    }
}
