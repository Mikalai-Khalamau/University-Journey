from Controller import LogisticsController
from Factory import MyLogisticsFactory


def main():
    factory = MyLogisticsFactory()
    controller = LogisticsController(factory)

    print("\nСценарий 1: Доставка грузовиком (1000 км)")
    cargo_list_1 = [
        {"type": "electronics", "qty": 10},
        {"type": "clothes", "qty": 50}
    ]
    result_1 = controller.process_request(cargo_list_1, 1000, "truck")

    if result_1["success"]:
        print(f"Транспорт: {result_1['transport']}")
        print(f"Расстояние: {result_1['distance']} км")
        print(f"Общая масса: {result_1['total_mass']:.2f} кг")
        print(f"Стоимость: {result_1['total_cost']:.2f} руб.")
        print(f"Время в пути: {result_1['time_hours']:.2f} ч.")
    else:
        print(f"Ошибка: {result_1['error']}")

    print("\nСценарий 2: Доставка поездом (2000 км)")
    cargo_list_2 = [
        {"type": "equipment", "qty": 5},
        {"type": "electronics", "qty": 20}
    ]
    result_2 = controller.process_request(cargo_list_2, 2000, "train")

    if result_2["success"]:
        print(f"Транспорт: {result_2['transport']}")
        print(f"Расстояние: {result_2['distance']} км")
        print(f"Общая масса: {result_2['total_mass']:.2f} кг")
        print(f"Стоимость: {result_2['total_cost']:.2f} руб.")
        print(f"Время в пути: {result_2['time_hours']:.2f} ч.")
    else:
        print(f"Ошибка: {result_2['error']}")

    print("\nСценарий 3: Доставка самолетом (3000 км)")
    cargo_list_3 = [
        {"type": "electronics", "qty": 5},
        {"type": "clothes", "qty": 10}
    ]
    result_3 = controller.process_request(cargo_list_3, 3000, "airplane")

    if result_3["success"]:
        print(f"Транспорт: {result_3['transport']}")
        print(f"Расстояние: {result_3['distance']} км")
        print(f"Общая масса: {result_3['total_mass']:.2f} кг")
        print(f"Стоимость: {result_3['total_cost']:.2f} руб.")
        print(f"Время в пути: {result_3['time_hours']:.2f} ч.")
    else:
        print(f"Ошибка: {result_3['error']}")

    print("\nСценарий 4: Доставка танкером (5000 км)")
    cargo_list_4 = [
        {"type": "foods", "qty": 100},
        {"type": "equipment", "qty": 10}
    ]
    result_4 = controller.process_request(cargo_list_4, 5000, "tanker")

    if result_4["success"]:
        print(f"Транспорт: {result_4['transport']}")
        print(f"Расстояние: {result_4['distance']} км")
        print(f"Общая масса: {result_4['total_mass']:.2f} кг")
        print(f"Стоимость: {result_4['total_cost']:.2f} руб.")
        print(f"Время в пути: {result_4['time_hours']:.2f} ч.")
    else:
        print(f"Ошибка: {result_4['error']}")

    print("\nСценарий 5: Обработка ошибки (пустой список грузов)")
    result_5 = controller.process_request([], 100, "truck")

    if result_5["success"]:
        print("Успешно")
    else:
        print(f"Ошибка: {result_5['error']}")

    print("\nСценарий 6: Обработка ошибки (неизвестный транспорт)")
    result_6 = controller.process_request([{"type": "clothes", "qty": 10}], 100, "submarine")

    if result_6["success"]:
        print("Успешно")
    else:
        print(f"Ошибка: {result_6['error']}")

if __name__ == "__main__":
    main()