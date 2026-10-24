using System;
using System.Diagnostics;
using System.Threading;

namespace Khalamau_Lab4
{
    public class Sinus
    {
        public double ComputeIntegral(IProgress<double> progress, CancellationToken cancellationToken)
        {
            int threadId = Thread.CurrentThread.ManagedThreadId;
            double h = 0.00000001;
            long totalSteps = (long)(1.0 / h);
            long whenReport = totalSteps / 100; 
            double sum = 0.0;

           

            for (long i = 0; i < totalSteps; i++)
            {
                cancellationToken.ThrowIfCancellationRequested();

                double x = i * h;
                sum += Math.Sin(x + h / 2) * h;

                for (int j = 0; j < 10; j++)
                {
                    double _ = j * j;
                }

                if (i % whenReport == 0)
                {
                    double percent = (double)i / totalSteps;
                    progress.Report(percent);
                }
            }

            progress.Report(1.0);
            return sum;
        }

      
    }
}