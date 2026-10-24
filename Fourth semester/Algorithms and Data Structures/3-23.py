from collections import deque


def solve_castle(n, m, grid):
    """Решение задачи 23: анализ замка."""
    # Идентификаторы комнат
    room_id = [[-1] * n for _ in range(m)]
    room_area = []
    current_room = 0

    # Поиск комнат с помощью BFS
    for r in range(m):
        for c in range(n):
            if room_id[r][c] == -1:
                queue = deque([(r, c)])
                room_id[r][c] = current_room
                area = 0
                while queue:
                    cr, cc = queue.popleft()
                    area += 1
                    p = grid[cr][cc]
                    # Запад (бит 1)
                    if not (p & 1) and cc > 0 and room_id[cr][cc - 1] == -1:
                        room_id[cr][cc - 1] = current_room
                        queue.append((cr, cc - 1))
                    # Север (бит 2)
                    if not (p & 2) and cr > 0 and room_id[cr - 1][cc] == -1:
                        room_id[cr - 1][cc] = current_room
                        queue.append((cr - 1, cc))
                    # Восток (бит 4)
                    if not (p & 4) and cc < n - 1 and room_id[cr][cc + 1] == -1:
                        room_id[cr][cc + 1] = current_room
                        queue.append((cr, cc + 1))
                    # Юг (бит 8)
                    if not (p & 8) and cr < m - 1 and room_id[cr + 1][cc] == -1:
                        room_id[cr + 1][cc] = current_room
                        queue.append((cr + 1, cc))
                room_area.append(area)
                current_room += 1

    num_rooms = current_room
    max_room_area = max(room_area) if room_area else 0

    # Поиск стены для разрушения
    best_area = 0
    best_wall = None

    # Перебор: столбцы слева направо, строки снизу вверх
    for c in range(n):
        for r in range(m - 1, -1, -1):
            p = grid[r][c]
            # Западная стена
            if (p & 1) and c > 0:
                room1 = room_id[r][c]
                room2 = room_id[r][c - 1]
                if room1 != room2:
                    new_area = room_area[room1] + room_area[room2]
                    if new_area > best_area:
                        best_area = new_area
                        best_wall = (r, c, 'west')
            # Северная стена
            if (p & 2) and r > 0:
                room1 = room_id[r][c]
                room2 = room_id[r - 1][c]
                if room1 != room2:
                    new_area = room_area[room1] + room_area[room2]
                    if new_area > best_area:
                        best_area = new_area
                        best_wall = (r, c, 'north')

    return num_rooms, max_room_area, best_area, best_wall


# === Прогон тестов ===
if __name__ == "__main__":
    # Тест 1
    n1, m1 = 3, 3
    grid1 = [
        [11, 14, 11],
        [7, 7, 11],
        [1, 4, 3]
    ]
    res1 = solve_castle(n1, m1, grid1)
    print("Тест 1:")
    print(f"  Количество комнат: {res1[0]}")
    print(f"  Площадь наибольшей комнаты: {res1[1]}")
    print(f"  Максимальная площадь после разрушения: {res1[2]}")
    if res1[3]:
        r, c, direction = res1[3]
        print(f"  Разрушить стену: строка {r + 1}, столбец {c + 1}, направление {direction}")

    # Тест 2
    n2, m2 = 2, 2
    grid2 = [
        [11, 6],
        [7, 5]
    ]
    res2 = solve_castle(n2, m2, grid2)
    print("\nТест 2:")
    print(f"  Количество комнат: {res2[0]}")
    print(f"  Площадь наибольшей комнаты: {res2[1]}")
    print(f"  Максимальная площадь после разрушения: {res2[2]}")
    if res2[3]:
        r, c, direction = res2[3]
        print(f"  Разрушить стену: строка {r + 1}, столбец {c + 1}, направление {direction}")