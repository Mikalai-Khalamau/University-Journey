#include "pch.h"
#include <gtest/gtest.h>
#include <iostream>
#include <clocale> // Для setlocale

// Тест для функции checkCondition (все элементы соответствуют условию)
TEST(CheckConditionTests, AllElementsSatisfy) {
    ll array[] = { 0, 1, 4, 9, 16 }; // 0 <= 1^2, 1 <= 2^2, 4 <= 3^2, 9 <= 4^2, 16 <= 5^2
    ll size = sizeof(array) / sizeof(array[0]);

    EXPECT_TRUE(checkCondition(array, 0, size - 1));
}

// Тест для функции checkCondition (один элемент не соответствует условию)
TEST(CheckConditionTests, OneElementDoesNotSatisfy) {
    ll array[] = { 0, 1, 4, 10, 16 }; // 10 > 4^2
    ll size = sizeof(array) / sizeof(array[0]);

    EXPECT_TRUE(checkCondition(array, 0, size - 1));
}

// Тест для функции checkCondition (нет элементов, соответствующих условию)
TEST(CheckConditionTests, NoElementsSatisfy) {
    ll array[] = { 17, 18, 19, 20 }; // Все элементы больше, чем i^2 для соответствующих i
    ll size = sizeof(array) / sizeof(array[0]);

    EXPECT_FALSE(checkCondition(array, 0, size - 1));
}

// Основная функция для запуска тестов
int main(int argc, char** argv) {
    setlocale(LC_ALL, "Russian"); // Устанавливаем локаль на русский
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}