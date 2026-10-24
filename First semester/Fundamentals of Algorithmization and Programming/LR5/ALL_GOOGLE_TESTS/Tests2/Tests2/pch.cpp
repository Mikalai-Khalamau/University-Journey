#include "pch.h"

// Функция для проверки условия Ai ≤ i^2
bool checkCondition(ll* array, ll start, ll end) {
    if (start == end) {
        return array[start] <= (start + 1) * (start + 1);
    }

    ll mid = (start + end) / 2;

    // Проверяем обе половины
    return checkCondition(array, start, mid) || checkCondition(array, mid + 1, end);
}

// Функция для проверки условия и вывода результата
void checkAndDisplayCondition(ll* array, ll size) {
    if (checkCondition(array, 0, size - 1)) {
        std::cout << "Существует хотя бы один элемент Ai, для которого Ai <= i^2." << '\n';
    }
    else {
        std::cout << "Нет элементов Ai, для которых Ai <= i^2." << '\n';
    }
}
