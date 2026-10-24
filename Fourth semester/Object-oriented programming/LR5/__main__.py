from LogisticsFacade import LogisticsFacade
from Export.JSONExport import JSONExport
from Export.CSVExport import CSVExport
from Export.EncryptedExport import EncryptedExport
from Export.CompressedExport import CompressedExport
from Filter.PriceFilter import PriceFilter
from Filter.SpeedFilter import SpeedFilter
from Sort.PriceSort import PriceSort
from Sort.SpeedSort import SpeedSort
from Sort.NameSort import NameSort
from Import.JSONImporter import JSONImporter
from Import.CSVImporter import CSVImporter
from Import.XMLImporter import XMLImporter


def print_options(options: list) -> None:
    if not options:
        print("Нет вариантов для отображения")
        return
    print(f"\n{'№':<3} {'Транспорт':<25} {'Стоимость':<12} {'Время':<10} {'Масса':<10}")
    print(f"{'-'*3} {'-'*25} {'-'*12} {'-'*10} {'-'*10}")
    for i, opt in enumerate(options, 1):
        print(f"{i:<3} {opt['transport']:<25} {opt['cost']:<12.2f} {opt['time']:<10.2f} {opt['mass']:<10.2f}")


def input_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            print("Значение должно быть положительным")
        except ValueError:
            print("Введите корректное число")


