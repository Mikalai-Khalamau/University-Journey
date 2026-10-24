#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
СРАВНЕНИЕ 4 МЕТОДОВ НА ДВУХ БАЗИСАХ
Для научного отчёта по численным методам
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve
import time
import csv
import os


# ============================================================================
# БАЗИС 1: СТЕПЕННЫЕ ПОЛИНОМЫ (как в статье Малышева)
# ============================================================================

class PolynomialBasis:
    """φ_k(x) = x^k * (1-x)"""

    @staticmethod
    def phi(x, k):
        return (x ** k) * (1 - x)

    @staticmethod
    def phi_deriv1(x, k):
        if k == 0:
            return -np.ones_like(x)
        return k * (x ** (k - 1)) * (1 - x) - (x ** k)

    @staticmethod
    def phi_deriv2(x, k):
        if k == 0:
            return np.zeros_like(x)
        if k == 1:
            return -2 * np.ones_like(x)
        return k * (k - 1) * (x ** (k - 2)) * (1 - x) - 2 * k * (x ** (k - 1))


# ============================================================================
# БАЗИС 2: ТРИГОНОМЕТРИЧЕСКИЕ ФУНКЦИИ
# ============================================================================

class TrigBasis:
    """φ_k(x) = sin(k * π * x)"""

    @staticmethod
    def phi(x, k):
        return np.sin(k * np.pi * x)

    @staticmethod
    def phi_deriv1(x, k):
        return k * np.pi * np.cos(k * np.pi * x)

    @staticmethod
    def phi_deriv2(x, k):
        return -(k * np.pi) ** 2 * np.sin(k * np.pi * x)


# ============================================================================
# ТЕСТОВОЕ УРАВНЕНИЕ
# ============================================================================

class TestEquation:
    """-y'' + y = 1, y(0) = 0, y(1) = 0"""

    @staticmethod
    def f(x):
        return np.ones_like(x)

    @staticmethod
    def exact(x):
        return 1 - np.cosh(x - 0.5) / np.cosh(0.5)

    @staticmethod
    def exact_at_zero():
        return 1 - 1 / np.cosh(0.5)  # ≈ 0.1132


# ============================================================================
# 4 ПРОЕКЦИОННЫХ МЕТОДА
# ============================================================================

