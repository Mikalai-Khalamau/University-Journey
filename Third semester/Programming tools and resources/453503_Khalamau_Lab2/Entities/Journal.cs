using System;
using System.Collections.Generic;

namespace _453503_Khalamau_Lab2.Entities
{
    public class Journal
    {
        private readonly List<string> entries = new();

        // Метод, который подписывается на события
        public void RecordEvent(object? sender, string info)
        {
            entries.Add($"{DateTime.Now:HH:mm:ss} — {info}");
        }

        public void PrintJournal()
        {
            Console.WriteLine("=== Журнал событий ===");
            foreach (var entry in entries)
                Console.WriteLine(entry);
        }
    }
}
