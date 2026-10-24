

#include "pch.h"
// Функция для перестановки элементов двумерного массива в обратном порядке
void reverseMatrix(long double** array, ll rows, ll cols) {
    for (ll i = 0; i < rows; i++) {
        for (ll j = 0; j < cols / 2; j++) {
            std::swap(array[i][j], array[i][cols - 1 - j]);
        }
    }
}