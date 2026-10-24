using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Lab5.Entities;

namespace Lab5.Services
{
    public interface IDbService
    {
        IEnumerable<Superhero> GetAllSuperheroes();
        IEnumerable<Superpower> GetSuperheroPowers(int superheroId);
        public void Init();
    }
}
