namespace KitchenProcessorApp.Abstract
{
    public abstract class KitchenProcessor
    {
        public string Name { get; set; }
        public string Type { get; set; }
        protected IProcessorFunction processorFunction;

        protected KitchenProcessor(string name, string type, IProcessorFunction function)
        {
            Name = name;
            Type = type;
            processorFunction = function;
        }

        public abstract void GetInfo();

        public void Process() => processorFunction.Process(Name);
    }
}
