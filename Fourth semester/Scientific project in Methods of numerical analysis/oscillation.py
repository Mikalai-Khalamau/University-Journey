#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
УРАВНЕНИЕ С ПОГРАНИЧНЫМ СЛОЕМ
-0.01·U'' + U' = 1, U(0) = U(1) = 0
Метод Малышева (по псевдокоду)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve
import time
import csv
import os


# ============================================================================
# БАЗИСНЫЕ ФУНКЦИИ (Чебышев для пограничного слоя)
# ============================================================================

class Basis:
    @staticmethod
    def chebyshev(x, k):
        """φ_k(x) = x(1-x)·T_k(2x-1)"""
        from scipy.special import chebyt
        T_k = chebyt(k)
        return x * (1 - x) * T_k(2 * x - 1)

    @staticmethod
    def chebyshev_deriv1(x, k, h=1e-7):
        """Первая производная (численно)"""
        return (Basis.chebyshev(x + h, k) - Basis.chebyshev(x - h, k)) / (2 * h)

    @staticmethod
    def chebyshev_deriv2(x, k, h=1e-7):
        """Вторая производная (численно)"""
        return (Basis.chebyshev(x + h, k) - 2 * Basis.chebyshev(x, k) +
                Basis.chebyshev(x - h, k)) / (h ** 2)

    @staticmethod
    def chebyshev_deriv_k(x, k, deriv_order, h=1e-6):
        """Производная порядка deriv_order (численно)"""
        if deriv_order == 0:
            return Basis.chebyshev(x, k)
        elif deriv_order == 1:
            return Basis.chebyshev_deriv1(x, k, h)
        elif deriv_order == 2:
            return Basis.chebyshev_deriv2(x, k, h)
        else:
            # Рекурсивное дифференцирование
            phi = Basis.chebyshev(x, k)
            for _ in range(deriv_order):
                phi = (Basis.chebyshev(x + h, k) - Basis.chebyshev(x - h, k)) / (2 * h)
            return phi


# ============================================================================
# УРАВНЕНИЕ С ПОГРАНИЧНЫМ СЛОЕМ
# ============================================================================

class BoundaryLayerEquation:
    @staticmethod
    def f(x):
        """Правая часть: 1"""
        return np.ones_like(x)

    @staticmethod
    def exact(x):
        """Точное решение: U(x) = x - (e^(100x) - 1)/(e^100 - 1)"""
        return x - (np.exp(100 * x) - 1) / (np.exp(100) - 1)

    @staticmethod
    def operator(U_dd, U_d, U, x):
        """Оператор уравнения: -0.01·U'' + U'"""
        return -0.01 * U_dd + U_d


# ============================================================================
# МЕТОД МАЛЫШЕВА (ПО ПСЕВДОКОДУ)
# ============================================================================

