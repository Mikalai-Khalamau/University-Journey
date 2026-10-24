#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ЭТАП 2: Сравнение базисных функций
Тригонометрический vs Лежандра vs Чебышев
Для всех 4 методов на уравнении Пуассона
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
        else:  # deriv_order % 4 == 3
            return -(k * pi) ** deriv_order * np.cos(k * pi * x)

    @staticmethod
    def legendre(x, k):
        """Базис Лежандра: φ_k(x) = x(1-x)·P_k(2x-1)"""
        P_k = legendre(k)
        return x * (1 - x) * P_k(2 * x - 1)

    @staticmethod
    def chebyshev(x, k):
        """Базис Чебышева: φ_k(x) = x(1-x)·T_k(2x-1)"""
        T_k = chebyt(k)
        return x * (1 - x) * T_k(2 * x - 1)

    @staticmethod
    def get_basis(name, x, k):
        """Получить базисную функцию по имени"""
        if name == 'trig':
            return BasisFunctions.trigonometric(x, k)
        elif name == 'legendre':
            return BasisFunctions.legendre(x, k)
        elif name == 'chebyshev':
            return BasisFunctions.chebyshev(x, k)
        else:
            raise ValueError(f"Неизвестный базис: {name}")

    @staticmethod
    def get_basis_deriv2(name, x, k):
        """Получить вторую производную базисной функции"""
        if name == 'trig':
            return BasisFunctions.trigonometric_deriv2(x, k)
        else:
            # Численное дифференцирование для полиномиальных базисов
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
            # Численное дифференцирование через конечные разности
            h = 1e-5
            if deriv_order == 1:
                phi_plus = BasisFunctions.get_basis(name, x + h, k)
                phi_minus = BasisFunctions.get_basis(name, x - h, k)
                return (phi_plus - phi_minus) / (2 * h)
            elif deriv_order == 2:
                phi_plus = BasisFunctions.get_basis(name, x + h, k)
                phi_minus = BasisFunctions.get_basis(name, x - h, k)
                phi_center = BasisFunctions.get_basis(name, x, k)
                return (phi_plus - 2 * phi_center + phi_minus) / (h ** 2)
            elif deriv_order == 3:
                phi_pp = BasisFunctions.get_basis(name, x + 2 * h, k)
                phi_p = BasisFunctions.get_basis(name, x + h, k)
                phi_m = BasisFunctions.get_basis(name, x - h, k)
                phi_mm = BasisFunctions.get_basis(name, x - 2 * h, k)
                return (phi_pp - 2 * phi_p + 2 * phi_m - phi_mm) / (2 * h ** 3)
            else:
                # Для высших производных используем рекурсивное дифференцирование
                phi = BasisFunctions.get_basis(name, x, k)
                for _ in range(deriv_order):
                    h = 1e-5
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
        Исправленная версия с правильными производными
        """
        start_time = time.perf_counter()

        n = self.n_funcs
        x_int = np.linspace(0, 1, 200)
        dx = x_int[1] - x_int[0]

        F = equation_f(x_int)
        pi = np.pi

        # Вычисляем производные правой части (для Пуассона f = π²·sin(πx))
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
                    # Аналитическая производная для тригонометрического базиса
                    if deriv_order % 4 == 0:
                        phi_deriv = (j * pi) ** deriv_order * np.sin(j * pi * x_int)
                    elif deriv_order % 4 == 1:
                        phi_deriv = (j * pi) ** deriv_order * np.cos(j * pi * x_int)
                    elif deriv_order % 4 == 2:
                        phi_deriv = -(j * pi) ** deriv_order * np.sin(j * pi * x_int)
                    else:
                        phi_deriv = -(j * pi) ** deriv_order * np.cos(j * pi * x_int)
                else:
                    # Численная производная для полиномиальных базисов
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


# ============================================================================
# ВИЗУАЛИЗАЦИЯ
# ============================================================================

class Visualization:
    """Класс для построения графиков"""

    @staticmethod
    def plot_basis_comparison(results_by_basis, save_path='results/stage2_basis_comparison.png'):
        """Построить графики сравнения базисов"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        basis_colors = {'trig': 'blue', 'legendre': 'green', 'chebyshev': 'red'}
        basis_names = {'trig': 'Тригонометрический', 'legendre': 'Лежандра', 'chebyshev': 'Чебышев'}
        method_colors = {'collocation': 'darkblue', 'least_squares': 'darkgreen',
                         'galerkin': 'darkred', 'malyshev': 'orange'}

        # 1. Сравнение решений для разных базисов (метод Галеркина)
        ax = axes[0, 0]
        x = results_by_basis[0]['x']
        u_exact = TestEquations.poisson_exact(x)
        ax.plot(x, u_exact, 'k--', linewidth=3, label='Точное решение', alpha=0.7)

        for res in results_by_basis:
            if res['method'] == 'galerkin':
                ax.plot(x, res['u_approx'], basis_colors[res['basis']], linewidth=2,
                        label=f"{basis_names[res['basis']]} (err={res['max_error']:.2e})")

        ax.set_xlabel('x', fontsize=12, fontweight='bold')
        ax.set_ylabel('U(x)', fontsize=12, fontweight='bold')
        ax.set_title('Сравнение решений (метод Галеркина, N=5)', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--')

        # 2. Погрешности для разных базисов
        ax = axes[0, 1]
        for res in results_by_basis:
            if res['method'] == 'galerkin' and res['error'] is not None:
                ax.plot(x, res['error'], basis_colors[res['basis']], linewidth=2,
                        label=f"{basis_names[res['basis']]}")

        ax.set_xlabel('x', fontsize=12, fontweight='bold')
        ax.set_ylabel('|U_exact - U_approx|', fontsize=12, fontweight='bold')
        ax.set_title('Погрешность решений (метод Галеркина, N=5)', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--')

        # 3. Сравнение методов для каждого базиса (столбчатая диаграмма)
        ax = axes[1, 0]

        methods = ['collocation', 'least_squares', 'galerkin', 'malyshev']
        method_labels = ['Коллокация', 'МНК', 'Галеркин', 'Малышев']
        x_pos = np.arange(len(methods))
        width = 0.25

        for i, basis in enumerate(['trig', 'legendre', 'chebyshev']):
            errors = []
            for method in methods:
                for res in results_by_basis:
                    if res['method'] == method and res['basis'] == basis:
                        errors.append(res['max_error'])
                        break
            ax.bar(x_pos + i * width, errors, width, label=basis_names[basis], color=basis_colors[basis])

        ax.set_xlabel('Метод', fontsize=12, fontweight='bold')
        ax.set_ylabel('Max ошибка (log scale)', fontsize=12, fontweight='bold')
        ax.set_title('Сравнение точности методов для разных базисов', fontsize=14, fontweight='bold')
        ax.set_xticks(x_pos + width)
        ax.set_xticklabels(method_labels, rotation=15)
        ax.set_yscale('log')
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')

        # 4. Таблица метрик
        ax = axes[1, 1]
        ax.axis('off')

        table_data = []
        headers = ['Базис', 'Метод', 'Max Error', 'RMS Error', 'Time (ms)', 'cond(A)']

        for res in results_by_basis:
            row = [
                basis_names[res['basis']],
                res['method_name'],
                f"{res['max_error']:.2e}",
                f"{res['rms_error']:.2e}",
                f"{res['time_ms']:.2f}",
                f"{res['condition_number']:.2f}"
            ]
            table_data.append(row)

        table = ax.table(cellText=table_data, colLabels=headers,
                         loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1.2, 1.6)

        ax.set_title('Сводная таблица метрик (N=5)', fontsize=14, fontweight='bold', pad=20)

        plt.suptitle('ЭТАП 2: Сравнение базисных функций\nУравнение Пуассона: -U\'\' = π²·sin(π·x), U(0)=U(1)=0',
                     fontsize=16, fontweight='bold', y=1.02)

        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show()

        print(f"✓ График сохранён: {save_path}")

    @staticmethod
    def save_results_to_csv(results, save_path='results/stage2_basis_comparison.csv'):
        """Сохранить результаты в CSV"""
        os.makedirs('results', exist_ok=True)

        with open(save_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')

            writer.writerow(['Базис', 'Метод', 'N', 'Max Error', 'RMS Error',
                             'Max Residual', 'Time (ms)', 'cond(A)', 'Отн. погрешность (%)'])

            for res in results:
                writer.writerow([
                    res['basis'],
                    res['method_name'],
                    res['n_funcs'],
                    f"{res['max_error']:.6e}",
                    f"{res['rms_error']:.6e}",
                    f"{res['max_residual']:.6e}",
                    f"{res['time_ms']:.4f}",
                    f"{res['condition_number']:.4f}",
                    f"{res['relative_error']:.4f}"
                ])

        print(f"✓ Результаты сохранены: {save_path}")


# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ ЭТАПА 2
# ============================================================================

def run_stage2_experiment():
    """Запустить Этап 2: Сравнение базисных функций"""
    print("=" * 80)
    print("ЭТАП 2: СРАВНЕНИЕ БАЗИСНЫХ ФУНКЦИЙ")
    print("=" * 80)
    print(f"Дата начала: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Параметры эксперимента
    equation_name = 'Уравнение Пуассона'
    n_funcs = 5

    bases = [
        ('trig', 'Тригонометрический'),
        ('legendre', 'Лежандра'),
        ('chebyshev', 'Чебышев')
    ]

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

    results = []

    print("-" * 80)
    print("ВЫПОЛНЕНИЕ РАСЧЁТОВ")
    print("-" * 80)

    for basis_key, basis_name in bases:
        print(f"\n{'=' * 60}")
        print(f"БАЗИС: {basis_name}")
        print(f"{'=' * 60}")

        for method_key, method_name in methods:
            print(f"\n  [{method_name}]...")

            try:
                solver = ProjectionMethods(n_funcs=n_funcs, basis_type=basis_key)

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

                results.append({
                    'method': method_key,
                    'method_name': method_name,
                    'basis': basis_key,
                    'basis_name': basis_name,
                    'n_funcs': n_funcs,
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
                results.append({
                    'method': method_key,
                    'method_name': method_name,
                    'basis': basis_key,
                    'basis_name': basis_name,
                    'n_funcs': n_funcs,
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

    # Группируем по базисам
    for basis_key, basis_name in bases:
        basis_results = [r for r in results if r['basis'] == basis_key and r['max_error'] != np.inf]
        if basis_results:
            best = min(basis_results, key=lambda x: x['max_error'])
            print(f"\n★ Лучший метод для базиса {basis_name}: {best['method_name']}")
            print(f"  Max погрешность: {best['max_error']:.2e}")

    # Группируем по методам
    for method_key, method_name in methods:
        method_results = [r for r in results if r['method'] == method_key and r['max_error'] != np.inf]
        if method_results:
            best = min(method_results, key=lambda x: x['max_error'])
            print(f"\n★ Лучший базис для метода {method_name}: {best['basis_name']}")
            print(f"  Max погрешность: {best['max_error']:.2e}")

    print()
    print("-" * 80)
    print("СОХРАНЕНИЕ РЕЗУЛЬТАТОВ")
    print("-" * 80)

    os.makedirs('results', exist_ok=True)
    Visualization.save_results_to_csv(results, 'results/stage2_basis_comparison.csv')
    Visualization.plot_basis_comparison(results, 'results/stage2_basis_comparison.png')

    print()
    print("=" * 80)
    print(f"ЭТАП 2 ЗАВЕРШЁН: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    return results


# ============================================================================
# АНАЛИЗ РЕЗУЛЬТАТОВ
# ============================================================================

def analyze_stage2_results(results):
    """Подробный анализ результатов Этапа 2"""
    print("\n" + "=" * 80)
    print("ПОДРОБНЫЙ АНАЛИЗ РЕЗУЛЬТАТОВ ЭТАПА 2")
    print("=" * 80)

    valid_results = [r for r in results if r['max_error'] != np.inf]

    if len(valid_results) < 2:
        print("Недостаточно данных для анализа")
        return

    # 1. Сравнение базисов по точности
    print("\n1. СРАВНЕНИЕ БАЗИСОВ ПО ТОЧНОСТИ (усреднённо по всем методам)")
    print("-" * 80)

    basis_errors = {}
    for basis in ['trig', 'legendre', 'chebyshev']:
        errors = [r['max_error'] for r in valid_results if r['basis'] == basis]
        basis_errors[basis] = np.mean(errors)

    sorted_basis = sorted(basis_errors.items(), key=lambda x: x[1])
    basis_names = {'trig': 'Тригонометрический', 'legendre': 'Лежандра', 'chebyshev': 'Чебышев'}

    for i, (basis, avg_error) in enumerate(sorted_basis, 1):
        print(f"  {i}. {basis_names[basis]:25s} → Средн. ошибка = {avg_error:.2e}")

    # 2. Сравнение методов по базисам
    print("\n2. ЛУЧШИЙ БАЗИС ДЛЯ КАЖДОГО МЕТОДА")
    print("-" * 80)

    method_names = {'collocation': 'Коллокация', 'least_squares': 'МНК',
                    'galerkin': 'Галеркин', 'malyshev': 'Малышев'}

    for method in ['collocation', 'least_squares', 'galerkin', 'malyshev']:
        method_results = [r for r in valid_results if r['method'] == method]
        if method_results:
            best = min(method_results, key=lambda x: x['max_error'])
            print(f"  {method_names[method]:20s} → {basis_names[best['basis']]:20s} (err={best['max_error']:.2e})")

    # 3. Число обусловленности по базисам
    print("\n3. СРАВНЕНИЕ БАЗИСОВ ПО УСТОЙЧИВОСТИ (cond(A))")
    print("-" * 80)

    basis_cond = {}
    for basis in ['trig', 'legendre', 'chebyshev']:
        conds = [r['condition_number'] for r in valid_results if
                 r['basis'] == basis and r['condition_number'] != np.inf]
        if conds:
            basis_cond[basis] = np.mean(conds)

    sorted_cond = sorted(basis_cond.items(), key=lambda x: x[1])

    for i, (basis, avg_cond) in enumerate(sorted_cond, 1):
        print(f"  {i}. {basis_names[basis]:25s} → Средн. cond(A) = {avg_cond:.2e}")

    print()
    print("=" * 80)


# ============================================================================
# ЗАПУСК
# ============================================================================

if __name__ == "__main__":
    results = run_stage2_experiment()
    analyze_stage2_results(results)

    print("\n" + "=" * 80)
    print("СЛЕДУЮЩИЙ ШАГ: Этап 3 - Исследование сходимости (N = 3,5,7,10,15,20)")
    print("=" * 80)