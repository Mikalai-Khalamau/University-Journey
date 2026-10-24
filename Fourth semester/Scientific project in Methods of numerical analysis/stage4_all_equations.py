#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ЭТАП 4: Тестирование на всех уравнениях
Сравнение 4 методов на 6 различных типах дифференциальных уравнений
N = 5 (фиксировано), тригонометрический базис
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import legendre, chebyt
from scipy.linalg import solve
import time
import csv
import os
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')


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
        """Первая производная"""
        return k * np.pi * np.cos(k * np.pi * x)

    @staticmethod
    def trigonometric_deriv2(x, k):
        """Вторая производная"""
        return -(k * np.pi) ** 2 * np.sin(k * np.pi * x)

    @staticmethod
    def trigonometric_deriv3(x, k):
        """Третья производная"""
        return -(k * np.pi) ** 3 * np.cos(k * np.pi * x)

    @staticmethod
    def trigonometric_deriv4(x, k):
        """Четвёртая производная"""
        return (k * np.pi) ** 4 * np.sin(k * np.pi * x)

    @staticmethod
    def trigonometric_deriv_k(x, k, deriv_order):
        """Производная порядка deriv_order"""
        pi = np.pi
        mod = deriv_order % 4
        if mod == 0:
            return (k * pi) ** deriv_order * np.sin(k * pi * x)
        elif mod == 1:
            return (k * pi) ** deriv_order * np.cos(k * pi * x)
        elif mod == 2:
            return -(k * pi) ** deriv_order * np.sin(k * pi * x)
        else:
            return -(k * pi) ** deriv_order * np.cos(k * pi * x)

    @staticmethod
    def get_basis(name, x, k):
        """Получить базисную функцию"""
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
    def poisson(x):
        """Уравнение Пуассона: -U'' = π²·sin(π·x)"""
        return np.pi ** 2 * np.sin(np.pi * x)

    @staticmethod
    def poisson_exact(x):
        return np.sin(np.pi * x)

    @staticmethod
    def poisson_bc():
        return {'type': 'dirichlet', 'u0': 0.0, 'u1': 0.0}

    @staticmethod
    def oscillating(x):
        """Осциллирующее ДУ: -U'' = 100·sin(10·x)"""
        return 100 * np.sin(10 * x)

    @staticmethod
    def oscillating_exact(x):
        return np.sin(10 * x)

    @staticmethod
    def oscillating_bc():
        return {'type': 'dirichlet', 'u0': 0.0, 'u1': np.sin(10)}

    @staticmethod
    def boundary_layer(x):
        """Пограничный слой: -0.01·U'' + U' = 1"""
        return np.ones_like(x)

    @staticmethod
    def boundary_layer_exact(x):
        return x - (np.exp(100 * x) - 1) / (np.exp(100) - 1)

    @staticmethod
    def boundary_layer_bc():
        return {'type': 'dirichlet', 'u0': 0.0, 'u1': 0.0}

    @staticmethod
    def asymmetric(x):
        """Несимметричное ЛДУ: -U'' + 5·U' + U = exp(x)"""
        return np.exp(x)

    @staticmethod
    def asymmetric_exact(x):
        """Приближённое точное решение"""
        return 0.1 * np.exp(x) * np.sin(np.pi * x)

    @staticmethod
    def asymmetric_bc():
        return {'type': 'dirichlet', 'u0': 0.0, 'u1': 0.0}

    @staticmethod
    def sturm_liouville(x):
        """Штурм-Лиувилль: -(1+x)·U'' + U = x"""
        return x

    @staticmethod
    def sturm_liouville_exact(x):
        return x * (1 - x) * 0.5

    @staticmethod
    def sturm_liouville_bc():
        return {'type': 'dirichlet', 'u0': 0.0, 'u1': 0.0}

    @staticmethod
    def fourth_order(x):
        """4-й порядок: U'''' = sin(π·x)"""
        return np.sin(np.pi * x)

    @staticmethod
    def fourth_order_exact(x):
        return np.sin(np.pi * x) / (np.pi ** 4)

    @staticmethod
    def fourth_order_bc():
        return {'type': 'clamped', 'u0': 0.0, 'u1': 0.0, 'up0': 0.0, 'up1': 0.0}

    @staticmethod
    def get_equation(name):
        """Получить уравнение по имени"""
        equations = {
            'poisson': {
                'f': TestEquations.poisson,
                'exact': TestEquations.poisson_exact,
                'bc': TestEquations.poisson_bc,
                'order': 2,
                'name': 'Пуассона'
            },
            'oscillating': {
                'f': TestEquations.oscillating,
                'exact': TestEquations.oscillating_exact,
                'bc': TestEquations.oscillating_bc,
                'order': 2,
                'name': 'Осциллирующее'
            },
            'boundary_layer': {
                'f': TestEquations.boundary_layer,
                'exact': TestEquations.boundary_layer_exact,
                'bc': TestEquations.boundary_layer_bc,
                'order': 2,
                'name': 'Пограничный слой'
            },
            'asymmetric': {
                'f': TestEquations.asymmetric,
                'exact': TestEquations.asymmetric_exact,
                'bc': TestEquations.asymmetric_bc,
                'order': 2,
                'name': 'Несимметричное'
            },
            'sturm_liouville': {
                'f': TestEquations.sturm_liouville,
                'exact': TestEquations.sturm_liouville_exact,
                'bc': TestEquations.sturm_liouville_bc,
                'order': 2,
                'name': 'Штурм-Лиувилль'
            },
            'fourth_order': {
                'f': TestEquations.fourth_order,
                'exact': TestEquations.fourth_order_exact,
                'bc': TestEquations.fourth_order_bc,
                'order': 4,
                'name': '4-й порядок'
            }
        }
        return equations.get(name)


