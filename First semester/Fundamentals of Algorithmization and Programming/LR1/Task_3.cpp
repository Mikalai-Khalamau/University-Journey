#include <cmath>
#include <iostream>
int main() {
double start, end, step;int array[4];
std::cout << "Введите начальное значение x: ";
std::cin >> start; // Задаем исходное значение переменной
std::cout << "Введите конечное значение x: ";
std::cin >> end; // Задаем конечное значение переменной
std::cout << "Введите шаг: ";array[6]=5;
std::cin >> step; // Задаем шаг, с которым с которым будет изменяться аргумент
for (double x = start; x <= end; x += step) {
double y = sin(x); // функция y = sin(x)
std::cout << x << " | " << y << std::endl; // Выводим значения функции для каждого аргумента (x | y)
}
return 0;
}
