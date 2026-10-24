def solve_post_office(n, k, coordinates):
    """Решение задачи 37: размещение k почтовых отделений для n деревень."""
    # Сортировка координат
    x = sorted(coordinates)

    # Вычисление таблицы cost[i][j] - стоимость обслуживания деревень i..j одним отделением
    cost = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            # Медиана отрезка [i, j]
            median_idx = (i + j) // 2
            median = x[median_idx]
            # Сумма расстояний до медианы
            total_cost = sum(abs(x[idx] - median) for idx in range(i, j + 1))
            cost[i][j] = total_cost

    # Таблица динамического программирования
    # dp[k][i] - минимальная стоимость обслуживания первых i деревень k отделениями
    INF = float('inf')
    dp = [[INF] * (n + 1) for _ in range(k + 1)]
    parent = [[0] * (n + 1) for _ in range(k + 1)]

    # Базовый случай: k=1
    for i in range(1, n + 1):
        dp[1][i] = cost[0][i - 1]
        parent[1][i] = 0

    # Заполнение таблицы
    for k_count in range(2, k + 1):
        for i in range(k_count, n + 1):
            for j in range(k_count - 1, i):
                current_cost = dp[k_count - 1][j] + cost[j][i - 1]
                if current_cost < dp[k_count][i]:
                    dp[k_count][i] = current_cost
                    parent[k_count][i] = j

    # Восстановление ответа
    min_cost = dp[k][n]
    post_offices = []
    current_i = n
    current_k = k

    while current_k > 0:
        j = parent[current_k][current_i]
        # Почтовое отделение обслуживает деревни j..current_i-1
        # Его координата - медиана этого отрезка
        median_idx = (j + current_i - 1) // 2
        post_offices.append(x[median_idx])
        current_i = j
        current_k -= 1

    post_offices.reverse()

    return min_cost, post_offices


# === Прогон тестов ===
if __name__ == "__main__":
    # Тест 1
    n1, k1 = 10, 3
    coords1 = [1, 2, 3, 6, 7, 9, 11, 22, 44, 50]
    cost1, offices1 = solve_post_office(n1, k1, coords1)
    print("Тест 1:")
    print(f"  Минимальная стоимость: {cost1}")
    print(f"  Координаты почтовых отделений: {offices1}")
    # Ожидаемый результат: 27, [6, 22, 44]

    # Тест 2
    n2, k2 = 8, 2
    coords2 = [1, 5, 10, 12, 15, 20, 25, 30]
    cost2, offices2 = solve_post_office(n2, k2, coords2)
    print("\nТест 2:")
    print(f"  Минимальная стоимость: {cost2}")
    print(f"  Координаты почтовых отделений: {offices2}")
    # Ожидаемый результат: 31, [10, 25]