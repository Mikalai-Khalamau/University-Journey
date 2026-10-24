//
// pch.cpp
//

#include "pch.h"

long double module(long double x) {
    return (x < 0) ? -x : x;
}

// Функция для заполнения матрицы a
void fillMatrixA(long double** a, long double** b, long double** c, ll n) {
    for (ll i = 0; i < n; i++) {
        for (ll j = 0; j < n; j++) {
            a[i][j] = (module(b[i][j]) > module(c[i][j])) ? b[i][j] : c[i][j];
        }
    }
}