class ProjectionMethods:
    def __init__(self, n_funcs, basis):
        self.n_funcs = n_funcs
        self.basis = basis
        self.coefficients = None
        self.condition_number = None

    def _build_matrix(self, x, deriv):
        """Построить матрицу базисных функций"""
        n = len(x)
        Phi = np.zeros((n, self.n_funcs))
        for k in range(1, self.n_funcs + 1):
            if deriv == 0:
                Phi[:, k - 1] = self.basis.phi(x, k)
            elif deriv == 1:
                Phi[:, k - 1] = self.basis.phi_deriv1(x, k)
            elif deriv == 2:
                Phi[:, k - 1] = self.basis.phi_deriv2(x, k)
        return Phi

    def collocation(self, f, x):
        """Метод коллокаций: R(x_i) = 0"""
        start = time.perf_counter()
        n = self.n_funcs
        x_coll = np.linspace(1 / (n + 1), n / (n + 1), n)

        Phi_dd = self._build_matrix(x_coll, deriv=2)
        Phi = self._build_matrix(x_coll, deriv=0)

        A = -Phi_dd + Phi
        B = f(x_coll)

        try:
            self.coefficients = solve(A, B)
            self.condition_number = np.linalg.cond(A)
        except:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        return self.coefficients, (time.perf_counter() - start) * 1000

    def galerkin(self, f, x):
        """Метод Галеркина: ∫R·φ_i dx = 0"""
        start = time.perf_counter()
        n = self.n_funcs
        x_int = np.linspace(0, 1, 200)
        dx = x_int[1] - x_int[0]

        Phi_dd = self._build_matrix(x_int, deriv=2)
        Phi = self._build_matrix(x_int, deriv=0)

        A = np.zeros((n, n))
        B = np.zeros(n)

        for i in range(n):
            for j in range(n):
                A[i, j] = np.sum((-Phi_dd[:, j] + Phi[:, j]) * Phi[:, i]) * dx
            B[i] = np.sum(f(x_int) * Phi[:, i]) * dx

        try:
            self.coefficients = solve(A, B)
            self.condition_number = np.linalg.cond(A)
        except:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        return self.coefficients, (time.perf_counter() - start) * 1000

    def malyshev(self, f, x):
        """Метод Малышева: ∫R^(k)dx = 0"""
        start = time.perf_counter()
        n = self.n_funcs
        x_int = np.linspace(0, 1, 200)
        dx = x_int[1] - x_int[0]

        A = np.zeros((n, n))
        B = np.zeros(n)
        x_0, x_1 = np.array([0.0]), np.array([1.0])

        for k in range(n):
            if k == 0:
                # ∫R dx = 0
                Phi_dd = self._build_matrix(x_int, deriv=2)
                Phi = self._build_matrix(x_int, deriv=0)
                A[k, :] = np.sum(-Phi_dd + Phi, axis=0) * dx
                B[k] = np.sum(f(x_int)) * dx
            elif k == 1:
                # ∫R' dx = 0 → R(1) - R(0) = 0
                Phi_dd_0 = self._build_matrix(x_0, deriv=2)
                Phi_dd_1 = self._build_matrix(x_1, deriv=2)
                Phi_0 = self._build_matrix(x_0, deriv=0)
                Phi_1 = self._build_matrix(x_1, deriv=0)
                A[k, :] = (-Phi_dd_1 + Phi_1)[0] - (-Phi_dd_0 + Phi_0)[0]
                B[k] = f(x_1)[0] - f(x_0)[0]
            else:
                # k >= 2: численное интегрирование
                Phi_dd = self._build_matrix(x_int, deriv=2)
                Phi = self._build_matrix(x_int, deriv=0)
                A[k, :] = np.sum(-Phi_dd + Phi, axis=0) * dx
                B[k] = np.sum(f(x_int)) * dx

        try:
            self.coefficients = solve(A, B)
            self.condition_number = np.linalg.cond(A)
        except:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        return self.coefficients, (time.perf_counter() - start) * 1000

    def get_solution(self, x):
        Phi = self._build_matrix(x, deriv=0)
        return Phi @ self.coefficients

    def get_residual(self, f, x):
        Phi_dd = self._build_matrix(x, deriv=2)
        Phi = self._build_matrix(x, deriv=0)
        return -Phi_dd @ self.coefficients + Phi @ self.coefficients - f(x)


# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================================

