#include "pch.h"
#include <gtest/gtest.h>
#include <iostream>
#include <clocale> // Для setlocale

// Тест для функции fillMatrixA (3x3 матрица)
TEST(MatrixTests, FillMatrixA_3x3) {
    long long N = 3;
    long double** b = new long double* [N];
    long double** c = new long double* [N];
    long double** a = new long double* [N];

    for (long long i = 0; i < N; i++) {
        b[i] = new long double[N];
        c[i] = new long double[N];
        a[i] = new long double[N]; // Матрица a, которую будем заполнять
    }

    // Инициализация матриц b и c
    b[0][0] = 1.0; b[0][1] = -1.0; b[0][2] = 3.0;
    b[1][0] = -4.0; b[1][1] = 5.0; b[1][2] = -6.0;
    b[2][0] = 0.0; b[2][1] = -4.0; b[2][2] = 22.0;

    c[0][0] = -5.0; c[0][1] = 2.0; c[0][2] = -3.0;
    c[1][0] = 4.0; c[1][1] = -5.0; c[1][2] = 6.0;
    c[2][0] = 0.0; c[2][1] = 8.0; c[2][2] = -9.0;

    // Ожидаемый результат для матрицы a
    long double expectedA[3][3] = {
        {-5.0, 2.0, -3.0},
        {4.0, -5.0, 6.0},
        {0.0, 8.0, 22.0}
    };

    // Вызов функции
    fillMatrixA(a, b, c, N);

    // Проверка результатов
    for (long long i = 0; i < N; i++) {
        for (long long j = 0; j < N; j++) {
            EXPECT_DOUBLE_EQ(a[i][j], expectedA[i][j]) << "Ошибка: элемент a[" << i << "][" << j << "] не совпадает.";
        }
    }

    // Освобождение памяти
    for (long long i = 0; i < N; i++) {
        delete[] b[i];
        delete[] c[i];
        delete[] a[i];
    }
    delete[] b;
    delete[] c;
    delete[] a;
}

// Тест для функции fillMatrixA (2x2 матрица)
TEST(MatrixTests, FillMatrixA_2x2) {
    long long N = 2;
    long double** b = new long double* [N];
    long double** c = new long double* [N];
    long double** a = new long double* [N];

    for (long long i = 0; i < N; i++) {
        b[i] = new long double[N];
        c[i] = new long double[N];
        a[i] = new long double[N]; // Матрица a, которую будем заполнять
    }

    // Инициализация матриц b и c
    b[0][0] = 1.0; b[0][1] = -3.0;
    b[1][0] = 4.0; b[1][1] = 5.0;

    c[0][0] = -2.0; c[0][1] = 6.0;
    c[1][0] = 3.0; c[1][1] = -1.0;

    // Ожидаемый результат для матрицы a
    long double expectedA[2][2] = {
        {-2.0, 6.0},
        {4.0, 5.0}
    };

    // Вызов функции
    fillMatrixA(a, b, c, N);

    // Проверка результатов
    for (long long i = 0; i < N; i++) {
        for (long long j = 0; j < N; j++) {
            EXPECT_DOUBLE_EQ(a[i][j], expectedA[i][j]) << "Ошибка: элемент a[" << i << "][" << j << "] не совпадает.";
        }
    }

    // Освобождение памяти
    for (long long i = 0; i < N; i++) {
        delete[] b[i];
        delete[] c[i];
        delete[] a[i];
    }
    delete[] b;
    delete[] c;
    delete[] a;
}

// Тест для функции fillMatrixA (1x1 матрица)
TEST(MatrixTests, FillMatrixA_1x1) {
    long long N = 1;
    long double** b = new long double* [N];
    long double** c = new long double* [N];
    long double** a = new long double* [N];

    for (long long i = 0; i < N; i++) {
        b[i] = new long double[N];
        c[i] = new long double[N];
        a[i] = new long double[N]; // Матрица a, которую будем заполнять
    }

    // Инициализация матриц b и c
    b[0][0] = 42.0;
    c[0][0] = -10.0;

    // Ожидаемый результат для матрицы a
    long double expectedA[1][1] = {
        {42.0}
    };

    // Вызов функции
    fillMatrixA(a, b, c, N);

    // Проверка результатов
    for (long long i = 0; i < N; i++) {
        for (long long j = 0; j < N; j++) {
            EXPECT_DOUBLE_EQ(a[i][j], expectedA[i][j]) << "Ошибка: элемент a[" << i << "][" << j << "] не совпадает.";
        }
    }

    // Освобождение памяти
    for (long long i = 0; i < N; i++) {
        delete[] b[i];
        delete[] c[i];
        delete[] a[i];
    }
    delete[] b;
    delete[] c;
    delete[] a;
}

// Основная функция для запуска тестов
int main(int argc, char** argv) {
    setlocale(LC_ALL, "Russian"); // Устанавливаем локаль на русский
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}