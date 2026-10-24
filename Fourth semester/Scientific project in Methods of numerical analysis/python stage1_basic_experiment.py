#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ЭТАП 1: Базовый эксперимент
Сравнение 4 проекционных методов на уравнении Пуассона
N = 5, тригонометрический базис
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import legendre, chebyt
from scipy.linalg import solve
import time
import csv
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
    def trigonometric_deriv1(x, k):
        """Первая производная: φ'_k(x) = k·π·cos(k·π·x)"""
        return k * np.pi * np.cos(k * np.pi * x)

    @staticmethod
    def trigonometric_deriv2(x, k):
        """Вторая производная: φ''_k(x) = -(k·π)²·sin(k·π·x)"""
        return -(k * np.pi) ** 2 * np.sin(k * np.pi * x)

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
            # Численное дифференцирование для других базисов
            h = 1e-6
            phi_plus = BasisFunctions.get_basis(name, x + h, k)
            phi_minus = BasisFunctions.get_basis(name, x - h, k)
            phi_center = BasisFunctions.get_basis(name, x, k)
            return (phi_plus - 2 * phi_center + phi_minus) / (h ** 2)


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
    def poisson_bc():
        """Граничные условия: U(0) = 0, U(1) = 0"""
        return 0.0, 0.0


# ============================================================================
# ПРОЕКЦИОННЫЕ МЕТОДЫ
# ============================================================================

