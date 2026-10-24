#include "pch.h"
#include <gtest/gtest.h>
#include <iostream>
#include <clocale> // Для setlocale


// Тесты для функции createFinalArray
TEST(CreateFinalArrayTests, AllEvenDiagonal) {
    ll lines = 3, columns = 3;
    ll** array = new ll * [lines];
    for (ll i = 0; i < lines; i++) {
        array[i] = new ll[columns];
    }

    array[0][0] = 2; array[0][1] = 1; array[0][2] = 3;
    array[1][0] = 4; array[1][1] = 6; array[1][2] = 1;
    array[2][0] = 1; array[2][1] = 2; array[2][2] = 8;

    ll final_array_size;
    ll* final_array = createFinalArray(array, lines, columns, final_array_size);

    EXPECT_EQ(final_array_size, 3);
    EXPECT_EQ(final_array[0], 2);
    EXPECT_EQ(final_array[1], 6);
    EXPECT_EQ(final_array[2], 8);

    // Освобождение памяти
    delete[] final_array;
    for (ll i = 0; i < lines; i++) {
        delete[] array[i];
    }
    delete[] array;
}

TEST(CreateFinalArrayTests, NoEvenDiagonal) {
    ll lines = 3, columns = 3;
    ll** array = new ll * [lines];
    for (ll i = 0; i < lines; i++) {
        array[i] = new ll[columns];
    }

    array[0][0] = 1; array[0][1] = 1; array[0][2] = 3;
    array[1][0] = 3; array[1][1] = 5; array[1][2] = 1;
    array[2][0] = 1; array[2][1] = 1; array[2][2] = 1;

    ll final_array_size;
    ll* final_array = createFinalArray(array, lines, columns, final_array_size);

    EXPECT_EQ(final_array_size, 0); // Ожидаем, что размер финального массива будет 0

    // Освобождение памяти
    delete[] final_array; // Не забудьте освободить память, даже если она нулевая
    for (ll i = 0; i < lines; i++) {
        delete[] array[i];
    }
    delete[] array;
}

TEST(CreateFinalArrayTests, MixedDiagonal) {
    ll lines = 3, columns = 3;
    ll** array = new ll * [lines];
    for (ll i = 0; i < lines; i++) {
        array[i] = new ll[columns];
    }

    array[0][0] = 1; array[0][1] = 2; array[0][2] = 3;
    array[1][0] = 2; array[1][1] = 3; array[1][2] = 4;
    array[2][0] = 5; array[2][1] = 6; array[2][2] = 0;

    ll final_array_size;
    ll* final_array = createFinalArray(array, lines, columns, final_array_size);

    EXPECT_EQ(final_array_size, 1);
    EXPECT_EQ(final_array[0], 0);
   

    // Освобождение памяти
    delete[] final_array;
    for (ll i = 0; i < lines; i++) {
        delete[] array[i];
    }
    delete[] array;
}

// Тесты для функции calculateProduct
TEST(CalculateProductTests, ProductWithZero) {
    ll array[] = { 1, 0, 3, 4 }; // Присутствует 0
    ll size = sizeof(array) / sizeof(array[0]);

    EXPECT_EQ(calculateProduct(array, size), 0); // Ожидаем, что произведение будет 0
}

TEST(CalculateProductTests, ProductWithOne) {
    ll array[] = { 1, 2, 3, 4 }; // Нет 0, все положительные
    ll size = sizeof(array) / sizeof(array[0]);

    EXPECT_EQ(calculateProduct(array, size), 24); // Ожидаем, что произведение будет 24
}

TEST(CalculateProductTests, EmptyArray) {
    ll* array = nullptr; // Пустой массив
    ll size = 0;

    EXPECT_EQ(calculateProduct(array, size), 1); // Ожидаем, что произведение будет 1
}

// Основная функция для запуска тестов
int main(int argc, char** argv) {
    setlocale(LC_ALL, "Russian"); // Устанавливаем локаль на русский
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}