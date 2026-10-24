#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ЭТАП 3: Исследование сходимости методов
Зависимость погрешности от числа базисных функций N
N = 3, 5, 7, 10, 15, 20
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import legendre, chebyt
from scipy.linalg import solve
import time
import csv
import os
from datetime import datetime


# ============================================================================
# БАЗИСНЫЕ ФУНКЦИИ
# ============================================================================

class BasisFunctions:
    """Класс для генерации базисных функций и их производных"""

    @staticmethod
    def trigonometric(x, k):
        """Тригонометрический базис: φ_k(x) = sin(k·π·x)"""
        return np.sin(k * np.pi * x)

    @staticmethod
    def trigonometric_deriv2(x, k):
        """Вторая производная: φ''_k(x) = -(k·π)²·sin(k·π·x)"""
        return -(k * np.pi) ** 2 * np.sin(k * np.pi * x)

    @staticmethod
    def trigonometric_deriv_k(x, k, deriv_order):
        """Производная порядка deriv_order для тригонометрического базиса"""
        pi = np.pi
        if deriv_order % 4 == 0:
            return (k * pi) ** deriv_order * np.sin(k * pi * x)
        elif deriv_order % 4 == 1:
            return (k * pi) ** deriv_order * np.cos(k * pi * x)
        elif deriv_order % 4 == 2:
            return -(k * pi) ** deriv_order * np.sin(k * pi * x)
        else:
            return -(k * pi) ** deriv_order * np.cos(k * pi * x)

    @staticmethod
    def get_basis(name, x, k):
        """Получить базисную функцию по имени"""
        if name == 'trig':
            return BasisFunctions.trigonometric(x, k)
        elif name == 'legendre':
            P_k = legendre(k)
            return x * (1 - x) * P_k(2 * x - 1)
        elif name == 'chebyshev':
            T_k = chebyt(k)
            return x * (1 - x) * T_k(2 * x - 1)
        else:
            raise ValueError(f"Неизвестный базис: {name}")

    @staticmethod
    def get_basis_deriv2(name, x, k):
        """Получить вторую производную базисной функции"""
        if name == 'trig':
            return BasisFunctions.trigonometric_deriv2(x, k)
        else:
            h = 1e-6
            phi_plus = BasisFunctions.get_basis(name, x + h, k)
            phi_minus = BasisFunctions.get_basis(name, x - h, k)
            phi_center = BasisFunctions.get_basis(name, x, k)
            return (phi_plus - 2 * phi_center + phi_minus) / (h ** 2)

    @staticmethod
    def get_basis_deriv_k(name, x, k, deriv_order):
        """Получить производную порядка deriv_order"""
        if name == 'trig':
            return BasisFunctions.trigonometric_deriv_k(x, k, deriv_order)
        else:
            h = 1e-5
            phi = BasisFunctions.get_basis(name, x, k)
            for _ in range(deriv_order):
                phi_plus = BasisFunctions.get_basis(name, x + h, k)
                phi_minus = BasisFunctions.get_basis(name, x - h, k)
                phi = (phi_plus - phi_minus) / (2 * h)
            return phi


# ============================================================================
# ТЕСТОВЫЕ УРАВНЕНИЯ
# ============================================================================

class TestEquations:
    """Класс с тестовыми уравнениями"""

    @staticmethod
    def poisson_f(x):
        """Правая часть уравнения Пуассона: -U'' = π²·sin(π·x)"""
        return np.pi ** 2 * np.sin(np.pi * x)

    @staticmethod
    def poisson_exact(x):
        """Точное решение: U(x) = sin(π·x)"""
        return np.sin(np.pi * x)

    @staticmethod
    def polynomial_f(x):
        """Правая часть: -U'' = 2"""
        return 2 * np.ones_like(x)

    @staticmethod
    def polynomial_exact(x):
        """Точное решение: U(x) = x - x²"""
        return x - x ** 2

    @staticmethod
    def poisson_bc():
        """Граничные условия: U(0) = 0, U(1) = 0"""
        return 0.0, 0.0


# ============================================================================
# ПРОЕКЦИОННЫЕ МЕТОДЫ
# ============================================================================

