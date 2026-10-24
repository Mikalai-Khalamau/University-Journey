#include "pch.h"
#include <gtest/gtest.h>
#include <iostream>
#include <clocale> // Для setlocale
#include <iomanip>  // Для std::setprecision


// Тесты для функции reverseMatrix
TEST(MatrixTests, ReverseEvenColumns) {
    ll rows = 2, cols = 4;
    long double** array = new long double* [rows];
    for (ll i = 0; i < rows; i++) {
        array[i] = new long double[cols];
    }

    // Инициализация массива
    array[0][0] = 1.0; array[0][1] = 2.0; array[0][2] = 3.0; array[0][3] = 4.0;
    array[1][0] = 5.0; array[1][1] = 6.0; array[1][2] = 7.0; array[1][3] = 8.0;

    // Переворот массива
    reverseMatrix(array, rows, cols);

    // Проверка результата
    EXPECT_DOUBLE_EQ(array[0][0], 4.0);
    EXPECT_DOUBLE_EQ(array[0][1], 3.0);
    EXPECT_DOUBLE_EQ(array[0][2], 2.0);
    EXPECT_DOUBLE_EQ(array[0][3], 1.0);
    EXPECT_DOUBLE_EQ(array[1][0], 8.0);
    EXPECT_DOUBLE_EQ(array[1][1], 7.0);
    EXPECT_DOUBLE_EQ(array[1][2], 6.0);
    EXPECT_DOUBLE_EQ(array[1][3], 5.0);

    // Освобождение памяти
    for (ll i = 0; i < rows; i++) {
        delete[] array[i];
    }
    delete[] array;
}

TEST(MatrixTests, ReverseOddColumns) {
    ll rows = 2, cols = 3;
    long double** array = new long double* [rows];
    for (ll i = 0; i < rows; i++) {
        array[i] = new long double[cols];
    }

    // Инициализация массива
    array[0][0] = 1.0; array[0][1] = 2.0; array[0][2] = 3.0;
    array[1][0] = 4.0; array[1][1] = 5.0; array[1][2] = 6.0;

    // Переворот массива
    reverseMatrix(array, rows, cols);

    // Проверка результата
    EXPECT_DOUBLE_EQ(array[0][0], 3.0);
    EXPECT_DOUBLE_EQ(array[0][1], 2.0);
    EXPECT_DOUBLE_EQ(array[0][2], 1.0);
    EXPECT_DOUBLE_EQ(array[1][0], 6.0);
    EXPECT_DOUBLE_EQ(array[1][1], 5.0);
    EXPECT_DOUBLE_EQ(array[1][2], 4.0);

    // Освобождение памяти
    for (ll i = 0; i < rows; i++) {
        delete[] array[i];
    }
    delete[] array;
}

TEST(MatrixTests, ReverseSingleRow) {
    ll rows = 1, cols = 5;
    long double** array = new long double* [rows];
    for (ll i = 0; i < rows; i++) {
        array[i] = new long double[cols];
    }

    // Инициализация массива
    array[0][0] = 10.0; array[0][1] = 20.0; array[0][2] = 30.0; array[0][3] = 40.0; array[0][4] = 50.0;

    // Переворот массива
    reverseMatrix(array, rows, cols);

    // Проверка результата
    EXPECT_DOUBLE_EQ(array[0][0], 50.0);
    EXPECT_DOUBLE_EQ(array[0][1], 40.0);
    EXPECT_DOUBLE_EQ(array[0][2], 30.0);
    EXPECT_DOUBLE_EQ(array[0][3], 20.0);
    EXPECT_DOUBLE_EQ(array[0][4], 10.0);

    // Освобождение памяти
    for (ll i = 0; i < rows; i++) {
        delete[] array[i];
    }
    delete[] array;
}

// Основная функция для запуска тестов
int main(int argc, char** argv) {
    setlocale(LC_ALL, "Russian"); // Устанавливаем локаль на русский
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}