def input_positive_int(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Значение должно быть положительным")
        except ValueError:
            print("Введите корректное целое число")


def input_cargo_item() -> dict | None:
    print("\nДоступные типы грузов: electronics, clothes, foods, equipment")
    cargo_type = input("Тип груза (или пустая строка для завершения): ").strip().lower()
    if not cargo_type:
        return None
    quantity = input_positive_int("Количество: ")
    return {"type": cargo_type, "qty": quantity}


def collect_cargo_list() -> list[dict]:
    cargo_list = []
    while True:
        item = input_cargo_item()
        if item is None:
            if cargo_list:
                break
            print("Добавьте хотя бы один груз")
        else:
            cargo_list.append(item)
            print(f"Добавлено: {item['type']} x {item['qty']}")
    return cargo_list


def configure_filters(facade: LogisticsFacade) -> None:
    while True:
        print("\n1. По максимальной цене")
        print("2. По максимальному времени")
        print("3. Закончить настройку фильтров")
        choice = input("Выбор: ").strip()
        if choice == "1":
            max_price = input_positive_float("Максимальная стоимость (руб): ")
            facade.add_filter(PriceFilter(max_price))
            print(f"Фильтр: цена <= {max_price:.2f} руб.")
        elif choice == "2":
            max_time = input_positive_float("Максимальное время (часов): ")
            facade.add_filter(SpeedFilter(max_time))
            print(f"Фильтр: время <= {max_time:.2f} ч.")
        elif choice == "3":
            break
        else:
            print("Неверный выбор")


def configure_sorters(facade: LogisticsFacade) -> None:
    while True:
        print("\n1. По цене")
        print("2. По времени")
        print("3. По названию транспорта")
        print("4. Закончить настройку сортировки")
        choice = input("Выбор: ").strip()
        if choice in ("1", "2", "3"):
            reverse = input("По убыванию? (да/нет, по умолчанию нет): ").strip().lower() == "да"
            if choice == "1":
                facade.add_sorter(PriceSort(reverse=reverse))
                print(f"Сортировка: по цене ({'убывание' if reverse else 'возрастание'})")
            elif choice == "2":
                facade.add_sorter(SpeedSort(reverse=reverse))
                print(f"Сортировка: по времени ({'убывание' if reverse else 'возрастание'})")
            elif choice == "3":
                facade.add_sorter(NameSort(reverse=reverse))
                print(f"Сортировка: по названию ({'убывание' if reverse else 'возрастание'})")
        elif choice == "4":
            break
        else:
            print("Неверный выбор")


def configure_export(facade: LogisticsFacade) -> str | None:
    print("\n1. Не экспортировать")
    print("2. JSON")
    print("3. CSV")
    print("4. JSON + Шифрование (Base64)")
    print("5. JSON + Сжатие (ZIP)")
    print("6. JSON + Шифрование + Сжатие")
    choice = input("Выбор: ").strip()
    if choice == "1":
        return None
    filename = input("Имя файла (без расширения): ").strip()
    if not filename:
        filename = "export_result"
    if choice == "2":
        facade.set_exporter(JSONExport())
        return f"{filename}.json"
    elif choice == "3":
        facade.set_exporter(CSVExport())
        return f"{filename}.csv"
    elif choice == "4":
        facade.set_exporter(EncryptedExport(JSONExport()))
        return f"{filename}.json.enc"
    elif choice == "5":
        facade.set_exporter(CompressedExport(JSONExport()))
        return f"{filename}.zip"
    elif choice == "6":
        encrypted = EncryptedExport(JSONExport())
        facade.set_exporter(CompressedExport(encrypted))
        return f"{filename}.zip"
    else:
        print("Неверный выбор")
        return None


def configure_import(facade: LogisticsFacade) -> dict | None:
    print("\n1. JSON")
    print("2. CSV")
    print("3. XML")
    print("4. Ввести данные вручную")
    choice = input("Выбор: ").strip()
    if choice == "4":
        return None
    file_path = input("Путь к файлу: ").strip()
    if not file_path:
        print("Пустой путь")
        return None
    try:
        if choice == "1":
            facade.set_importer(JSONImporter())
        elif choice == "2":
            facade.set_importer(CSVImporter())
        elif choice == "3":
            facade.set_importer(XMLImporter())
        else:
            print("Неверный выбор")
            return None
        data = facade.import_from_file(file_path)
        print(f"Данные импортированы: {len(data.get('cargo', []))} грузов")
        return data
    except Exception as e:
        print(f"Ошибка импорта: {e}")
        return None


def run_calculation(facade: LogisticsFacade, cargo_list: list, distance: float) -> dict | None:
    try:
        result = facade.process_with_all_options(cargo_list, distance)
        if not result["success"]:
            print(f"Ошибка: {result.get('error', 'Неизвестная ошибка')}")
            return None
        print(f"\nРезультаты для расстояния {distance} км:")
        print(f"   Грузов: {result['cargo_count']}")
        print(f"   Найдено вариантов: {result['options_count']}")
        if result["options"]:
            print_options(result["options"])
        return result
    except Exception as e:
        print(f"Ошибка расчёта: {e}")
        return None


def main_menu() -> str:
    print("\nЛогистическая система")
    print("1. Новый расчёт")
    print("2. Импорт данных из файла")
    print("3. Выход")
    return input("Выбор: ").strip()


def main():
    facade = LogisticsFacade()
    print("\nДобро пожаловать в логистическую систему!")
    print("Доступные грузы: electronics, clothes, foods, equipment")
    print("Доступный транспорт: truck, train, tanker, airplane, helicopter")
    while True:
        choice = main_menu()
        if choice == "1":
            cargo_list = collect_cargo_list()
            distance = input_positive_float("Расстояние до точки назначения (км): ")
            configure_filters(facade)
            configure_sorters(facade)
            result = run_calculation(facade, cargo_list, distance)
            if result:
                export_path = configure_export(facade)
                if export_path:
                    try:
                        facade.export_to_file(result, export_path)
                        print(f"Файл сохранён: {export_path}")
                    except Exception as e:
                        print(f"Ошибка экспорта: {e}")
            facade.clear_filters()
            facade.clear_sorters()
            input("\nНажмите Enter для продолжения...")
        elif choice == "2":
            imported = configure_import(facade)
            if imported and imported.get("cargo"):
                cargo_list = imported["cargo"]
                distance = imported.get("distance", 0)
                if distance <= 0:
                    distance = input_positive_float("Введите расстояние (км): ")
                configure_filters(facade)
                configure_sorters(facade)
                result = run_calculation(facade, cargo_list, distance)
                if result:
                    export_path = configure_export(facade)
                    if export_path:
                        try:
                            facade.export_to_file(result, export_path)
                            print(f"Файл сохранён: {export_path}")
                        except Exception as e:
                            print(f"Ошибка экспорта: {e}")
                facade.clear_filters()
                facade.clear_sorters()
                input("\nНажмите Enter для продолжения...")
        elif choice == "3":
            print("\nДо свидания!")
            break
        else:
            print("Неверный выбор, попробуйте снова")


if __name__ == "__main__":
    main()