class ProjectionMethods:
    """Класс с реализацией 4 проекционных методов"""

    def __init__(self, n_funcs=5, basis_type='trig'):
        self.n_funcs = n_funcs
        self.basis_type = basis_type
        self.coefficients = None
        self.matrix_A = None
        self.condition_number = None

    def _build_basis_matrix(self, x_points, deriv_order=0):
        """Построить матрицу базисных функций или их производных"""
        n = len(x_points)
        Phi = np.zeros((n, self.n_funcs))
        for k in range(1, self.n_funcs + 1):
            if deriv_order == 0:
                Phi[:, k - 1] = BasisFunctions.get_basis(self.basis_type, x_points, k)
            elif deriv_order == 2:
                Phi[:, k - 1] = BasisFunctions.get_basis_deriv2(self.basis_type, x_points, k)
            else:
                Phi[:, k - 1] = BasisFunctions.get_basis_deriv_k(self.basis_type, x_points, k, deriv_order)
        return Phi

    def collocation(self, equation_f, x_points):
        """Метод коллокаций: R(x_i) = 0"""
        start_time = time.perf_counter()

        n = self.n_funcs
        x_coll = np.linspace(0.1, 0.9, n)
        Phi_dd = self._build_basis_matrix(x_coll, deriv_order=2)
        F = equation_f(x_coll)

        A = -Phi_dd
        B = F

        try:
            self.coefficients = solve(A, B)
            self.matrix_A = A
            self.condition_number = np.linalg.cond(A)
        except:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        elapsed_time = (time.perf_counter() - start_time) * 1000
        return self.coefficients, elapsed_time

    def least_squares_integral(self, equation_f, x_points):
        """Интегральный МНК: min ∫R²dx"""
        start_time = time.perf_counter()

        n = self.n_funcs
        x_int = np.linspace(0, 1, 200)
        dx = x_int[1] - x_int[0]

        Phi_dd = self._build_basis_matrix(x_int, deriv_order=2)
        F = equation_f(x_int)

        A = Phi_dd.T @ Phi_dd * dx
        B = -Phi_dd.T @ F * dx

        try:
            self.coefficients = solve(A, B)
            self.matrix_A = A
            self.condition_number = np.linalg.cond(A)
        except:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        elapsed_time = (time.perf_counter() - start_time) * 1000
        return self.coefficients, elapsed_time

    def galerkin_classical(self, equation_f, x_points):
        """Классический метод Галеркина: ∫R·φ_i dx = 0"""
        start_time = time.perf_counter()

        n = self.n_funcs
        x_int = np.linspace(0, 1, 200)
        dx = x_int[1] - x_int[0]

        Phi_dd = self._build_basis_matrix(x_int, deriv_order=2)
        Phi = self._build_basis_matrix(x_int, deriv_order=0)
        F = equation_f(x_int)

        A = np.zeros((n, n))
        B = np.zeros(n)

        for i in range(n):
            for j in range(n):
                A[i, j] = np.sum(Phi[:, i] * Phi_dd[:, j]) * dx
            B[i] = -np.sum(Phi[:, i] * F) * dx

        try:
            self.coefficients = solve(A, B)
            self.matrix_A = A
            self.condition_number = np.linalg.cond(A)
        except:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        elapsed_time = (time.perf_counter() - start_time) * 1000
        return self.coefficients, elapsed_time

    def galerkin_malyshev(self, equation_f, x_points):
        """
        Модифицированный метод Галеркина (Малышева): ∫R^(k)(x)dx = 0
        """
        start_time = time.perf_counter()

        n = self.n_funcs
        x_int = np.linspace(0, 1, 200)
        dx = x_int[1] - x_int[0]

        F = equation_f(x_int)
        pi = np.pi

        F_derivs = []
        for k in range(n):
            deriv_order = k
            if deriv_order % 2 == 0:
                sign = (-1) ** (deriv_order // 2)
                F_derivs.append(sign * (pi ** (2 + deriv_order)) * np.sin(pi * x_int))
            else:
                sign = (-1) ** (deriv_order // 2)
                F_derivs.append(sign * (pi ** (2 + deriv_order)) * np.cos(pi * x_int))

        A = np.zeros((n, n))
        B = np.zeros(n)

        for k in range(n):
            deriv_order = k + 2

            for j in range(1, n + 1):
                if self.basis_type == 'trig':
                    if deriv_order % 4 == 0:
                        phi_deriv = (j * pi) ** deriv_order * np.sin(j * pi * x_int)
                    elif deriv_order % 4 == 1:
                        phi_deriv = (j * pi) ** deriv_order * np.cos(j * pi * x_int)
                    elif deriv_order % 4 == 2:
                        phi_deriv = -(j * pi) ** deriv_order * np.sin(j * pi * x_int)
                    else:
                        phi_deriv = -(j * pi) ** deriv_order * np.cos(j * pi * x_int)
                else:
                    phi_deriv = BasisFunctions.get_basis_deriv_k(self.basis_type, x_int, j, deriv_order)

                A[k, j - 1] = -np.sum(phi_deriv) * dx

            B[k] = np.sum(F_derivs[k]) * dx

        try:
            self.coefficients = solve(A, B)
            self.matrix_A = A
            self.condition_number = np.linalg.cond(A)
        except:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        elapsed_time = (time.perf_counter() - start_time) * 1000
        return self.coefficients, elapsed_time

    def get_solution(self, x_points):
        """Получить приближённое решение"""
        if self.coefficients is None:
            raise ValueError("Сначала нужно решить уравнение!")
        Phi = self._build_basis_matrix(x_points, deriv_order=0)
        return Phi @ self.coefficients

    def get_residual(self, equation_f, x_points):
        """Получить невязку"""
        if self.coefficients is None:
            raise ValueError("Сначала нужно решить уравнение!")
        Phi_dd = self._build_basis_matrix(x_points, deriv_order=2)
        F = equation_f(x_points)
        U_approx_dd = Phi_dd @ self.coefficients
        return -U_approx_dd - F


# ============================================================================
# МЕТРИКИ
# ============================================================================

class Metrics:
    """Класс для расчёта метрик качества"""

    @staticmethod
    def max_error(u_exact, u_approx):
        return np.max(np.abs(u_exact - u_approx))

    @staticmethod
    def rms_error(u_exact, u_approx):
        return np.sqrt(np.mean((u_exact - u_approx) ** 2))

    @staticmethod
    def max_residual(residual):
        return np.max(np.abs(residual))

    @staticmethod
    def relative_error(u_exact, u_approx):
        max_exact = np.max(np.abs(u_exact))
        if max_exact == 0:
            return np.inf
        return (np.max(np.abs(u_exact - u_approx)) / max_exact) * 100

    @staticmethod
    def convergence_rate(n_values, errors):
        """Вычислить порядок сходимости"""
        if len(n_values) < 2 or len(errors) < 2:
            return None

        log_n = np.log(n_values)
        log_e = np.log(errors)

        # Линейная регрессия для оценки порядка сходимости
        slope = np.polyfit(log_n, log_e, 1)[0]
        return -slope  # Отрицательный наклон = порядок сходимости


# ============================================================================
# ВИЗУАЛИЗАЦИЯ
# ============================================================================

class Visualization:
    """Класс для построения графиков"""

    @staticmethod
    def plot_convergence(results_by_n, save_path='results/stage3_convergence.png'):
        """Построить график сходимости (log-log масштаб)"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        method_colors = {'collocation': 'blue', 'least_squares': 'green',
                         'galerkin': 'red', 'malyshev': 'orange'}
        method_names = {'collocation': 'Коллокация', 'least_squares': 'МНК',
                        'galerkin': 'Галеркин', 'malyshev': 'Малышев'}
        markers = {'collocation': 'o', 'least_squares': 's',
                   'galerkin': '^', 'malyshev': 'd'}

        # 1. Сходимость по максимальной погрешности (log-log)
        ax = axes[0, 0]

        for method in ['collocation', 'least_squares', 'galerkin', 'malyshev']:
            n_values = []
            errors = []

            for n, results in results_by_n.items():
                for res in results:
                    if res['method'] == method and res['max_error'] < 1e-10:
                        n_values.append(n)
                        errors.append(res['max_error'])
                        break

            if n_values:
                ax.loglog(n_values, errors, markers[method], color=method_colors[method],
                          linewidth=2, markersize=8, label=f"{method_names[method]}")

                # Добавить линию тренда
                if len(n_values) >= 2:
                    z = np.polyfit(np.log(n_values), np.log(errors), 1)
                    p = np.poly1d(z)
                    ax.loglog(n_values, np.exp(p(np.log(n_values))),
                              color=method_colors[method], linestyle='--', alpha=0.5)

        ax.set_xlabel('Число базисных функций (N)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Максимальная погрешность', fontsize=12, fontweight='bold')
        ax.set_title('Сходимость методов (log-log масштаб)', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--', which='both')

        # 2. Сходимость по RMS погрешности
        ax = axes[0, 1]

        for method in ['collocation', 'least_squares', 'galerkin', 'malyshev']:
            n_values = []
            errors = []

            for n, results in results_by_n.items():
                for res in results:
                    if res['method'] == method and res['rms_error'] < 1e-10:
                        n_values.append(n)
                        errors.append(res['rms_error'])
                        break

            if n_values:
                ax.loglog(n_values, errors, markers[method], color=method_colors[method],
                          linewidth=2, markersize=8, label=f"{method_names[method]}")

        ax.set_xlabel('Число базисных функций (N)', fontsize=12, fontweight='bold')
        ax.set_ylabel('RMS погрешность', fontsize=12, fontweight='bold')
        ax.set_title('Сходимость по RMS погрешности', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--', which='both')

        # 3. Число обусловленности vs N
        ax = axes[1, 0]

        for method in ['collocation', 'least_squares', 'galerkin', 'malyshev']:
            n_values = []
            conds = []

            for n, results in results_by_n.items():
                for res in results:
                    if res['method'] == method and res['condition_number'] != np.inf:
                        n_values.append(n)
                        conds.append(res['condition_number'])
                        break

            if n_values:
                ax.semilogy(n_values, conds, markers[method], color=method_colors[method],
                            linewidth=2, markersize=8, label=f"{method_names[method]}")

        ax.set_xlabel('Число базисных функций (N)', fontsize=12, fontweight='bold')
        ax.set_ylabel('cond(A) (log scale)', fontsize=12, fontweight='bold')
        ax.set_title('Устойчивость методов (число обусловленности)', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--', which='both')

        # 4. Время вычислений vs N
        ax = axes[1, 1]

        for method in ['collocation', 'least_squares', 'galerkin', 'malyshev']:
            n_values = []
            times = []

            for n, results in results_by_n.items():
                for res in results:
                    if res['method'] == method:
                        n_values.append(n)
                        times.append(res['time_ms'])
                        break

            if n_values:
                ax.plot(n_values, times, markers[method], color=method_colors[method],
                        linewidth=2, markersize=8, label=f"{method_names[method]}")

        ax.set_xlabel('Число базисных функций (N)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Время вычислений (мс)', fontsize=12, fontweight='bold')
        ax.set_title('Вычислительная эффективность', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--')

        plt.suptitle(
            'ЭТАП 3: Исследование сходимости методов\nУравнение Пуассона: -U\'\' = π²·sin(π·x), N = 3,5,7,10,15,20',
            fontsize=16, fontweight='bold', y=1.02)

        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show()

        print(f"✓ График сохранён: {save_path}")

    @staticmethod
    def save_results_to_csv(results_by_n, save_path='results/stage3_convergence.csv'):
        """Сохранить результаты в CSV"""
        os.makedirs('results', exist_ok=True)

        with open(save_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')

            writer.writerow(['N', 'Метод', 'Базис', 'Max Error', 'RMS Error',
                             'Max Residual', 'Time (ms)', 'cond(A)', 'Отн. погрешность (%)'])

            for n, results in sorted(results_by_n.items()):
                for res in results:
                    writer.writerow([
                        n,
                        res['method_name'],
                        res['basis_type'],
                        f"{res['max_error']:.6e}",
                        f"{res['rms_error']:.6e}",
                        f"{res['max_residual']:.6e}",
                        f"{res['time_ms']:.4f}",
                        f"{res['condition_number']:.4f}",
                        f"{res['relative_error']:.4f}"
                    ])

        print(f"✓ Результаты сохранены: {save_path}")


# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ ЭТАПА 3
# ============================================================================

def run_stage3_experiment():
    """Запустить Этап 3: Исследование сходимости"""
    print("=" * 80)
    print("ЭТАП 3: ИССЛЕДОВАНИЕ СХОДИМОСТИ МЕТОДОВ")
    print("=" * 80)
    print(f"Дата начала: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Параметры эксперимента
    equation_name = 'Уравнение Пуассона'
    basis_type = 'trig'
    basis_name = 'Тригонометрический'

    # Значения N для исследования
    n_values = [3, 5, 7, 10, 15, 20]

    methods = [
        ('collocation', 'Коллокация'),
        ('least_squares', 'МНК интегральный'),
        ('galerkin', 'Галеркин классический'),
        ('malyshev', 'Галеркин Малышева')
    ]

    # Сетка для вычислений
    x = np.linspace(0, 1, 200)

    # Точное решение
    u_exact = TestEquations.poisson_exact(x)
    f = TestEquations.poisson_f

    results_by_n = {}

    print("-" * 80)
    print("ВЫПОЛНЕНИЕ РАСЧЁТОВ")
    print("-" * 80)

    for n in n_values:
        print(f"\n{'=' * 60}")
        print(f"ЧИСЛО БАЗИСНЫХ ФУНКЦИЙ: N = {n}")
        print(f"{'=' * 60}")

        results_by_n[n] = []

        for method_key, method_name in methods:
            print(f"\n  [{method_name}]...")

            try:
                solver = ProjectionMethods(n_funcs=n, basis_type=basis_type)

                method_map = {
                    'collocation': solver.collocation,
                    'least_squares': solver.least_squares_integral,
                    'galerkin': solver.galerkin_classical,
                    'malyshev': solver.galerkin_malyshev
                }

                coefficients, time_ms = method_map[method_key](f, x)
                u_approx = solver.get_solution(x)
                residual = solver.get_residual(f, x)

                max_error = Metrics.max_error(u_exact, u_approx)
                rms_error = Metrics.rms_error(u_exact, u_approx)
                max_residual = Metrics.max_residual(residual)
                relative_error = Metrics.relative_error(u_exact, u_approx)

                results_by_n[n].append({
                    'method': method_key,
                    'method_name': method_name,
                    'basis_type': basis_type,
                    'n_funcs': n,
                    'x': x,
                    'u_approx': u_approx,
                    'u_exact': u_exact,
                    'error': u_exact - u_approx,
                    'residual': residual,
                    'max_error': max_error,
                    'rms_error': rms_error,
                    'max_residual': max_residual,
                    'relative_error': relative_error,
                    'time_ms': time_ms,
                    'condition_number': solver.condition_number,
                    'coefficients': coefficients
                })

                print(f"    ✓ Max ошибка: {max_error:.2e}")
                print(f"    ✓ RMS ошибка: {rms_error:.2e}")
                print(f"    ✓ Время: {time_ms:.2f} мс")
                print(f"    ✓ cond(A): {solver.condition_number:.2f}")

            except Exception as e:
                print(f"    ✗ Ошибка: {e}")
                results_by_n[n].append({
                    'method': method_key,
                    'method_name': method_name,
                    'basis_type': basis_type,
                    'n_funcs': n,
                    'max_error': np.inf,
                    'rms_error': np.inf,
                    'max_residual': np.inf,
                    'time_ms': 0,
                    'condition_number': np.inf,
                    'error': None
                })

    print()
    print("-" * 80)
    print("АНАЛИЗ РЕЗУЛЬТАТОВ")
    print("-" * 80)

    # Анализ сходимости для каждого метода
    for method_key, method_name in methods:
        n_vals = []
        errors = []

        for n in n_values:
            for res in results_by_n[n]:
                if res['method'] == method_key and res['max_error'] != np.inf:
                    n_vals.append(n)
                    errors.append(res['max_error'])
                    break

        if len(n_vals) >= 2:
            rate = Metrics.convergence_rate(n_vals, errors)
            if rate:
                print(f"\n★ Порядок сходимости {method_name}: {rate:.2f}")

    # Сравнение методов при N=20
    print(f"\n{'=' * 60}")
    print(f"СРАВНЕНИЕ ПРИ N = 20 (максимальное)")
    print(f"{'=' * 60}")

    final_results = results_by_n[20]
    sorted_by_error = sorted([r for r in final_results if r['max_error'] != np.inf],
                             key=lambda x: x['max_error'])

    for i, res in enumerate(sorted_by_error, 1):
        print(f"  {i}. {res['method_name']:25s} → Max Error = {res['max_error']:.2e}")

    print()
    print("-" * 80)
    print("СОХРАНЕНИЕ РЕЗУЛЬТАТОВ")
    print("-" * 80)

    os.makedirs('results', exist_ok=True)
    Visualization.save_results_to_csv(results_by_n, 'results/stage3_convergence.csv')
    Visualization.plot_convergence(results_by_n, 'results/stage3_convergence.png')

    print()
    print("=" * 80)
    print(f"ЭТАП 3 ЗАВЕРШЁН: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    return results_by_n


# ============================================================================
# АНАЛИЗ РЕЗУЛЬТАТОВ
# ============================================================================

def analyze_stage3_results(results_by_n):
    """Подробный анализ результатов Этапа 3"""
    print("\n" + "=" * 80)
    print("ПОДРОБНЫЙ АНАЛИЗ РЕЗУЛЬТАТОВ ЭТАПА 3")
    print("=" * 80)

    n_values = [3, 5, 7, 10, 15, 20]
    methods = ['collocation', 'least_squares', 'galerkin', 'malyshev']
    method_names = {'collocation': 'Коллокация', 'least_squares': 'МНК',
                    'galerkin': 'Галеркин', 'malyshev': 'Малышев'}

    # 1. Таблица сходимости
    print("\n1. ТАБЛИЦА СХОДИМОСТИ (Max ошибка)")
    print("-" * 80)

    header = f"{'N':>5}"
    for method in methods:
        header += f"│{method_names[method]:>18}"
    print(header)
    print("-" * 80)

    for n in n_values:
        row = f"{n:>5}"
        for method in methods:
            for res in results_by_n[n]:
                if res['method'] == method:
                    if res['max_error'] != np.inf:
                        row += f"│{res['max_error']:>18.2e}"
                    else:
                        row += f"│{'∞':>18}"
                    break
        print(row)

    # 2. Порядок сходимости
    print("\n2. ПОРЯДОК СХОДИМОСТИ МЕТОДОВ")
    print("-" * 80)

    for method in methods:
        n_vals = []
        errors = []

        for n in n_values:
            for res in results_by_n[n]:
                if res['method'] == method and res['max_error'] != np.inf and res['max_error'] > 1e-15:
                    n_vals.append(n)
                    errors.append(res['max_error'])
                    break

        if len(n_vals) >= 2:
            rate = Metrics.convergence_rate(n_vals, errors)
            if rate:
                print(f"  {method_names[method]:20s} → Порядок сходимости: {rate:.2f}")

    # 3. Устойчивость при больших N
    print("\n3. УСТОЙЧИВОСТЬ ПРИ БОЛЬШИХ N (cond(A))")
    print("-" * 80)

    for method in methods:
        for res in results_by_n[20]:
            if res['method'] == method:
                status = "✅" if res['condition_number'] < 1e6 else "⚠️" if res['condition_number'] < 1e10 else "❌"
                print(f"  {method_names[method]:20s} → cond(A) = {res['condition_number']:.2e} {status}")
                break

    print()
    print("=" * 80)


# ============================================================================
# ЗАПУСК
# ============================================================================

if __name__ == "__main__":
    results = run_stage3_experiment()
    analyze_stage3_results(results)

    print("\n" + "=" * 80)
    print("СЛЕДУЮЩИЙ ШАГ: Этап 4 - Тестирование на всех 6 уравнениях")
    print("=" * 80)