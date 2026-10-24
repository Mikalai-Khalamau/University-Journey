from collections import deque


def solve(n):
    """Решение задачи 7: определение начального расположения карточек."""
    if n == 0:
        return []

    # Очередь индексов начальной стопки
    queue = deque(range(n))

    # table_order[p] = индекс в начальной стопке, попавший на позицию p на столе
    table_order = []

    while queue:
        # Берём верхнюю карточку — на стол
        table_order.append(queue.popleft())
        # Если остались карточки, следующую — под низ
        if queue:
            queue.append(queue.popleft())

    # Формируем результат: на позиции p на столе должен быть цвет p % 2
    result = [0] * n
    for table_pos, stack_idx in enumerate(table_order):
        result[stack_idx] = table_pos % 2

    return result


# === Прогон тестов ===
if __name__ == "__main__":
    # Тест 1
    res1 = solve(4)
    print("Тест 1 (n=4):", res1)  # [0, 0, 1, 1]

    # Тест 2
    res2 = solve(6)
    print("Тест 2 (n=6):", res2)  # [0, 1, 1, 1, 0, 0]

    # Тест 3: одна карточка
    res3 = solve(1)
    print("Тест 3 (n=1):", res3)  # [0]

    # Тест 4: проверка корректности для n=10
    res4 = solve(10)
    print("Тест 4 (n=10):", res4)

    # Универсальная проверка: симуляция раскладывания
    def verify(n, initial):
        stack = deque(initial)
        table = []
        while stack:
            table.append(stack.popleft())
            if stack:
                stack.append(stack.popleft())
        expected = [i % 2 for i in range(n)]
        return table == expected

    print("\nПроверка:")
    print("  n=4:", verify(4, solve(4)))    # True
    print("  n=6:", verify(6, solve(6)))    # True
    print("  n=10:", verify(10, solve(10))) # True