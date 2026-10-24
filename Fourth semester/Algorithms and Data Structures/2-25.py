def solve(A, B, x, y, z):
    """Решение задачи 25: минимальная стоимость преобразования B в A."""
    n = len(A)
    m = len(B)

    # Инициализация таблицы dp
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Базовые случаи
    for i in range(m + 1):
        dp[i][0] = i * x
    for j in range(n + 1):
        dp[0][j] = j * y

    # Заполнение таблицы
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if B[i - 1] == A[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                delete_cost = dp[i - 1][j] + x
                insert_cost = dp[i][j - 1] + y
                replace_cost = dp[i - 1][j - 1] + z
                dp[i][j] = min(delete_cost, insert_cost, replace_cost)

    return dp[m][n]


def solve_with_path(A, B, x, y, z):
    """Решение с восстановлением последовательности операций."""
    n = len(A)
    m = len(B)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i * x
    for j in range(n + 1):
        dp[0][j] = j * y

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if B[i - 1] == A[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                delete_cost = dp[i - 1][j] + x
                insert_cost = dp[i][j - 1] + y
                replace_cost = dp[i - 1][j - 1] + z
                dp[i][j] = min(delete_cost, insert_cost, replace_cost)

    # Восстановление пути
    operations = []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and B[i - 1] == A[j - 1] and dp[i][j] == dp[i - 1][j - 1]:
            operations.append(f"Match '{B[i - 1]}'")
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + z:
            operations.append(f"Replace '{B[i - 1]}' with '{A[j - 1]}' (cost {z})")
            i -= 1
            j -= 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + x:
            operations.append(f"Delete '{B[i - 1]}' (cost {x})")
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + y:
            operations.append(f"Insert '{A[j - 1]}' (cost {y})")
            j -= 1

    operations.reverse()
    return dp[m][n], operations


# === Прогон тестов ===
if __name__ == "__main__":
    # Тест 1
    res1 = solve("abc", "adc", 1, 1, 2)
    print("Тест 1:", res1)  # 2

    # Тест 2
    res2 = solve("citty", "kitten", 1, 1, 2)
    print("Тест 2:", res2)  # 1

    # Тест 3
    res3 = solve("abc", "abcd", 1, 1, 2)
    print("Тест 3:", res3)  # 1

    # Дополнительный тест с восстановлением пути
    cost, ops = solve_with_path("abc", "adc", 1, 1, 2)
    print("\nДополнительный тест:")
    print("Стоимость:", cost)
    print("Операции:")
    for op in ops:
        print(" ", op)