class MalyshevMethod:
    def __init__(self, n_funcs, basis_type='chebyshev'):
        self.n = n_funcs
        self.basis = basis_type
        self.coefficients = None
        self.condition_number = None

    def _build_basis(self, x, k, deriv=0):
        """Получить k-ю базисную функцию с производной порядка deriv"""
        if self.basis == 'chebyshev':
            return Basis.chebyshev_deriv_k(x, k, deriv)
        return np.zeros_like(x)

    def compute_residual(self, x, coefficients):
        """Вычислить невязку R = -0.01·U'' + U' - 1"""
        U_dd = np.zeros_like(x)
        U_d = np.zeros_like(x)

        for k in range(1, self.n + 1):
            U_dd += coefficients[k - 1] * self._build_basis(x, k, deriv=2)
            U_d += coefficients[k - 1] * self._build_basis(x, k, deriv=1)

        R = BoundaryLayerEquation.operator(U_dd, U_d, None, x) - BoundaryLayerEquation.f(x)
        return R

    def solve(self, x):
        """
        Реализация псевдокода Малышева:
        1. ∫R dx = 0
        2. ∫R^(k) dx = 0 → R^(k-1)(1) - R^(k-1)(0) = 0 (Ньютон-Лейбниц)
        """
        start = time.perf_counter()

        # Точки для интегрирования
        x_int = np.linspace(0, 1, 500)
        dx = x_int[1] - x_int[0]

        # Граничные точки
        x_0 = np.array([0.0])
        x_1 = np.array([1.0])

        # Система уравнений
        A = np.zeros((self.n, self.n))
        B = np.zeros(self.n)

        # Условие 1: ∫R dx = 0 (j=1 в псевдокоде)
        for k in range(1, self.n + 1):
            U_dd_k = self._build_basis(x_int, k, deriv=2)
            U_d_k = self._build_basis(x_int, k, deriv=1)
            A[0, k - 1] = np.sum(-0.01 * U_dd_k + U_d_k) * dx
        B[0] = np.sum(BoundaryLayerEquation.f(x_int)) * dx

        # Условия 2..N: ∫R^(k) dx = 0 → R^(k-1)(1) - R^(k-1)(0) = 0
        for j in range(2, self.n + 1):
            k = j - 2  # Порядок производной невязки

            if k == 0:
                # R(1) - R(0) = 0
                # R = -0.01·U'' + U' - f
                for m in range(1, self.n + 1):
                    U_dd_m_0 = self._build_basis(x_0, m, deriv=2)[0]
                    U_dd_m_1 = self._build_basis(x_1, m, deriv=2)[0]
                    U_d_m_0 = self._build_basis(x_0, m, deriv=1)[0]
                    U_d_m_1 = self._build_basis(x_1, m, deriv=1)[0]

                    A[j - 1, m - 1] = (-0.01 * U_dd_m_1 + U_d_m_1) - (-0.01 * U_dd_m_0 + U_d_m_0)

                B[j - 1] = BoundaryLayerEquation.f(x_1)[0] - BoundaryLayerEquation.f(x_0)[0]

            else:
                # R^(k)(1) - R^(k)(0) = 0
                for m in range(1, self.n + 1):
                    # Производные порядка k+1 и k+2 для оператора
                    U_dd_deriv_0 = self._build_basis(x_0, m, deriv=k + 2)
                    U_dd_deriv_1 = self._build_basis(x_1, m, deriv=k + 2)
                    U_d_deriv_0 = self._build_basis(x_0, m, deriv=k + 1)
                    U_d_deriv_1 = self._build_basis(x_1, m, deriv=k + 1)

                    A[j - 1, m - 1] = (-0.01 * U_dd_deriv_1 + U_d_deriv_1) - \
                                      (-0.01 * U_dd_deriv_0 + U_d_deriv_0)

                B[j - 1] = 0.0  # Производные f(x)=1 равны 0

        # Регуляризация для устойчивости
        alpha = 1e-8
        A = A + alpha * np.eye(self.n)

        try:
            self.coefficients = solve(A, B)
            self.condition_number = np.linalg.cond(A)
        except:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        elapsed = (time.perf_counter() - start) * 1000
        return self.coefficients, elapsed

    def get_solution(self, x):
        """Получить приближённое решение"""
        U = np.zeros_like(x)
        for k in range(1, self.n + 1):
            U += self.coefficients[k - 1] * self._build_basis(x, k, deriv=0)
        return U

    def get_residual(self, x):
        """Получить невязку"""
        return self.compute_residual(x, self.coefficients)


# ============================================================================
# МЕТОД ГАЛЕРКИНА (ДЛЯ СРАВНЕНИЯ)
# ============================================================================

class GalerkinMethod:
    def __init__(self, n_funcs, basis_type='chebyshev'):
        self.n = n_funcs
        self.basis = basis_type
        self.coefficients = None
        self.condition_number = None

    def _build_basis(self, x, k, deriv=0):
        if self.basis == 'chebyshev':
            return Basis.chebyshev_deriv_k(x, k, deriv)
        return np.zeros_like(x)

    def solve(self, x):
        """Классический метод Галеркина: ∫R·φ_i dx = 0"""
        start = time.perf_counter()

        x_int = np.linspace(0, 1, 500)
        dx = x_int[1] - x_int[0]

        A = np.zeros((self.n, self.n))
        B = np.zeros(self.n)

        for i in range(1, self.n + 1):
            phi_i = self._build_basis(x_int, i, deriv=0)

            for j in range(1, self.n + 1):
                U_dd_j = self._build_basis(x_int, j, deriv=2)
                U_d_j = self._build_basis(x_int, j, deriv=1)

                integrand = (-0.01 * U_dd_j + U_d_j) * phi_i
                A[i - 1, j - 1] = np.sum(integrand) * dx

            B[i - 1] = np.sum(BoundaryLayerEquation.f(x_int) * phi_i) * dx

        try:
            self.coefficients = solve(A, B)
            self.condition_number = np.linalg.cond(A)
        except:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        elapsed = (time.perf_counter() - start) * 1000
        return self.coefficients, elapsed

    def get_solution(self, x):
        U = np.zeros_like(x)
        for k in range(1, self.n + 1):
            U += self.coefficients[k - 1] * self._build_basis(x, k, deriv=0)
        return U

    def get_residual(self, x):
        U_dd = np.zeros_like(x)
        U_d = np.zeros_like(x)
        for k in range(1, self.n + 1):
            U_dd += self.coefficients[k - 1] * self._build_basis(x, k, deriv=2)
            U_d += self.coefficients[k - 1] * self._build_basis(x, k, deriv=1)
        return -0.01 * U_dd + U_d - BoundaryLayerEquation.f(x)


# ============================================================================
# МЕТРИКИ
# ============================================================================

class Metrics:
    @staticmethod
    def max_error(u_exact, u_approx):
        return np.max(np.abs(u_exact - u_approx))

    @staticmethod
    def rms_error(u_exact, u_approx):
        return np.sqrt(np.mean((u_exact - u_approx) ** 2))

    @staticmethod
    def rms_residual(residual):
        return np.sqrt(np.mean(residual ** 2))