# ============================================================================
# ПРОЕКЦИОННЫЕ МЕТОДЫ
# ============================================================================

class ProjectionMethods:
    """Класс с реализацией 4 проекционных методов"""

    def __init__(self, n_funcs=5, basis_type='trig', equation_order=2):
        self.n_funcs = n_funcs
        self.basis_type = basis_type
        self.order = equation_order
        self.coefficients = None
        self.matrix_A = None
        self.condition_number = None

    def _build_basis_matrix(self, x_points, deriv_order=0):
        """Построить матрицу базисных функций или их производных"""
        n = len(x_points)
        Phi = np.zeros((n, self.n_funcs))
        for k in range(1, self.n_funcs + 1):
            Phi[:, k - 1] = BasisFunctions.get_basis_deriv_k(
                self.basis_type, x_points, k, deriv_order
            )
        return Phi

    def collocation(self, equation_f, bc, x_points):
        """Метод коллокаций: R(x_i) = 0"""
        start_time = time.perf_counter()

        n = self.n_funcs
        x_coll = np.linspace(0.1, 0.9, n)

        if self.order == 2:
            Phi_dd = self._build_basis_matrix(x_coll, deriv_order=2)
            F = equation_f(x_coll)
            A = -Phi_dd
            B = F
        else:  # 4th order
            Phi_4 = self._build_basis_matrix(x_coll, deriv_order=4)
            F = equation_f(x_coll)
            A = Phi_4
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

    def least_squares_integral(self, equation_f, bc, x_points):
        """Интегральный МНК: min ∫R²dx"""
        start_time = time.perf_counter()

        n = self.n_funcs
        x_int = np.linspace(0, 1, 200)
        dx = x_int[1] - x_int[0]

        if self.order == 2:
            Phi_dd = self._build_basis_matrix(x_int, deriv_order=2)
            F = equation_f(x_int)
            A = Phi_dd.T @ Phi_dd * dx
            B = -Phi_dd.T @ F * dx
        else:  # 4th order
            Phi_4 = self._build_basis_matrix(x_int, deriv_order=4)
            F = equation_f(x_int)
            A = Phi_4.T @ Phi_4 * dx
            B = Phi_4.T @ F * dx

        try:
            self.coefficients = solve(A, B)
            self.matrix_A = A
            self.condition_number = np.linalg.cond(A)
        except:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        elapsed_time = (time.perf_counter() - start_time) * 1000
        return self.coefficients, elapsed_time

    def galerkin_classical(self, equation_f, bc, x_points):
        """Классический метод Галеркина: ∫R·φ_i dx = 0"""
        start_time = time.perf_counter()

        n = self.n_funcs
        x_int = np.linspace(0, 1, 200)
        dx = x_int[1] - x_int[0]

        if self.order == 2:
            Phi_dd = self._build_basis_matrix(x_int, deriv_order=2)
            Phi = self._build_basis_matrix(x_int, deriv_order=0)
            F = equation_f(x_int)

            A = np.zeros((n, n))
            B = np.zeros(n)

            for i in range(n):
                for j in range(n):
                    A[i, j] = np.sum(Phi[:, i] * Phi_dd[:, j]) * dx
                B[i] = -np.sum(Phi[:, i] * F) * dx
        else:  # 4th order
            Phi_4 = self._build_basis_matrix(x_int, deriv_order=4)
            Phi = self._build_basis_matrix(x_int, deriv_order=0)
            F = equation_f(x_int)

            A = np.zeros((n, n))
            B = np.zeros(n)

            for i in range(n):
                for j in range(n):
                    A[i, j] = np.sum(Phi[:, i] * Phi_4[:, j]) * dx
                B[i] = np.sum(Phi[:, i] * F) * dx

        try:
            self.coefficients = solve(A, B)
            self.matrix_A = A
            self.condition_number = np.linalg.cond(A)
        except:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        elapsed_time = (time.perf_counter() - start_time) * 1000
        return self.coefficients, elapsed_time

    def galerkin_malyshev(self, equation_f, bc, x_points):
        """Модифицированный метод Галеркина (Малышева): ∫R^(k)(x)dx = 0"""
        start_time = time.perf_counter()

        n = self.n_funcs
        x_int = np.linspace(0, 1, 200)
        dx = x_int[1] - x_int[0]

        F = equation_f(x_int)
        pi = np.pi

        A = np.zeros((n, n))
        B = np.zeros(n)

        for k in range(n):
            if self.order == 2:
                deriv_order = k + 2

                for j in range(1, n + 1):
                    if self.basis_type == 'trig':
                        phi_deriv = BasisFunctions.trigonometric_deriv_k(x_int, j, deriv_order)
                    else:
                        phi_deriv = BasisFunctions.get_basis_deriv_k(
                            self.basis_type, x_int, j, deriv_order
                        )
                    A[k, j - 1] = -np.sum(phi_deriv) * dx

                # Производные правой части
                if k % 2 == 0:
                    sign = (-1) ** (k // 2)
                    F_deriv = sign * (pi ** (2 + k)) * np.sin(pi * x_int)
                else:
                    sign = (-1) ** (k // 2)
                    F_deriv = sign * (pi ** (2 + k)) * np.cos(pi * x_int)
                B[k] = np.sum(F_deriv) * dx
            else:  # 4th order
                deriv_order = k + 4

                for j in range(1, n + 1):
                    if self.basis_type == 'trig':
                        phi_deriv = BasisFunctions.trigonometric_deriv_k(x_int, j, deriv_order)
                    else:
                        phi_deriv = BasisFunctions.get_basis_deriv_k(
                            self.basis_type, x_int, j, deriv_order
                        )
                    A[k, j - 1] = np.sum(phi_deriv) * dx

                # Производные правой части для 4-го порядка
                if k % 2 == 0:
                    F_deriv = (pi ** k) * np.sin(pi * x_int)
                else:
                    F_deriv = (pi ** k) * np.cos(pi * x_int)
                B[k] = np.sum(F_deriv) * dx

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

        if self.order == 2:
            Phi_dd = self._build_basis_matrix(x_points, deriv_order=2)
            U_approx_dd = Phi_dd @ self.coefficients
            F = equation_f(x_points)
            return -U_approx_dd - F
        else:  # 4th order
            Phi_4 = self._build_basis_matrix(x_points, deriv_order=4)
            U_approx_4 = Phi_4 @ self.coefficients
            F = equation_f(x_points)
            return U_approx_4 - F


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
    def plot_equation_comparison(results_by_equation, save_path='results/stage4_equations_comparison.png'):
        """Построить графики сравнения для всех уравнений"""
        fig, axes = plt.subplots(3, 2, figsize=(18, 15))
        axes = axes.flatten()

        method_colors = {'collocation': 'blue', 'least_squares': 'green',
                         'galerkin': 'red', 'malyshev': 'orange'}
        method_names = {'collocation': 'Коллокация', 'least_squares': 'МНК',
                        'galerkin': 'Галеркин', 'malyshev': 'Малышев'}

        equation_list = ['poisson', 'oscillating', 'boundary_layer',
                         'asymmetric', 'sturm_liouville', 'fourth_order']

        for idx, eq_name in enumerate(equation_list):
            ax = axes[idx]
            results = results_by_equation.get(eq_name, [])

            # Точное решение
            if results:
                x = results[0]['x']
                u_exact = results[0]['u_exact']
                ax.plot(x, u_exact, 'k--', linewidth=2, label='Точное', alpha=0.7)

            # Приближённые решения
            for res in results:
                ax.plot(x, res['u_approx'], method_colors[res['method']],
                        linewidth=1.5, alpha=0.8,
                        label=f"{method_names[res['method']]} ({res['max_error']:.1e})")

            eq_info = TestEquations.get_equation(eq_name)
            ax.set_xlabel('x', fontsize=11, fontweight='bold')
            ax.set_ylabel('U(x)', fontsize=11, fontweight='bold')
            ax.set_title(f'{eq_info["name"]} (N=5)', fontsize=12, fontweight='bold')
            ax.legend(fontsize=8, loc='best')
            ax.grid(True, alpha=0.3, linestyle='--')

        plt.suptitle('ЭТАП 4: Сравнение методов на 6 уравнениях\nN=5, тригонометрический базис',
                     fontsize=16, fontweight='bold', y=1.02)

        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show()

        print(f"✓ График сохранён: {save_path}")

    @staticmethod
    def plot_heatmap(results_by_equation, save_path='results/stage4_heatmap.png'):
        """Построить тепловую карту погрешностей"""
        fig, ax = plt.subplots(figsize=(12, 8))

        methods = ['collocation', 'least_squares', 'galerkin', 'malyshev']
        method_labels = ['Коллокация', 'МНК', 'Галеркин', 'Малышев']
        equations = ['poisson', 'oscillating', 'boundary_layer',
                     'asymmetric', 'sturm_liouville', 'fourth_order']
        eq_labels = ['Пуассона', 'Осцилл.', 'Погр.слой', 'Несимм.', 'Штурм', '4-й пор.']

        # Матрица погрешностей
        error_matrix = np.zeros((len(equations), len(methods)))

        for i, eq in enumerate(equations):
            for j, method in enumerate(methods):
                for res in results_by_equation.get(eq, []):
                    if res['method'] == method:
                        error_matrix[i, j] = res['max_error'] if res['max_error'] != np.inf else 1e10
                        break

        # Тепловая карта
        im = ax.imshow(error_matrix, cmap='RdYlGn_r', aspect='auto')

        # Подписи
        ax.set_xticks(np.arange(len(methods)))
        ax.set_yticks(np.arange(len(equations)))
        ax.set_xticklabels(method_labels, fontsize=11)
        ax.set_yticklabels(eq_labels, fontsize=11)

        # Поворот подписей
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

        # Значения в ячейках
        for i in range(len(equations)):
            for j in range(len(methods)):
                val = error_matrix[i, j]
                if val > 0:
                    text = f"{val:.1e}" if val < 1 else f"{val:.1f}"
                    ax.text(j, i, text, ha="center", va="center",
                            color="white" if val > np.max(error_matrix) / 2 else "black",
                            fontsize=9)

        ax.set_xlabel('Метод', fontsize=12, fontweight='bold')
        ax.set_ylabel('Уравнение', fontsize=12, fontweight='bold')
        ax.set_title('Тепловая карта максимальной погрешности (N=5)',
                     fontsize=14, fontweight='bold')

        # Цветовая шкала
        cbar = ax.figure.colorbar(im, ax=ax)
        cbar.ax.set_ylabel('Max ошибка', rotation=-90, va="bottom", fontsize=11)

        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show()

        print(f"✓ Тепловая карта сохранена: {save_path}")

    @staticmethod
    def save_results_to_csv(results_by_equation, save_path='results/stage4_all_equations.csv'):
        """Сохранить результаты в CSV"""
        os.makedirs('results', exist_ok=True)

        with open(save_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')

            writer.writerow(['Уравнение', 'Метод', 'N', 'Базис', 'Порядок',
                             'Max Error', 'RMS Error', 'Max Residual',
                             'Time (ms)', 'cond(A)', 'Отн. погрешность (%)'])

            for eq_name, results in results_by_equation.items():
                for res in results:
                    writer.writerow([
                        eq_name,
                        res['method_name'],
                        res['n_funcs'],
                        res['basis_type'],
                        res['equation_order'],
                        f"{res['max_error']:.6e}",
                        f"{res['rms_error']:.6e}",
                        f"{res['max_residual']:.6e}",
                        f"{res['time_ms']:.4f}",
                        f"{res['condition_number']:.4f}",
                        f"{res['relative_error']:.4f}"
                    ])

        print(f"✓ Результаты сохранены: {save_path}")


# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ ЭТАПА 4
# ============================================================================

def run_stage4_experiment():
    """Запустить Этап 4: Тестирование на всех уравнениях"""
    print("=" * 80)
    print("ЭТАП 4: ТЕСТИРОВАНИЕ НА ВСЕХ УРАВНЕНИЯХ")
    print("=" * 80)
    print(f"Дата начала: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Параметры эксперимента
    n_funcs = 5
    basis_type = 'trig'

    equations = [
        'poisson', 'oscillating', 'boundary_layer',
        'asymmetric', 'sturm_liouville', 'fourth_order'
    ]

    methods = [
        ('collocation', 'Коллокация'),
        ('least_squares', 'МНК интегральный'),
        ('galerkin', 'Галеркин классический'),
        ('malyshev', 'Галеркин Малышева')
    ]

    # Сетка для вычислений
    x = np.linspace(0, 1, 200)

    results_by_equation = {}

    print("-" * 80)
    print("ВЫПОЛНЕНИЕ РАСЧЁТОВ")
    print("-" * 80)

    for eq_name in equations:
        print(f"\n{'=' * 60}")
        eq_info = TestEquations.get_equation(eq_name)
        print(f"УРАВНЕНИЕ: {eq_info['name']} (порядок {eq_info['order']})")
        print(f"{'=' * 60}")

        results_by_equation[eq_name] = []

        f = eq_info['f']
        exact = eq_info['exact']
        bc = eq_info['bc']()

        for method_key, method_name in methods:
            print(f"\n  [{method_name}]...")

            try:
                solver = ProjectionMethods(
                    n_funcs=n_funcs,
                    basis_type=basis_type,
                    equation_order=eq_info['order']
                )

                method_map = {
                    'collocation': solver.collocation,
                    'least_squares': solver.least_squares_integral,
                    'galerkin': solver.galerkin_classical,
                    'malyshev': solver.galerkin_malyshev
                }

                coefficients, time_ms = method_map[method_key](f, bc, x)
                u_approx = solver.get_solution(x)
                residual = solver.get_residual(f, x)

                u_exact = exact(x)
                max_error = Metrics.max_error(u_exact, u_approx)
                rms_error = Metrics.rms_error(u_exact, u_approx)
                max_residual = Metrics.max_residual(residual)
                relative_error = Metrics.relative_error(u_exact, u_approx)

                results_by_equation[eq_name].append({
                    'method': method_key,
                    'method_name': method_name,
                    'basis_type': basis_type,
                    'n_funcs': n_funcs,
                    'equation_order': eq_info['order'],
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
                results_by_equation[eq_name].append({
                    'method': method_key,
                    'method_name': method_name,
                    'basis_type': basis_type,
                    'n_funcs': n_funcs,
                    'equation_order': eq_info['order'],
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

    # Анализ для каждого уравнения
    for eq_name in equations:
        eq_info = TestEquations.get_equation(eq_name)
        results = results_by_equation[eq_name]
        valid_results = [r for r in results if r['max_error'] != np.inf]

        if valid_results:
            best = min(valid_results, key=lambda x: x['max_error'])
            print(f"\n★ Лучший метод для '{eq_info['name']}': {best['method_name']}")
            print(f"  Max погрешность: {best['max_error']:.2e}")

    print()
    print("-" * 80)
    print("СОХРАНЕНИЕ РЕЗУЛЬТАТОВ")
    print("-" * 80)

    os.makedirs('results', exist_ok=True)
    Visualization.save_results_to_csv(results_by_equation, 'results/stage4_all_equations.csv')
    Visualization.plot_equation_comparison(results_by_equation, 'results/stage4_equations_comparison.png')
    Visualization.plot_heatmap(results_by_equation, 'results/stage4_heatmap.png')

    print()
    print("=" * 80)
    print(f"ЭТАП 4 ЗАВЕРШЁН: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    return results_by_equation


# ============================================================================
# АНАЛИЗ РЕЗУЛЬТАТОВ
# ============================================================================

def analyze_stage4_results(results_by_equation):
    """Подробный анализ результатов Этапа 4"""
    print("\n" + "=" * 80)
    print("ПОДРОБНЫЙ АНАЛИЗ РЕЗУЛЬТАТОВ ЭТАПА 4")
    print("=" * 80)

    methods = ['collocation', 'least_squares', 'galerkin', 'malyshev']
    method_names = {'collocation': 'Коллокация', 'least_squares': 'МНК',
                    'galerkin': 'Галеркин', 'malyshev': 'Малышев'}

    equations = ['poisson', 'oscillating', 'boundary_layer',
                 'asymmetric', 'sturm_liouville', 'fourth_order']

    # 1. Сводная таблица погрешностей
    print("\n1. СВОДНАЯ ТАБЛИЦА ПОГРЕШНОСТЕЙ (Max ошибка)")
    print("-" * 80)

    header = f"{'Уравнение':>15}"
    for method in methods:
        header += f"│{method_names[method]:>18}"
    print(header)
    print("-" * 80)

    for eq in equations:
        eq_info = TestEquations.get_equation(eq)
        row = f"{eq_info['name']:>15}"
        for method in methods:
            for res in results_by_equation.get(eq, []):
                if res['method'] == method:
                    if res['max_error'] != np.inf:
                        row += f"│{res['max_error']:>18.2e}"
                    else:
                        row += f"│{'∞':>18}"
                    break
        print(row)

    # 2. Лучший метод для каждого уравнения
    print("\n2. ЛУЧШИЙ МЕТОД ДЛЯ КАЖДОГО УРАВНЕНИЯ")
    print("-" * 80)

    for eq in equations:
        eq_info = TestEquations.get_equation(eq)
        results = results_by_equation.get(eq, [])
        valid_results = [r for r in results if r['max_error'] != np.inf]

        if valid_results:
            best = min(valid_results, key=lambda x: x['max_error'])
            print(f"  {eq_info['name']:15s} → {best['method_name']:20s} (err={best['max_error']:.2e})")

    # 3. Средние метрики по всем уравнениям
    print("\n3. СРЕДНИЕ МЕТРИКИ ПО ВСЕМ УРАВНЕНИЯМ")
    print("-" * 80)

    for method in methods:
        errors = []
        times = []
        conds = []

        for eq in equations:
            for res in results_by_equation.get(eq, []):
                if res['method'] == method:
                    if res['max_error'] != np.inf:
                        errors.append(res['max_error'])
                        times.append(res['time_ms'])
                        if res['condition_number'] != np.inf:
                            conds.append(res['condition_number'])
                    break

        if errors:
            avg_error = np.mean(errors)
            avg_time = np.mean(times)
            avg_cond = np.mean(conds) if conds else np.inf
            print(
                f"  {method_names[method]:20s} → Avg Error: {avg_error:.2e}, Time: {avg_time:.2f} мс, cond: {avg_cond:.2e}")

    print()
    print("=" * 80)


# ============================================================================
# ЗАПУСК
# ============================================================================

if __name__ == "__main__":
    results = run_stage4_experiment()
    analyze_stage4_results(results)

    print("\n" + "=" * 80)
    print("СЛЕДУЮЩИЙ ШАГ: Этап 5 - Вычислительная эффективность (время, cond(A))")
    print("=" * 80)