def run_comparison():
    print("=" * 80)
    print("СРАВНЕНИЕ 4 МЕТОДОВ НА ДВУХ БАЗИСАХ")
    print("Уравнение: -y'' + y = 1, y(0) = 0, y(1) = 0")
    print("=" * 80)

    n_funcs = 3
    x = np.linspace(0, 1, 200)
    y_exact = TestEquation.exact(x)

    bases = [
        ('polynomial', 'Степенные полиномы', PolynomialBasis),
        ('trig', 'Тригонометрический', TrigBasis)
    ]

    methods = [
        ('collocation', 'Коллокация'),
        ('galerkin', 'Галеркин'),
        ('malyshev', 'Малышев')
    ]

    all_results = {}

    for basis_key, basis_name, basis_class in bases:
        print(f"\n{'=' * 60}")
        print(f"БАЗИС: {basis_name}")
        print(f"{'=' * 60}")

        all_results[basis_key] = []

        for method_key, method_name in methods:
            print(f"\n[{method_name}]...")

            solver = ProjectionMethods(n_funcs, basis_class())
            method_map = {
                'collocation': solver.collocation,
                'galerkin': solver.galerkin,
                'malyshev': solver.malyshev
            }

            try:
                C, t_ms = method_map[method_key](TestEquation.f, x)
                y_approx = solver.get_solution(x)
                residual = solver.get_residual(TestEquation.f, x)

                max_err = np.max(np.abs(y_exact - y_approx))
                rms_err = np.sqrt(np.mean((y_exact - y_approx) ** 2))
                max_res = np.max(np.abs(residual))

                all_results[basis_key].append({
                    'method': method_name,
                    'basis': basis_name,
                    'max_error': max_err,
                    'rms_error': rms_err,
                    'max_residual': max_res,
                    'time_ms': t_ms,
                    'cond': solver.condition_number,
                    'y_approx': y_approx
                })

                print(f"  Max ошибка: {max_err:.2e}")
                print(f"  RMS ошибка: {rms_err:.2e}")
                print(f"  Max невязка: {max_res:.2e}")
                print(f"  Время: {t_ms:.2f} мс")
                print(f"  cond(A): {solver.condition_number:.2f}")

            except Exception as e:
                print(f"  ОШИБКА: {e}")
                all_results[basis_key].append({
                    'method': method_name,
                    'basis': basis_name,
                    'max_error': np.inf,
                    'rms_error': np.inf,
                    'max_residual': np.inf,
                    'time_ms': 0,
                    'cond': np.inf
                })

    # Анализ
    print("\n" + "=" * 80)
    print("СРАВНЕНИЕ БАЗИСОВ")
    print("=" * 80)

    for method_key, method_name in methods:
        print(f"\n{method_name}:")
        for basis_key, basis_name, _ in bases:
            for res in all_results[basis_key]:
                if res['method'] == method_name:
                    print(f"  {basis_name:25s}: Max ошибка = {res['max_error']:.2e}, cond = {res['cond']:.2f}")

    # Сохранение
    os.makedirs('results', exist_ok=True)

    with open('results/basis_comparison.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['Базис', 'Метод', 'Max Error', 'RMS Error', 'Max Residual', 'Time (ms)', 'cond(A)'])
        for basis_key in all_results:
            for res in all_results[basis_key]:
                w.writerow([
                    res['basis'],
                    res['method'],
                    f"{res['max_error']:.6e}",
                    f"{res['rms_error']:.6e}",
                    f"{res['max_residual']:.6e}",
                    f"{res['time_ms']:.4f}",
                    f"{res['cond']:.4f}"
                ])

    # Графики
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Решения на полиномиальном базисе
    ax = axes[0, 0]
    ax.plot(x, y_exact, 'k--', linewidth=2, label='Точное')
    for res in all_results['polynomial']:
        if res['max_error'] != np.inf:
            ax.plot(x, res['y_approx'], label=f"{res['method']} ({res['max_error']:.1e})")
    ax.set_xlabel('x')
    ax.set_ylabel('y(x)')
    ax.set_title('Степенные полиномы (N=3)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # 2. Решения на тригонометрическом базисе
    ax = axes[0, 1]
    ax.plot(x, y_exact, 'k--', linewidth=2, label='Точное')
    for res in all_results['trig']:
        if res['max_error'] != np.inf:
            ax.plot(x, res['y_approx'], label=f"{res['method']} ({res['max_error']:.1e})")
    ax.set_xlabel('x')
    ax.set_ylabel('y(x)')
    ax.set_title('Тригонометрический базис (N=3)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # 3. Сравнение точности по базисам
    ax = axes[1, 0]
    method_names = [res['method'] for res in all_results['polynomial']]
    x_pos = np.arange(len(method_names))
    width = 0.35

    poly_errors = [res['max_error'] for res in all_results['polynomial']]
    trig_errors = [res['max_error'] for res in all_results['trig']]

    ax.bar(x_pos - width / 2, poly_errors, width, label='Полиномы', color='blue')
    ax.bar(x_pos + width / 2, trig_errors, width, label='Тригонометрия', color='orange')
    ax.set_yscale('log')
    ax.set_ylabel('Max ошибка (log)')
    ax.set_title('Сравнение точности по базисам')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(method_names, rotation=15)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')

    # 4. Сравнение обусловленности
    ax = axes[1, 1]
    poly_cond = [res['cond'] for res in all_results['polynomial']]
    trig_cond = [res['cond'] for res in all_results['trig']]

    ax.bar(x_pos - width / 2, poly_cond, width, color='blue')
    ax.bar(x_pos + width / 2, trig_cond, width, color='orange')
    ax.set_yscale('log')
    ax.set_ylabel('cond(A) (log)')
    ax.set_title('Сравнение обусловленности')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(method_names, rotation=15)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('results/basis_comparison.png', dpi=150)
    plt.show()

    print("\n" + "=" * 80)
    print("РЕЗУЛЬТАТЫ СОХРАНЕНЫ В: results/")
    print("=" * 80)

    return all_results


if __name__ == "__main__":
    run_comparison()