# ============================================================================
# ЭКСПЕРИМЕНТ
# ============================================================================

def run_experiment():
    print("=" * 80)
    print("УРАВНЕНИЕ С ПОГРАНИЧНЫМ СЛОЕМ")
    print("Уравнение: -0.01·U'' + U' = 1, U(0) = U(1) = 0")
    print("Базис: Полиномы Чебышева")
    print("=" * 80)

    x = np.linspace(0, 1, 500)
    u_exact = BoundaryLayerEquation.exact(x)

    n_values = [5, 7, 10, 15]
    methods = [
        ('galerkin', 'Галеркин', GalerkinMethod),
        ('malyshev', 'Малышев', MalyshevMethod)
    ]

    results = {n: {} for n in n_values}

    print("\n" + "=" * 80)
    print("СХОДИМОСТЬ ПО N")
    print("=" * 80)

    for n in n_values:
        print(f"\nN = {n}:")
        results[n] = {}

        for method_key, method_name, method_class in methods:
            print(f"  [{method_name}]...")

            solver = method_class(n_funcs=n, basis_type='chebyshev')
            coefficients, time_ms = solver.solve(x)
            u_approx = solver.get_solution(x)
            residual = solver.get_residual(x)

            max_err = Metrics.max_error(u_exact, u_approx)
            rms_err = Metrics.rms_error(u_exact, u_approx)
            rms_res = Metrics.rms_residual(residual)

            results[n][method_key] = {
                'max_error': max_err,
                'rms_error': rms_err,
                'rms_residual': rms_res,
                'time_ms': time_ms,
                'cond': solver.condition_number,
                'u_approx': u_approx,
                'residual': residual
            }

            print(f"    Max ошибка: {max_err:.2e}")
            print(f"    RMS ошибка: {rms_err:.2e}")
            print(f"    RMS невязка: {rms_res:.2e}")
            print(f"    Время: {time_ms:.2f} мс")
            print(f"    cond(A): {solver.condition_number:.2e}")

    # Сохранение результатов
    os.makedirs('results', exist_ok=True)

    with open('results/boundary_layer_convergence.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['N', 'Метод', 'Max Error', 'RMS Error', 'RMS Residual', 'Time (ms)', 'cond(A)'])
        for n in n_values:
            for method_key, method_name, _ in methods:
                r = results[n][method_key]
                w.writerow([n, method_name, f"{r['max_error']:.6e}",
                            f"{r['rms_error']:.6e}", f"{r['rms_residual']:.6e}",
                            f"{r['time_ms']:.4f}", f"{r['cond']:.4e}"])

    # Графики
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Сравнение решений (N=10)
    ax = axes[0, 0]
    n_plot = 10
    ax.plot(x, u_exact, 'k--', linewidth=2, label='Точное')
    for method_key, method_name, _ in methods:
        ax.plot(x, results[n_plot][method_key]['u_approx'],
                label=f"{method_name} (err={results[n_plot][method_key]['max_error']:.1e})")
    ax.set_xlabel('x')
    ax.set_ylabel('U(x)')
    ax.set_title(f'Решения (N={n_plot})')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 2. Погрешности (N=10)
    ax = axes[0, 1]
    for method_key, method_name, _ in methods:
        error = np.abs(u_exact - results[n_plot][method_key]['u_approx'])
        ax.plot(x, error, label=method_name)
    ax.set_xlabel('x')
    ax.set_ylabel('|Error|')
    ax.set_title(f'Погрешность (N={n_plot})')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')

    # 3. Сходимость по Max ошибке
    ax = axes[1, 0]
    for method_key, method_name, _ in methods:
        n_vals = []
        errors = []
        for n in n_values:
            n_vals.append(n)
            errors.append(results[n][method_key]['max_error'])
        ax.loglog(n_vals, errors, 'o-', linewidth=2, label=method_name)
    ax.set_xlabel('Число базисных функций (N)')
    ax.set_ylabel('Max ошибка')
    ax.set_title('Сходимость методов')
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')

    # 4. Время вычислений
    ax = axes[1, 1]
    for method_key, method_name, _ in methods:
        n_vals = []
        times = []
        for n in n_values:
            n_vals.append(n)
            times.append(results[n][method_key]['time_ms'])
        ax.plot(n_vals, times, 'o-', linewidth=2, label=method_name)
    ax.set_xlabel('Число базисных функций (N)')
    ax.set_ylabel('Время (мс)')
    ax.set_title('Вычислительные затраты')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('results/boundary_layer_results.png', dpi=150, bbox_inches='tight')
    plt.show()

    print("\n" + "=" * 80)
    print("РЕЗУЛЬТАТЫ СОХРАНЕНЫ В: results/")
    print("  - boundary_layer_convergence.csv")
    print("  - boundary_layer_results.png")
    print("=" * 80)

    return results


if __name__ == "__main__":
    run_experiment()