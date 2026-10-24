//
// pch.cpp
//

#include "pch.h"

// Функция для создания финального массива из четных элементов главной диагонали
ll* createFinalArray(ll** array, ll lines, ll columns, ll& final_array_size) {
    final_array_size = 0;

    // Подсчет размера финального массива
    for (ll i = 0; i < lines && i < columns; i++) {
        if (array[i][i] % 2 == 0) {
            final_array_size++;
        }
    }

    // Создание финального массива
    ll* final_array = new ll[final_array_size];
    ll k = 0;

    // Заполнение финального массива
    for (ll i = 0; i < lines && i < columns; i++) {
        if (array[i][i] % 2 == 0) {
            final_array[k] = array[i][i];
            k++;
        }
    }

    return final_array;
}

// Функция для подсчета произведения элементов массива
ll calculateProduct(const ll* array, ll size) {
    ll product = 1;
    for (ll i = 0; i < size; i++) {
        product *= array[i];
    }
    return product;
}

