using KitchenProcessorApp.Abstract;
using KitchenProcessorApp.Models;

namespace KitchenProcessorApp.Builder
{
    public class HandProcessorBuilder : IProcessorBuilder
    {
        private string name;
        private IProcessorFunction function;

        public void SetName(string name) => this.name = name;
        public void SetFunction(IProcessorFunction function) => this.function = function;
        public KitchenProcessor Build() => new HandProcessor(name, function);
    }
}
