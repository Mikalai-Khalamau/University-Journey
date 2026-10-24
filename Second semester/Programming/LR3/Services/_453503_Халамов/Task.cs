using System;

namespace _453503_Халамов.Services
{
    internal class Task
    {
        public static void MainTask()
        {
            Display.ConsoleMenu();

            double k = Input.GetNumber("k");
            double z = Input.GetNumber("z");

            Method.Function(k, z);
        }
    }
}
