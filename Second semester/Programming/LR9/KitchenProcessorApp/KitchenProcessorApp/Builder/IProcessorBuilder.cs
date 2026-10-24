using KitchenProcessorApp.Abstract;

namespace KitchenProcessorApp.Builder
{
    public interface IProcessorBuilder
    {
        void SetName(string name);
        void SetFunction(IProcessorFunction function);
        KitchenProcessor Build();
    }
}
