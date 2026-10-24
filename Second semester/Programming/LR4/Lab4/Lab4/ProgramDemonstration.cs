using System;

namespace Lab4
{
    internal class ProgramDemonstration
    {
        static void InputOfDoubleValue(out double value)
        {
            string? str = null;
            while (true)
            {
                str = Console.ReadLine();
                if (double.TryParse(str, out value) && double.Parse(str) >= 0)
                {
                    value = double.Parse(str);
                    break;
                }
                Console.WriteLine("Введите значение заново: ");
            }
        }

        static void InputOfIntValue(out int value)
        {
            string? str = null;
            while (true)
            {
                str = Console.ReadLine();
                if (int.TryParse(str, out value) && int.Parse(str) >= 0)
                {
                    value = int.Parse(str);
                    break;
                }
                Console.WriteLine("Введите значение заново: ");
            }
        }

        static void Main(string[] args)
        {
            string? district = null, str = null;
            double costOfTariff = 0;
            int numberOfRoomers = 0;
            int numberOfPayers = 0;
            int numberOfService = 0;

            Console.WriteLine("Введите район вашей ЖЭС(любая строка, даже пустая если района нет):");
            district = Console.ReadLine();

            Console.WriteLine("Введите номер вашей ЖЭС:");
            InputOfIntValue(out numberOfService);

            Console.WriteLine("Введите стоимость тарифа:");
            InputOfDoubleValue(out costOfTariff);

            Console.WriteLine("Введите количество жильцов:");
            InputOfIntValue(out numberOfRoomers);

            Console.WriteLine("Введите количество жильцов, оплативших услуги:");
            InputOfIntValue(out numberOfPayers);
            while (numberOfPayers > numberOfRoomers)
            {
                Console.WriteLine("Введите значение еще раз, так как количество оплативших не может быть больше количества жильцов:");
                InputOfIntValue(out numberOfPayers);
            }

            Console.Clear();

            // Инициализация объекта HousingService
            HousingService.Initialize(district, numberOfService, numberOfRoomers, numberOfPayers, costOfTariff);
            HousingService myHousingService = HousingService.GetInstance();

            while (true)
            {
                Console.WriteLine("Выберите действие под цифрой или любой другой ввод для выхода:\n" +
                    "0 - Узнать как расшифровывается аббревиатура ЖЭС\n" +
                     "1 - Узнать информацию о задании\n" +
                     "2 - Узнать район, к которому принадлежит ЖЭС\n" +
                      "3 - Узнать номер ЖЭС\n" +
                    "4 - Узнать стоимость тарифа\n" +
                    "5 - Узнать число жильцов\n" +
                     "6 - Узнать число оплативших тариф жильцов\n" +
                    "7 - Узнать общую задолженность\n" +
                    "8 - Увеличить тариф\n" +
                    "9 - Уменьшить тариф\n");

                str = Console.ReadLine();

                if (str != "0" && str != "1" && str != "2" && str != "3" && str != "4" &&
                    str != "5" && str != "6" && str != "7" && str != "8" && str != "9")
                {
                    Console.WriteLine("Выход из программы...");
                    break;
                }

                switch (int.Parse(str))
                {
                    case 0:
                        {
                            Console.WriteLine("Жилищно-эксплуатационная служба");
                            break;
                        }
                    case 1:
                        {
                            Console.WriteLine("Предметная область: ЖЭС-Тариф. В классе хранить информацию\r\nо районе, к которому принадлежит ЖЭС, номер ЖЭС, число жильцов, оплату\r\nза месяц (одинаковая для всех - класс Тариф), число оплативших. Реализовать\r\nметод для подсчета общей задолженности жильцов. Реализовать возможность\r\nизменения (увеличения и уменьшения) тарифа.\n");
                            Console.WriteLine("Выполнил студент группы 453503 Халамов Николай Андреевич");
                            break;
                        }
                    case 2:
                        {
                            Console.WriteLine("Район, в котором находится ЖЭС: " + myHousingService.District + "\n");
                            break;
                        }
                    case 3:
                        {
                            Console.WriteLine("Номер ЖЭС: " + myHousingService.NumberOfService + "\n");
                            break;
                        }
                    case 4:
                        {
                            Console.WriteLine("Стоимость тарифа: " + myHousingService.tariff.CostOfTariff + "\n");
                            break;
                        }
                    case 5:
                        {
                            Console.WriteLine("Количество жильцов: " + myHousingService.NumberOfRoomers + "\n");
                            break;
                        }
                    case 6:
                        {
                            Console.WriteLine("Количество жильцов, оплативших тариф: " + myHousingService.NumberOfPayers + "\n");
                            break;
                        }
                    case 7:
                        {
                            Console.WriteLine("Общая задолженность жильцов: " + myHousingService.Arrear() + "\n");
                            break;
                        }
                    case 8:
                        {
                            double value = 0;

                            Console.WriteLine("Введите значение, на которое увеличится тариф:");
                            InputOfDoubleValue(out value);

                            myHousingService.IncreaseCost(value);
                            Console.WriteLine("Стоимость тарифа увеличена!");
                            break;
                        }
                    case 9:
                        {

                            double value = 0;
                            Console.WriteLine("Введите значение, на которое уменьшится тариф:");
                            InputOfDoubleValue(out value);

                            // Используем текущее значение тарифа вместо переменной costOfTariff
                            while (myHousingService.tariff.CostOfTariff - value < 0)
                            {
                                Console.WriteLine("Стоимость тарифа должна быть неотрицательным числом. Введите значение еще раз:");
                                InputOfDoubleValue(out value);
                            }

                            myHousingService.DecreaseCost(value);
                            Console.WriteLine("Стоимость тарифа уменьшена!");
                            break;
                        }
                    default:
                        {
                            break;
                        }
                }
            }
        }
    }
}