class ProjectionMethods:
    """Класс с реализацией 4 проекционных методов"""

    def __init__(self, n_funcs=5, basis_type='trig'):
        """
        Parameters:
        -----------
        n_funcs : int - количество базисных функций
        basis_type : str - 'trig', 'legendre', 'chebyshev'
        """
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
        return Phi

    def collocation(self, equation_f, x_points):
        """
        Метод коллокаций: R(x_i) = 0 в выбранных точках
        Для уравнения: -U''(x) = f(x)
        """
        start_time = time.perf_counter()

        n = self.n_funcs
        # Точки коллокации (внутренние точки)
        x_coll = np.linspace(0.1, 0.9, n)

        # Матрица вторых производных базисных функций
        Phi_dd = self._build_basis_matrix(x_coll, deriv_order=2)

        # Правая часть
        F = equation_f(x_coll)

        # Система: -Phi_dd @ C = F
        A = -Phi_dd
        B = F

        # Решаем СЛАУ
        try:
            self.coefficients = solve(A, B)
            self.matrix_A = A
            self.condition_number = np.linalg.cond(A)
        except np.linalg.LinAlgError:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        elapsed_time = (time.perf_counter() - start_time) * 1000
        return self.coefficients, elapsed_time

    def least_squares_integral(self, equation_f, x_points):
        """
        Интегральный метод наименьших квадратов: min ∫R²dx
        """
        start_time = time.perf_counter()

        n = self.n_funcs
        # Точки для интегрирования
        x_int = np.linspace(0, 1, 200)
        dx = x_int[1] - x_int[0]

        # Матрица вторых производных
        Phi_dd = self._build_basis_matrix(x_int, deriv_order=2)

        # Правая часть
        F = equation_f(x_int)

        # Нормальные уравнения: (Phi_dd^T @ Phi_dd) @ C = -Phi_dd^T @ F
        A = Phi_dd.T @ Phi_dd * dx
        B = -Phi_dd.T @ F * dx

        try:
            self.coefficients = solve(A, B)
            self.matrix_A = A
            self.condition_number = np.linalg.cond(A)
        except np.linalg.LinAlgError:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        elapsed_time = (time.perf_counter() - start_time) * 1000
        return self.coefficients, elapsed_time

    def galerkin_classical(self, equation_f, x_points):
        """
        Классический метод Галеркина: ∫R(x)·φ_i(x)dx = 0
        """
        start_time = time.perf_counter()

        n = self.n_funcs
        # Точки для интегрирования
        x_int = np.linspace(0, 1, 200)
        dx = x_int[1] - x_int[0]

        # Матрица вторых производных базисных функций
        Phi_dd = self._build_basis_matrix(x_int, deriv_order=2)

        # Матрица базисных функций
        Phi = self._build_basis_matrix(x_int, deriv_order=0)

        # Правая часть
        F = equation_f(x_int)

        # Формируем систему: ∫(-Phi_dd @ C - F) · Phi_i dx = 0
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
        except np.linalg.LinAlgError:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        elapsed_time = (time.perf_counter() - start_time) * 1000
        return self.coefficients, elapsed_time

    def galerkin_malyshev(self, equation_f, x_points):
        """
        Модифицированный метод Галеркина (Малышева): ∫R^(k)(x)dx = 0

        Для уравнения: -U''(x) = f(x)
        Невязка: R = -U_approx''(x) - f(x)

        Условия:
        k=0: ∫R dx = 0      → ∫(-U'' - f) dx = 0
        k=1: ∫R' dx = 0     → ∫(-U''' - f') dx = 0
        k=2: ∫R'' dx = 0    → ∫(-U'''' - f'') dx = 0
        ...
        """
        start_time = time.perf_counter()

        n = self.n_funcs
        # Точки для интегрирования
        x_int = np.linspace(0, 1, 200)
        dx = x_int[1] - x_int[0]

        # Правая часть и её производные (для Пуассона f = π²·sin(πx))
        F = equation_f(x_int)

        # Для уравнения Пуассона f(x) = π²·sin(πx)
        # f'(x) = π³·cos(πx)
        # f''(x) = -π⁴·sin(πx)
        # f'''(x) = -π⁵·cos(πx)
        # f''''(x) = π⁶·sin(πx)

        pi = np.pi
        F_derivs = []
        for k in range(n):
            if k % 2 == 0:
                # Чётные производные: sin
                sign = (-1) ** (k // 2)
                F_derivs.append(sign * (pi ** (k + 2)) * np.sin(pi * x_int))
            else:
                # Нечётные производные: cos
                sign = (-1) ** (k // 2)
                F_derivs.append(sign * (pi ** (k + 2)) * np.cos(pi * x_int))

        # Формируем систему уравнений
        A = np.zeros((n, n))
        B = np.zeros(n)

        for k in range(n):
            # k-е условие: ∫R^(k) dx = 0
            # R^(k) = -U^(k+2) - f^(k)

            # Получаем (k+2)-ю производную базисных функций
            deriv_order = k + 2

            # Для тригонометрического базиса φ_j = sin(j·π·x)
            # φ_j' = j·π·cos(j·π·x)
            # φ_j'' = -(j·π)²·sin(j·π·x)
            # φ_j''' = -(j·π)³·cos(j·π·x)
            # φ_j'''' = (j·π)⁴·sin(j·π·x)

            for j in range(1, n + 1):
                if deriv_order % 2 == 0:
                    # Чётная производная → sin
                    sign = (-1) ** (deriv_order // 2)
                    phi_deriv = sign * (j * pi) ** deriv_order * np.sin(j * pi * x_int)
                else:
                    # Нечётная производная → cos
                    sign = (-1) ** ((deriv_order - 1) // 2)
                    phi_deriv = sign * (j * pi) ** deriv_order * np.cos(j * pi * x_int)

                A[k, j - 1] = -np.sum(phi_deriv) * dx

            B[k] = np.sum(F_derivs[k]) * dx

        try:
            self.coefficients = solve(A, B)
            self.matrix_A = A
            self.condition_number = np.linalg.cond(A)
        except np.linalg.LinAlgError:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        elapsed_time = (time.perf_counter() - start_time) * 1000
        return self.coefficients, elapsed_time

    def get_solution(self, x_points):
        """Получить приближённое решение в точках"""
        if self.coefficients is None:
            raise ValueError("Сначала нужно решить уравнение!")

        Phi = self._build_basis_matrix(x_points, deriv_order=0)
        return Phi @ self.coefficients

    def get_residual(self, equation_f, x_points):
        """Получить невязку в точках"""
        if self.coefficients is None:
            raise ValueError("Сначала нужно решить уравнение!")

        Phi_dd = self._build_basis_matrix(x_points, deriv_order=2)
        F = equation_f(x_points)

        U_approx_dd = Phi_dd @ self.coefficients
        residual = -U_approx_dd - F

        return residual


# ============================================================================
# МЕТРИКИ И АНАЛИЗ
# ============================================================================

class Metrics:
    """Класс для расчёта метрик качества"""

    @staticmethod
    def max_error(u_exact, u_approx):
        """Максимальная погрешность"""
        return np.max(np.abs(u_exact - u_approx))

    @staticmethod
    def rms_error(u_exact, u_approx):
        """Среднеквадратичная погрешность"""
        return np.sqrt(np.mean((u_exact - u_approx) ** 2))

    @staticmethod
    def max_residual(residual):
        """Максимальная невязка"""
        return np.max(np.abs(residual))

    @staticmethod
    def relative_error(u_exact, u_approx):
        """Относительная погрешность в %"""
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
    def plot_stage1_results(results, save_path='results/stage1_comparison.png'):
        """
        Построить графики для Этапа 1
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        colors = {'collocation': 'blue', 'least_squares': 'green',
                  'galerkin': 'red', 'malyshev': 'orange'}
        markers = {'collocation': 'o', 'least_squares': 's',
                   'galerkin': '^', 'malyshev': 'd'}

        # 1. Сравнение решений
        ax = axes[0, 0]
        x = results[0]['x']
        u_exact = TestEquations.poisson_exact(x)
        ax.plot(x, u_exact, 'k--', linewidth=3, label='Точное решение', alpha=0.7)

        for res in results:
            ax.plot(x, res['u_approx'], colors[res['method']], linewidth=2,
                    marker=markers[res['method']], markersize=4, markevery=10,
                    label=f"{res['method_name']} (N={res['n_funcs']})")

        ax.set_xlabel('x', fontsize=12, fontweight='bold')
        ax.set_ylabel('U(x)', fontsize=12, fontweight='bold')
        ax.set_title('Сравнение приближённых решений с точным', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--')

        # 2. Погрешности
        ax = axes[0, 1]
        for res in results:
            if res['error'] is not None:
                ax.plot(x, res['error'], colors[res['method']], linewidth=2,
                        label=f"{res['method_name']}: max={res['max_error']:.2e}")

        ax.set_xlabel('x', fontsize=12, fontweight='bold')
        ax.set_ylabel('|U_exact - U_approx|', fontsize=12, fontweight='bold')
        ax.set_title('Погрешность решений', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--')

        # 3. Невязки
        ax = axes[1, 0]
        for res in results:
            ax.plot(x, res['residual'], colors[res['method']], linewidth=2,
                    label=f"{res['method_name']}: max={res['max_residual']:.2e}")

        ax.set_xlabel('x', fontsize=12, fontweight='bold')
        ax.set_ylabel('R(x)', fontsize=12, fontweight='bold')
        ax.set_title('Невязка уравнения', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)

        # 4. Таблица метрик
        ax = axes[1, 1]
        ax.axis('off')

        table_data = []
        headers = ['Метод', 'Max Error', 'RMS Error', 'Max Residual', 'Time (ms)', 'cond(A)']

        for res in results:
            row = [
                res['method_name'],
                f"{res['max_error']:.2e}",
                f"{res['rms_error']:.2e}",
                f"{res['max_residual']:.2e}",
                f"{res['time_ms']:.2f}",
                f"{res['condition_number']:.2f}"
            ]
            table_data.append(row)

        # Находим лучший метод по точности
        min_error_idx = np.argmin([res['max_error'] for res in results])

        table = ax.table(cellText=table_data, colLabels=headers,
                         loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.3, 1.8)

        # Подсветка лучшего метода
        for col in range(6):
            table[(min_error_idx + 1, col)].set_facecolor('#90EE90')  # Светло-зелёный

        ax.set_title('Метрики качества (N=5, тригонометрический базис)',
                     fontsize=14, fontweight='bold', pad=20)

        plt.suptitle('ЭТАП 1: Сравнение 4 проекционных методов\nУравнение Пуассона: -U\'\' = π²·sin(π·x), U(0)=U(1)=0',
                     fontsize=16, fontweight='bold', y=1.02)

        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show()

        print(f"✓ График сохранён: {save_path}")

    @staticmethod
    def save_results_to_csv(results, save_path='results/stage1_results.csv'):
        """Сохранить результаты в CSV"""
        with open(save_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')

            # Заголовок
            writer.writerow(['Метод', 'N', 'Базис', 'Max Error', 'RMS Error',
                             'Max Residual', 'Time (ms)', 'cond(A)', 'Отн. погрешность (%)'])

            # Данные
            for res in results:
                writer.writerow([
                    res['method_name'],
                    res['n_funcs'],
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
# ГЛАВНАЯ ФУНКЦИЯ ЭТАПА 1
# ============================================================================

def run_stage1_experiment():
    """
    Запустить Этап 1: Базовый эксперимент
    """
    print("=" * 80)
    print("ЭТАП 1: БАЗОВЫЙ ЭКСПЕРИМЕНТ")
    print("=" * 80)
    print(f"Дата начала: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Параметры эксперимента
    equation_name = 'Уравнение Пуассона'
    n_funcs = 5
    basis_type = 'trig'
    basis_name = 'Тригонометрический'

    print(f"Уравнение: {equation_name}")
    print(f"Число базисных функций (N): {n_funcs}")
    print(f"Тип базиса: {basis_name}")
    print()

    # Методы для сравнения
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

    for method_key, method_name in methods:
        print(f"\n[{method_name}]...")

        try:
            # Создаём решатель
            solver = ProjectionMethods(n_funcs=n_funcs, basis_type=basis_type)

            # Решаем уравнение
            method_map = {
                'collocation': solver.collocation,
                'least_squares': solver.least_squares_integral,
                'galerkin': solver.galerkin_classical,
                'malyshev': solver.galerkin_malyshev
            }

            coefficients, time_ms = method_map[method_key](f, x)

            # Получаем решение
            u_approx = solver.get_solution(x)

            # Получаем невязку
            residual = solver.get_residual(f, x)

            # Считаем метрики
            max_error = Metrics.max_error(u_exact, u_approx)
            rms_error = Metrics.rms_error(u_exact, u_approx)
            max_residual = Metrics.max_residual(residual)
            relative_error = Metrics.relative_error(u_exact, u_approx)

            # Сохраняем результаты
            results.append({
                'method': method_key,
                'method_name': method_name,
                'n_funcs': n_funcs,
                'basis_type': basis_type,
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

            print(f"  ✓ Max ошибка: {max_error:.2e}")
            print(f"  ✓ RMS ошибка: {rms_error:.2e}")
            print(f"  ✓ Max невязка: {max_residual:.2e}")
            print(f"  ✓ Время: {time_ms:.2f} мс")
            print(f"  ✓ cond(A): {solver.condition_number:.2f}")

        except Exception as e:
            print(f"  ✗ Ошибка: {e}")
            results.append({
                'method': method_key,
                'method_name': method_name,
                'n_funcs': n_funcs,
                'basis_type': basis_type,
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

    # Находим лучший метод по точности
    valid_results = [r for r in results if r['max_error'] != np.inf]
    if valid_results:
        best_method = min(valid_results, key=lambda x: x['max_error'])
        print(f"\n★ Лучший метод по точности: {best_method['method_name']}")
        print(f"  Max погрешность: {best_method['max_error']:.2e}")

        # Находим самый быстрый метод
        fastest_method = min(valid_results, key=lambda x: x['time_ms'])
        print(f"\n★ Самый быстрый метод: {fastest_method['method_name']}")
        print(f"  Время: {fastest_method['time_ms']:.2f} мс")

        # Находим метод с лучшей обусловленностью
        best_cond = min(valid_results, key=lambda x: x['condition_number'])
        print(f"\n★ Лучшая обусловленность: {best_cond['method_name']}")
        print(f"  cond(A): {best_cond['condition_number']:.2f}")

    print()
    print("-" * 80)
    print("СОХРАНЕНИЕ РЕЗУЛЬТАТОВ")
    print("-" * 80)

    # Создаём папку для результатов
    import os
    os.makedirs('results', exist_ok=True)

    # Сохраняем в CSV
    Visualization.save_results_to_csv(results, 'results/stage1_results.csv')

    # Строим графики
    Visualization.plot_stage1_results(results, 'results/stage1_comparison.png')

    print()
    print("=" * 80)
    print(f"ЭТАП 1 ЗАВЕРШЁН: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    return results


# ============================================================================
# АНАЛИЗ РЕЗУЛЬТАТОВ
# ============================================================================

def analyze_stage1_results(results):
    """
    Подробный анализ результатов Этапа 1
    """
    print("\n" + "=" * 80)
    print("ПОДРОБНЫЙ АНАЛИЗ РЕЗУЛЬТАТОВ ЭТАПА 1")
    print("=" * 80)

    valid_results = [r for r in results if r['max_error'] != np.inf]

    if len(valid_results) < 2:
        print("Недостаточно данных для анализа")
        return

    # 1. Сравнение точности
    print("\n1. СРАВНЕНИЕ ТОЧНОСТИ")
    print("-" * 80)

    sorted_by_error = sorted(valid_results, key=lambda x: x['max_error'])
    for i, res in enumerate(sorted_by_error, 1):
        print(f"  {i}. {res['method_name']:25s} → Max Error = {res['max_error']:.2e}")

    # 2. Сравнение времени
    print("\n2. СРАВНЕНИЕ ВЫЧИСЛИТЕЛЬНОЙ ЭФФЕКТИВНОСТИ")
    print("-" * 80)

    sorted_by_time = sorted(valid_results, key=lambda x: x['time_ms'])
    for i, res in enumerate(sorted_by_time, 1):
        print(f"  {i}. {res['method_name']:25s} → Time = {res['time_ms']:.2f} мс")

    # 3. Сравнение обусловленности
    print("\n3. СРАВНЕНИЕ УСТОЙЧИВОСТИ (число обусловленности)")
    print("-" * 80)

    sorted_by_cond = sorted(valid_results, key=lambda x: x['condition_number'])
    for i, res in enumerate(sorted_by_cond, 1):
        print(f"  {i}. {res['method_name']:25s} → cond(A) = {res['condition_number']:.2f}")

    # 4. Проверка гипотез
    print("\n4. ПРОВЕРКА ГИПОТЕЗ ЭТАПА 1")
    print("-" * 80)

    # Гипотеза H1: Метод Малышева точнее классического Галеркина
    malyshev = next((r for r in valid_results if r['method'] == 'malyshev'), None)
    galerkin = next((r for r in valid_results if r['method'] == 'galerkin'), None)

    if malyshev and galerkin:
        if malyshev['max_error'] < galerkin['max_error']:
            improvement = (galerkin['max_error'] - malyshev['max_error']) / galerkin['max_error'] * 100
            print(f"  ✓ H1: Метод Малышева точнее Галеркина на {improvement:.1f}%")
        else:
            print(f"  ✗ H1: Метод Малышева НЕ точнее Галеркина")

    # Гипотеза H2: Метод Малышева быстрее
    if malyshev and galerkin:
        if malyshev['time_ms'] < galerkin['time_ms']:
            improvement = (galerkin['time_ms'] - malyshev['time_ms']) / galerkin['time_ms'] * 100
            print(f"  ✓ H2: Метод Малышева быстрее Галеркина на {improvement:.1f}%")
        else:
            print(f"  ✗ H2: Метод Малышева НЕ быстрее Галеркина")

    print()
    print("=" * 80)


# ============================================================================
# ЗАПУСК
# ============================================================================

if __name__ == "__main__":
    # Запускаем эксперимент
    results = run_stage1_experiment()

    # Анализируем результаты
    analyze_stage1_results(results)

    print("\n" + "=" * 80)
    print("СЛЕДУЮЩИЙ ШАГ: Этап 2 - Сравнение базисов (TRIG, LEG, CHEB)")
    print("=" * 80)