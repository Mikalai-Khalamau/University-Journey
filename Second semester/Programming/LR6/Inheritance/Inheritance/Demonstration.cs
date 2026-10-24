   namespace Inheritance
    {
        internal class Demonstration 
        {
            static void Main()
            {
                Console.WriteLine("=== Демонстрация работы класса Beer ===");
                var beer = new Beer(ibu: 45, strength: 6.5, price: 300,name: "Эль", brand: "Baltika", isCraft: true);
                Console.WriteLine($"Beer создан: {beer.Name}, {beer.Brand}, {beer.Price} руб.,коэффициент горечи: {beer.Ibu} , крепость: {beer.Strength},крафтовое? {beer.IsCraft}");
                Console.WriteLine($"Рейтинг качества: {beer.CalculateQualityRating()}"); //Абстрактный метод

                Console.WriteLine($"Повысим стоимость пива.Стоимость сейчас {beer.Price}"); //Перегруженный метод
                beer.IncreasePrice(100, "повышение спроса", out string increaseDetails);
                Console.WriteLine(increaseDetails);

                Console.WriteLine($"Вызовем родительский метод для умножения,без скрытия.Начальная цена {beer.Price}");
                beer.MultiplyPrice(1.5);
                Console.WriteLine($"Конечная цена {beer.Price}");

                Console.WriteLine("Вызовем скрытый метод");
                beer.MultiplyPrice(2,out string operationDetails);
                Console.WriteLine(operationDetails);

                Console.WriteLine($"Поменяем бренд.Старый бренд {beer.Brand}"); //Метод из родителя 
                beer.ChangeBrand("Zatezky Gus");
                Console.WriteLine($"Новый бренд: {beer.Brand}");

                Console.WriteLine($"Время ферментации: {beer.GetFermentationTime()} дней"); // Собственный метод



                Console.WriteLine("\n=== Демонстрация работы класса Wine ===");
                var wine = new Wine(strength: 14.0, price: 5000,
                                  name: "Полусладкое", brand: "Massandra",
                                  agingYears: 5, berrySize: 9.5);

                Console.WriteLine($"Wine создан: {wine.Name}, {wine.Brand}, {wine.Price} руб.,размер ягод: {wine.BerrySize}, крепость: {wine.Strength}, выдержка {wine.AgingYears} лет");
            
                Console.WriteLine($"Рейтинг качества: {wine.CalculateQualityRating()}");  //Абстрактный метод

            
                Console.WriteLine($"Поменяем бренд.Старый бренд {wine.Brand}"); // Вызов переопределенного виртуального метода
                wine.ChangeBrand("Chardonnet");
                Console.WriteLine($"Новый бренд: {wine.Brand}");

                Console.WriteLine($"Повысим стоимость вина.Стоимость сейчас {wine.Price}"); //Метод из родителя
                beer.IncreasePrice(1000);
                Console.WriteLine($"Стоимость после повышения {wine.Price}");

                Console.WriteLine("Продемонстрируем метод из родителя,который скрывали для пива.Тут возьмем реализацию родителя.");
                Console.WriteLine($"Начальная цена {wine.Price}");
                wine.MultiplyPrice(3);
                Console.WriteLine($"Конечная цена {wine.Price}");

                Console.WriteLine($"Оптимальная выдержка: {wine.CalculateOptimalAging()} лет"); // Уникальный метод Wine

            }
        }
    }
