using SQLite;
using Lab5.Entities;
using Lab5.Services;

namespace Lab5.Services
{
    public class SQLiteService : IDbService
    {
        private SQLiteConnection _db;
        private readonly string _dbPath;

        public SQLiteService()
        {
            _dbPath = Path.Combine(FileSystem.AppDataDirectory, "superheroes.db3");
        }

        public void Init()
        {
            _db = new SQLiteConnection(_dbPath);
            _db.CreateTable<Superhero>();
            _db.CreateTable<Superpower>();

            if (!_db.Table<Superhero>().Any())
            {
                SeedData();
            }
        }

        private void SeedData()
        {
            var spiderman = new Superhero { Name = "Человек-паук", Age = 23, Universe = "Marvel" };
            var ironman = new Superhero { Name = "Железный человек", Age = 48, Universe = "Marvel" };
            var batman = new Superhero { Name = "Бэтмен", Age = 35, Universe = "DC" };

            _db.Insert(spiderman);
            _db.Insert(ironman);
            _db.Insert(batman);

            // Создаем способности для Человека-паука
            _db.Insert(new Superpower { Name = "Паутина", Description = "Стреляет паутиной из запястий", SuperheroId = spiderman.Id });
            _db.Insert(new Superpower { Name = "Паучье чутьё", Description = "Предчувствует опасность", SuperheroId = spiderman.Id });
            _db.Insert(new Superpower { Name = "Сверхсила", Description = "Может поднимать автомобили", SuperheroId = spiderman.Id });
            _db.Insert(new Superpower { Name = "Лазание по стенам", Description = "Прилипает к любым поверхностям", SuperheroId = spiderman.Id });

            // Создаем способности для Железного человека
            _db.Insert(new Superpower { Name = "Бронекостюм", Description = "Высокотехнологичная броня", SuperheroId = ironman.Id });
            _db.Insert(new Superpower { Name = "Полёт", Description = "Реактивные двигатели в ботинках", SuperheroId = ironman.Id });
            _db.Insert(new Superpower { Name = "Репульсоры", Description = "Энергетические лучи из рук", SuperheroId = ironman.Id });
            _db.Insert(new Superpower { Name = "Гениальный интеллект", Description = "Изобретатель и инженер", SuperheroId = ironman.Id });

            // Создаем способности для Бэтмена
            _db.Insert(new Superpower { Name = "Детективные навыки", Description = "Мастер расследований", SuperheroId = batman.Id });
            _db.Insert(new Superpower { Name = "Боевые искусства", Description = "Мастер рукопашного боя", SuperheroId = batman.Id });
            _db.Insert(new Superpower { Name = "Гаджеты", Description = "Различные устройства и оружие", SuperheroId = batman.Id });
            _db.Insert(new Superpower { Name = "Интеллект", Description = "Стратегическое мышление", SuperheroId = batman.Id });
        }

        public IEnumerable<Superhero> GetAllSuperheroes()
        {
            Init();
            return _db.Table<Superhero>().ToList();
        }

        public IEnumerable<Superpower> GetSuperheroPowers(int superheroId)
        {
            Init();
            return _db.Table<Superpower>()
                     .Where(p => p.SuperheroId == superheroId)
                     .ToList();
        }
    }
}