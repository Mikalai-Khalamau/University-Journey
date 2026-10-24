using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using SQLite;

namespace Lab5.Entities
{
    [Table("Superheroes")]
    public class Superhero
    {
        [PrimaryKey, AutoIncrement, Indexed]
        public int Id { get; set; }

        public string Name { get; set; } = string.Empty;

        public int Age { get; set; } = 0;

        public string Universe { get; set; } = string.Empty;
    }
}
