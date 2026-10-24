using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using SQLite;

namespace Lab5.Entities
{
    [Table("Superpowers")]
    public class Superpower
    {
        [PrimaryKey, AutoIncrement, Indexed]
        [Column("Id")]
        public int PowerId { get; set; }

        public string Name { get; set; } = string.Empty;

        public string Description { get; set; } = string.Empty;

        [Indexed]
        public int SuperheroId { get; set; }
    }
}
