#include "function.h"

const int k6=6;

Function::Function() {}

QVector<QPair<int, int>> Function::Hanoi(int rings, int from, int to) {
    QVector<QPair<int, int>> moves;


    if (rings == 0) {
        return moves;  // Нет колец — нет ходов
    }
    int temp = k6 - from - to;  // Временный стержень (1+2+3=6)

    // Рекурсивно перемещаем n-1 колец на временный стержень
    moves.append(Hanoi(rings - 1, from, temp));

    // Перемещаем последнее кольцо на целевой стержень
    moves.push_back({from, to});

    // Рекурсивно перемещаем n-1 колец обратно на целевой стержень
    moves.append(Hanoi(rings - 1, temp, to));

    return moves;
}
