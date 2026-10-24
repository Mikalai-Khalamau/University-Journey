def solve(n, m, matrix):
    """Решение задачи 24: поиск максимального квадратного блока из 1
    с возвратом координат его границ."""
    if n == 0 or m == 0:
        return None

    # Инициализация матрицы dp
    dp = [[0] * m for _ in range(n)]
    max_side = 0
    best_r, best_c = -1, -1  # координаты нижнего правого угла (0-based)

    for i in range(n):
        for j in range(m):
            if matrix[i][j] == 1:
                if i == 0 or j == 0:
                    dp[i][j] = 1
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

                if dp[i][j] > max_side:
                    max_side = dp[i][j]
                    best_r, best_c = i, j
            else:
                dp[i][j] = 0

    if max_side == 0:
        return None

    # Верхняя левая клетка (0-based)
    top_r = best_r - max_side + 1
    top_c = best_c - max_side + 1

    # Перевод в 1-based
    return (top_r + 1, top_c + 1), (best_r + 1, best_c + 1)


def read_input():
    """Чтение входных данных."""
    import sys
    data = sys.stdin.read().split()
    if not data:
        return 0, 0, []
    n = int(data[0])
    m = int(data[1])
    matrix = []
    idx = 2
    for i in range(n):
        row = [int(data[idx + j]) for j in range(m)]
        matrix.append(row)
        idx += m
    return n, m, matrix


# === Прогон тестов ===
if __name__ == "__main__":
    # Тест 1
    n1, m1 = 4, 5
    matrix1 = [
        [1, 0, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ]
    res1 = solve(n1, m1, matrix1)
    print("Тест 1:", f"{res1[0]} - {res1[1]}" if res1 else "Блок не найден")
    # (2, 2) - (4, 4)

    # Тест 2
    n2, m2 = 3, 3
    matrix2 = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]
    ]
    res2 = solve(n2, m2, matrix2)
    print("Тест 2:", f"{res2[0]} - {res2[1]}" if res2 else "Блок не найден")
    # (1, 1) - (3, 3)

    # Тест 3
    n3, m3 = 2, 3
    matrix3 = [
        [0, 0, 0],
        [0, 0, 0]
    ]
    res3 = solve(n3, m3, matrix3)
    print("Тест 3:", f"{res3[0]} - {res3[1]}" if res3 else "Блок не найден")
    # Блок не найден