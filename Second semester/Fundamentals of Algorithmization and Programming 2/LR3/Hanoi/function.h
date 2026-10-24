#include <QPair>
#include <QString>
#include <QVector>
#ifndef FUNCTION_H
#define FUNCTION_H

class Function {
public:
    Function();
    QVector<QPair<int, int>> Hanoi(int rings, int from, int to);
};

#endif	// FUNCTION_H
