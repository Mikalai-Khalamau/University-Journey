using KitchenProcessorApp.Abstract;
using KitchenProcessorApp.Builder;
using KitchenProcessorApp.Functions;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        var processors = new List<KitchenProcessor>();

        var builder1 = new DesktopProcessorBuilder();
        builder1.SetName("Процессор A");
        builder1.SetFunction(new Shredder());
        processors.Add(builder1.Build());

        var builder2 = new HandProcessorBuilder();
        builder2.SetName("Процессор B");
        builder2.SetFunction(new MeatGrinder());
        processors.Add(builder2.Build());

        foreach (var proc in processors)
        {
            proc.GetInfo();
            proc.Process();

            if (proc is IMixer mixer) mixer.Mix();
            if (proc is IBlender blender) blender.Blend();
            if (proc is IDoughKneader kneader) kneader.KneadDough();

            Console.WriteLine();
        }
    }
}
