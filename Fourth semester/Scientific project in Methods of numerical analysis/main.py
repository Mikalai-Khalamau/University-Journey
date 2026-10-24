#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
СРАВНИТЕЛЬНЫЙ АНАЛИЗ ПРОЕКЦИОННЫХ МЕТОДОВ РЕШЕНИЯ КРАЕВЫХ ЗАДАЧ
Научный проект МЧА | БГУИР + T-Academy
Версия: 2.0 (ИСПРАВЛЕННАЯ)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve
from scipy.special import legendre, chebyt
import time
import csv
import os
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')


# ============================================================================
# ЧАСТЬ 1: БАЗИСНЫЕ ФУНКЦИИ
# ============================================================================

class BasisFunctions:
    """Базисные функции для проекционных методов"""

    @staticmethod
    def polynomial(x, k):
        """Степенные полиномы: φ_k(x) = x^k * (1-x)"""
        return (x ** k) * (1 - x)

    @staticmethod
    def polynomial_deriv1(x, k):
        """Первая производная"""
        if k == 0:
            return -np.ones_like(x)
        return k * (x ** (k - 1)) * (1 - x) - (x ** k)

    @staticmethod
    def polynomial_deriv2(x, k):
        """Вторая производная"""
        if k == 0:
            return np.zeros_like(x)
        if k == 1:
            return -2 * np.ones_like(x)
        return k * (k - 1) * (x ** (k - 2)) * (1 - x) - 2 * k * (x ** (k - 1))

    @staticmethod
    def legendre(x, k):
        """Полиномы Лежандра: φ_k(x) = x(1-x) * P_k(2x-1)"""
        P_k = legendre(k)
        return x * (1 - x) * P_k(2 * x - 1)

    @staticmethod
    def legendre_deriv2(x, k):
        """Вторая производная Лежандра (аналитически)"""
        h = 1e-7
        phi_pp = BasisFunctions.legendre(x + h, k)
        phi_pm = BasisFunctions.legendre(x - h, k)
        phi_c = BasisFunctions.legendre(x, k)
        return (phi_pp - 2 * phi_c + phi_pm) / (h ** 2)

    @staticmethod
    def chebyshev(x, k):
        """Полиномы Чебышева: φ_k(x) = x(1-x) * T_k(2x-1)"""
        T_k = chebyt(k)
        return x * (1 - x) * T_k(2 * x - 1)

    @staticmethod
    def chebyshev_deriv2(x, k):
        """Вторая производная Чебышева"""
        h = 1e-7
        phi_pp = BasisFunctions.chebyshev(x + h, k)
        phi_pm = BasisFunctions.chebyshev(x - h, k)
        phi_c = BasisFunctions.chebyshev(x, k)
        return (phi_pp - 2 * phi_c + phi_pm) / (h ** 2)

    @staticmethod
    def trigonometric(x, k):
        """Тригонометрические: φ_k(x) = sin(k * π * x)"""
        return np.sin(k * np.pi * x)

    @staticmethod
    def trigonometric_deriv2(x, k):
        """Вторая производная тригонометрических"""
        return -(k * np.pi) ** 2 * np.sin(k * np.pi * x)

    @staticmethod
    def get_basis(name, x, k, deriv=0):
        """Получить базисную функцию или производную"""
        if name == 'polynomial':
            if deriv == 0:
                return BasisFunctions.polynomial(x, k)
            elif deriv == 1:
                return BasisFunctions.polynomial_deriv1(x, k)
            elif deriv == 2:
                return BasisFunctions.polynomial_deriv2(x, k)
        elif name == 'legendre':
            if deriv == 0:
                return BasisFunctions.legendre(x, k)
            elif deriv == 2:
                return BasisFunctions.legendre_deriv2(x, k)
        elif name == 'chebyshev':
            if deriv == 0:
                return BasisFunctions.chebyshev(x, k)
            elif deriv == 2:
                return BasisFunctions.chebyshev_deriv2(x, k)
        elif name == 'trigonometric':
            if deriv == 0:
                return BasisFunctions.trigonometric(x, k)
            elif deriv == 2:
                return BasisFunctions.trigonometric_deriv2(x, k)
        return np.zeros_like(x)


# ============================================================================
# ЧАСТЬ 2: ТЕСТОВЫЕ УРАВНЕНИЯ (ИСПРАВЛЕННЫЕ)
# ============================================================================

class TestEquations:
    """Тестовые уравнения с известными точными решениями"""

    @staticmethod
    def poisson(x):
        """Уравнение Пуассона: -U'' = 2"""
        return 2 * np.ones_like(x)

    @staticmethod
    def poisson_exact(x):
        """Точное решение: U(x) = x - x²"""
        return x - x ** 2

    @staticmethod
    def poisson_with_sine(x):
        """-U'' = π²·sin(π·x)"""
        return (np.pi ** 2) * np.sin(np.pi * x)

    @staticmethod
    def poisson_with_sine_exact(x):
        """Точное решение: U(x) = sin(π·x)"""
        return np.sin(np.pi * x)

    @staticmethod
    def oscillating(x):
        """Осциллирующее: -U'' = 100·sin(10·x)"""
        return 100 * np.sin(10 * x)

    @staticmethod
    def oscillating_exact(x):
        """Точное решение: U(x) = sin(10·x)"""
        return np.sin(10 * x)

    @staticmethod
    def boundary_layer(x):
        """Пограничный слой: -0.01·U'' + U' = 1"""
        return np.ones_like(x)

    @staticmethod
    def boundary_layer_exact(x):
        """Точное решение"""
        return x - (np.exp(100 * x) - 1) / (np.exp(100) - 1)

    @staticmethod
    def asymmetric(x):
        """Несимметричное: -U'' + 5·U' + U = exp(x)"""
        return np.exp(x)

    @staticmethod
    def asymmetric_exact(x):
        """Приближённое точное решение"""
        return 0.1 * np.exp(x) * np.sin(np.pi * x)

    @staticmethod
    def sturm_liouville(x):
        """Штурм-Лиувилль: -(1+x)·U'' + U = x"""
        return x

    @staticmethod
    def sturm_liouville_exact(x):
        """Приближённое решение"""
        return 0.5 * x * (1 - x)

    @staticmethod
    def get_equation(name):
        """Получить уравнение по имени"""
        equations = {
            'poisson': {
                'f': TestEquations.poisson,
                'exact': TestEquations.poisson_exact,
                'name': 'Пуассона (полином)',
                'order': 2,
                'has_first_deriv': False,
                'has_variable_coef': False
            },
            'poisson_sine': {
                'f': TestEquations.poisson_with_sine,
                'exact': TestEquations.poisson_with_sine_exact,
                'name': 'Пуассона (тригонометрия)',
                'order': 2,
                'has_first_deriv': False,
                'has_variable_coef': False
            },
            'oscillating': {
                'f': TestEquations.oscillating,
                'exact': TestEquations.oscillating_exact,
                'name': 'Осциллирующее',
                'order': 2,
                'has_first_deriv': False,
                'has_variable_coef': False
            },
            'boundary_layer': {
                'f': TestEquations.boundary_layer,
                'exact': TestEquations.boundary_layer_exact,
                'name': 'Пограничный слой',
                'order': 2,
                'has_first_deriv': True,
                'has_variable_coef': False
            },
            'asymmetric': {
                'f': TestEquations.asymmetric,
                'exact': TestEquations.asymmetric_exact,
                'name': 'Несимметричное',
                'order': 2,
                'has_first_deriv': True,
                'has_variable_coef': False
            },
            'sturm_liouville': {
                'f': TestEquations.sturm_liouville,
                'exact': TestEquations.sturm_liouville_exact,
                'name': 'Штурм-Лиувилль',
                'order': 2,
                'has_first_deriv': False,
                'has_variable_coef': True
            }
        }
        return equations.get(name)


# ============================================================================
# ЧАСТЬ 3: ПРОЕКЦИОННЫЕ МЕТОДЫ (ИСПРАВЛЕННЫЕ)
# ============================================================================

class ProjectionMethods:
    """Проекционные методы решения краевых задач"""

    def __init__(self, n_funcs=5, basis_type='polynomial'):
        self.n_funcs = n_funcs
        self.basis_type = basis_type
        self.coefficients = None
        self.condition_number = None
        self.matrix_A = None

    def _build_basis_matrix(self, x_points, deriv=0):
        """Построить матрицу базисных функций"""
        n = len(x_points)
        Phi = np.zeros((n, self.n_funcs))
        for k in range(1, self.n_funcs + 1):
            Phi[:, k - 1] = BasisFunctions.get_basis(
                self.basis_type, x_points, k, deriv=deriv
            )
        return Phi

    def collocation(self, equation_f, x_points, has_first_deriv=False,
                    variable_coef=None):
        """
        Метод коллокаций: R(x_i) = 0
        """
        start = time.perf_counter()
        n = self.n_funcs

        # Точки коллокации (чебышевские узлы для лучшей устойчивости)
        x_coll = np.array([(1 - np.cos((2 * i - 1) * np.pi / (2 * n))) / 2
                           for i in range(1, n + 1)])

        Phi_dd = self._build_basis_matrix(x_coll, deriv=2)
        Phi = self._build_basis_matrix(x_coll, deriv=0)
        F = equation_f(x_coll)

        # Формируем матрицу системы
        if has_first_deriv:
            Phi_d = self._build_basis_matrix(x_coll, deriv=1)
            if variable_coef is not None:
                # -(1+x)·U'' + U = f
                coef = 1 + x_coll
                A = -coef[:, np.newaxis] * Phi_dd + Phi
            else:
                # -U'' + 5·U' + U = f
                A = -Phi_dd + 5 * Phi_d + Phi
        else:
            # -U'' + U = f или -U'' = f
            A = -Phi_dd + Phi

        B = F

        try:
            self.coefficients = solve(A, B)
            self.condition_number = np.linalg.cond(A)
            self.matrix_A = A
        except:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        elapsed = (time.perf_counter() - start) * 1000
        return self.coefficients, elapsed

    def least_squares(self, equation_f, x_points, has_first_deriv=False,
                      variable_coef=None):
        """
        Интегральный МНК: min ∫R²dx
        """
        start = time.perf_counter()
        n = self.n_funcs

        x_int = np.linspace(0, 1, 300)
        dx = x_int[1] - x_int[0]

        Phi_dd = self._build_basis_matrix(x_int, deriv=2)
        Phi = self._build_basis_matrix(x_int, deriv=0)
        F = equation_f(x_int)

        if has_first_deriv:
            Phi_d = self._build_basis_matrix(x_int, deriv=1)
            if variable_coef is not None:
                coef = 1 + x_int
                A_matrix = -coef[:, np.newaxis] * Phi_dd + Phi
            else:
                A_matrix = -Phi_dd + 5 * Phi_d + Phi
        else:
            A_matrix = -Phi_dd + Phi

        # Нормальные уравнения
        A = A_matrix.T @ A_matrix * dx
        B = A_matrix.T @ F * dx

        try:
            self.coefficients = solve(A, B)
            self.condition_number = np.linalg.cond(A)
            self.matrix_A = A
        except:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        elapsed = (time.perf_counter() - start) * 1000
        return self.coefficients, elapsed

    def galerkin(self, equation_f, x_points, has_first_deriv=False,
                 variable_coef=None):
        """
        Классический метод Галеркина: ∫R·φ_i dx = 0
        """
        start = time.perf_counter()
        n = self.n_funcs

        x_int = np.linspace(0, 1, 300)
        dx = x_int[1] - x_int[0]

        Phi_dd = self._build_basis_matrix(x_int, deriv=2)
        Phi = self._build_basis_matrix(x_int, deriv=0)
        F = equation_f(x_int)

        A = np.zeros((n, n))
        B = np.zeros(n)

        for i in range(n):
            for j in range(n):
                if has_first_deriv:
                    Phi_d = self._build_basis_matrix(x_int, deriv=1)
                    if variable_coef is not None:
                        coef = 1 + x_int
                        integrand = (-coef * Phi_dd[:, j] + Phi[:, j]) * Phi[:, i]
                    else:
                        integrand = (-Phi_dd[:, j] + 5 * Phi_d[:, j] + Phi[:, j]) * Phi[:, i]
                else:
                    integrand = (-Phi_dd[:, j] + Phi[:, j]) * Phi[:, i]
                A[i, j] = np.sum(integrand) * dx
            B[i] = np.sum(F * Phi[:, i]) * dx

        try:
            self.coefficients = solve(A, B)
            self.condition_number = np.linalg.cond(A)
            self.matrix_A = A
        except:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        elapsed = (time.perf_counter() - start) * 1000
        return self.coefficients, elapsed

    def malyshev(self, equation_f, x_points, has_first_deriv=False,
                 variable_coef=None):
        """
        Метод Малышева: ∫R dx = 0, ∫R' dx = 0, ...
        ИСПРАВЛЕННАЯ ВЕРСИЯ
        """
        start = time.perf_counter()
        n = self.n_funcs

        x_int = np.linspace(0, 1, 300)
        dx = x_int[1] - x_int[0]

        A = np.zeros((n, n))
        B = np.zeros(n)

        x_0, x_1 = np.array([0.0]), np.array([1.0])

        for k in range(n):
            if k == 0:
                # Условие 1: ∫R dx = 0
                Phi_dd = self._build_basis_matrix(x_int, deriv=2)
                Phi = self._build_basis_matrix(x_int, deriv=0)

                if has_first_deriv:
                    Phi_d = self._build_basis_matrix(x_int, deriv=1)
                    if variable_coef is not None:
                        coef = 1 + x_int
                        A[k, :] = np.sum(-coef[:, np.newaxis] * Phi_dd + Phi, axis=0) * dx
                    else:
                        A[k, :] = np.sum(-Phi_dd + 5 * Phi_d + Phi, axis=0) * dx
                else:
                    A[k, :] = np.sum(-Phi_dd + Phi, axis=0) * dx

                B[k] = np.sum(equation_f(x_int)) * dx

            elif k == 1:
                # Условие 2: ∫R' dx = 0 → R(1) - R(0) = 0
                Phi_dd_0 = self._build_basis_matrix(x_0, deriv=2)
                Phi_dd_1 = self._build_basis_matrix(x_1, deriv=2)
                Phi_0 = self._build_basis_matrix(x_0, deriv=0)
                Phi_1 = self._build_basis_matrix(x_1, deriv=0)

                f_0 = equation_f(x_0)[0]
                f_1 = equation_f(x_1)[0]

                if has_first_deriv:
                    Phi_d_0 = self._build_basis_matrix(x_0, deriv=1)
                    Phi_d_1 = self._build_basis_matrix(x_1, deriv=1)
                    if variable_coef is not None:
                        A[k, :] = (-(1 + 1) * Phi_dd_1 + Phi_1)[0] - (-(1 + 0) * Phi_dd_0 + Phi_0)[0]
                        B[k] = f_1 - f_0
                    else:
                        A[k, :] = (-Phi_dd_1 + 5 * Phi_d_1 + Phi_1)[0] - \
                                  (-Phi_dd_0 + 5 * Phi_d_0 + Phi_0)[0]
                        B[k] = f_1 - f_0
                else:
                    A[k, :] = (-Phi_dd_1 + Phi_1)[0] - (-Phi_dd_0 + Phi_0)[0]
                    B[k] = f_1 - f_0

            else:
                # k >= 2: используем интегралы от невязки (упрощённо)
                Phi_dd = self._build_basis_matrix(x_int, deriv=2)
                Phi = self._build_basis_matrix(x_int, deriv=0)

                if has_first_deriv:
                    Phi_d = self._build_basis_matrix(x_int, deriv=1)
                    A[k, :] = np.sum(-Phi_dd + 5 * Phi_d + Phi, axis=0) * dx
                else:
                    A[k, :] = np.sum(-Phi_dd + Phi, axis=0) * dx

                B[k] = np.sum(equation_f(x_int)) * dx

        try:
            self.coefficients = solve(A, B)
            self.condition_number = np.linalg.cond(A)
            self.matrix_A = A
        except:
            self.coefficients = np.linalg.lstsq(A, B, rcond=None)[0]
            self.condition_number = np.inf

        elapsed = (time.perf_counter() - start) * 1000
        return self.coefficients, elapsed

    def get_solution(self, x_points):
        """Получить приближённое решение"""
        if self.coefficients is None:
            raise ValueError("Сначала нужно решить уравнение!")
        Phi = self._build_basis_matrix(x_points, deriv=0)
        return Phi @ self.coefficients

    def get_residual(self, equation_f, x_points, has_first_deriv=False,
                     variable_coef=None):
        """Получить невязку"""
        if self.coefficients is None:
            raise ValueError("Сначала нужно решить уравнение!")

        Phi_dd = self._build_basis_matrix(x_points, deriv=2)
        Phi = self._build_basis_matrix(x_points, deriv=0)
        F = equation_f(x_points)

        if has_first_deriv:
            Phi_d = self._build_basis_matrix(x_points, deriv=1)
            if variable_coef is not None:
                coef = 1 + x_points
                return -coef[:, np.newaxis] * (Phi_dd @ self.coefficients) + \
                    Phi @ self.coefficients - F
            else:
                return -Phi_dd @ self.coefficients + 5 * Phi_d @ self.coefficients + \
                    Phi @ self.coefficients - F
        else:
            return -Phi_dd @ self.coefficients + Phi @ self.coefficients - F


# ============================================================================
# ЧАСТЬ 4: МЕТРИКИ
# ============================================================================

class Metrics:
    """Метрики качества"""

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
    def convergence_rate(n_values, errors):
        if len(n_values) < 2 or len(errors) < 2:
            return None
        log_n = np.log(n_values)
        log_e = np.log(errors)
        slope = np.polyfit(log_n, log_e, 1)[0]
        return -slope


# ============================================================================
# ЧАСТЬ 5: ВИЗУАЛИЗАЦИЯ (ИСПРАВЛЕННАЯ)
# ============================================================================

class Visualization:
    """Визуализация результатов"""

    @staticmethod
    def plot_equation_comparison(results, equation_name, save_path):
        """Графики сравнения методов"""
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))

        method_colors = {
            'collocation': 'blue',
            'least_squares': 'green',
            'galerkin': 'red',
            'malyshev': 'orange'
        }
        method_names = {
            'collocation': 'Коллокация',
            'least_squares': 'МНК',
            'galerkin': 'Галеркин',
            'malyshev': 'Малышев'
        }

        # 1. Сравнение решений
        ax = axes[0, 0]
        x = results[0]['x']
        u_exact = results[0]['u_exact']
        ax.plot(x, u_exact, 'k--', linewidth=3, label='Точное', alpha=0.7)

        for res in results:
            ax.plot(x, res['u_approx'], method_colors[res['method']],
                    linewidth=2, label=f"{method_names[res['method']]} ({res['max_error']:.1e})")

        ax.set_xlabel('x', fontsize=12, fontweight='bold')
        ax.set_ylabel('U(x)', fontsize=12, fontweight='bold')
        ax.set_title(f'Приближённые решения ({equation_name})', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--')

        # 2. Погрешности
        ax = axes[0, 1]
        for res in results:
            ax.plot(x, res['error'], method_colors[res['method']],
                    linewidth=2, label=f"{method_names[res['method']]}")

        ax.set_xlabel('x', fontsize=12, fontweight='bold')
        ax.set_ylabel('|U_exact - U_approx|', fontsize=12, fontweight='bold')
        ax.set_title('Погрешность решений', fontsize=14, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3, linestyle='--')

        # 3. Невязки
        ax = axes[1, 0]
        for res in results:
            ax.plot(x, res['residual'], method_colors[res['method']],
                    linewidth=2, label=f"{method_names[res['method']]}")

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
        headers = ['Метод', 'Max Error', 'RMS Error', 'Time (ms)', 'cond(A)']

        for res in results:
            row = [
                method_names[res['method']],
                f"{res['max_error']:.2e}",
                f"{res['rms_error']:.2e}",
                f"{res['time_ms']:.2f}",
                f"{res['condition_number']:.2f}"
            ]
            table_data.append(row)

        table = ax.table(cellText=table_data, colLabels=headers,
                         loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.3, 1.8)

        ax.set_title('Метрики качества', fontsize=14, fontweight='bold', pad=20)

        plt.suptitle(f'СРАВНЕНИЕ МЕТОДОВ: {equation_name}',
                     fontsize=16, fontweight='bold', y=1.02)

        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show()

    @staticmethod
    def plot_convergence(results_by_n, equation_name, save_path):
        """График сходимости"""
        fig, ax = plt.subplots(figsize=(10, 6))

        method_colors = {
            'collocation': 'blue',
            'least_squares': 'green',
            'galerkin': 'red',
            'malyshev': 'orange'
        }
        method_names = {
            'collocation': 'Коллокация',
            'least_squares': 'МНК',
            'galerkin': 'Галеркин',
            'malyshev': 'Малышев'
        }
        markers = {'collocation': 'o', 'least_squares': 's',
                   'galerkin': '^', 'malyshev': 'd'}

        for method in ['collocation', 'least_squares', 'galerkin', 'malyshev']:
            n_values = []
            errors = []

            for n, results in results_by_n.items():
                for res in results:
                    if res['method'] == method and res['max_error'] != np.inf:
                        n_values.append(n)
                        errors.append(res['max_error'])
                        break

            if n_values:
                ax.loglog(n_values, errors, markers[method],
                          color=method_colors[method], linewidth=2,
                          markersize=8, label=method_names[method])

        ax.set_xlabel('Число базисных функций (N)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Максимальная погрешность', fontsize=12, fontweight='bold')
        ax.set_title(f'Сходимость методов ({equation_name})', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='--', which='both')

        plt.tight_layout()
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.show()

    @staticmethod
    def save_results_to_csv(results, save_path):
        """Сохранить результаты в CSV"""
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['Уравнение', 'Метод', 'Базис', 'N',
                             'Max Error', 'RMS Error', 'Max Residual',
                             'Time (ms)', 'cond(A)'])

            for res in results:
                writer.writerow([
                    res.get('equation', 'N/A'),
                    res['method'],
                    res.get('basis', 'polynomial'),
                    res['n_funcs'],
                    f"{res['max_error']:.6e}",
                    f"{res.get('rms_error', 0):.6e}",
                    f"{res.get('max_residual', 0):.6e}",
                    f"{res['time_ms']:.4f}",
                    f"{res['condition_number']:.4f}"
                ])


# ============================================================================
# ЧАСТЬ 6: ЭКСПЕРИМЕНТЫ
# ============================================================================

def run_single_equation_comparison(equation_name='poisson', n_funcs=5, basis='polynomial'):
    """Эксперимент 1: Сравнение 4 методов на одном уравнении"""
    print("=" * 80)
    print(f"ЭКСПЕРИМЕНТ 1: {equation_name.upper()}")
    print("=" * 80)

    eq = TestEquations.get_equation(equation_name)
    x = np.linspace(0, 1, 200)
    u_exact = eq['exact'](x)
    f = eq['f']

    methods = [
        ('collocation', 'Коллокация'),
        ('least_squares', 'МНК'),
        ('galerkin', 'Галеркин'),
        ('malyshev', 'Малышев')
    ]

    results = []

    for method_key, method_name in methods:
        print(f"\n[{method_name}]...")

        solver = ProjectionMethods(n_funcs=n_funcs, basis_type=basis)
        method_map = {
            'collocation': solver.collocation,
            'least_squares': solver.least_squares,
            'galerkin': solver.galerkin,
            'malyshev': solver.malyshev
        }

        coefficients, time_ms = method_map[method_key](
            f, x, eq['has_first_deriv'], eq['has_variable_coef']
        )
        u_approx = solver.get_solution(x)
        residual = solver.get_residual(f, x, eq['has_first_deriv'], eq['has_variable_coef'])

        max_error = Metrics.max_error(u_exact, u_approx)
        rms_error = Metrics.rms_error(u_exact, u_approx)
        max_residual = Metrics.max_residual(residual)

        results.append({
            'equation': equation_name,
            'method': method_key,
            'basis': basis,
            'n_funcs': n_funcs,
            'x': x,
            'u_approx': u_approx,
            'u_exact': u_exact,
            'error': u_exact - u_approx,
            'residual': residual,
            'max_error': max_error,
            'rms_error': rms_error,
            'max_residual': max_residual,
            'time_ms': time_ms,
            'condition_number': solver.condition_number
        })

        print(f"  Max ошибка: {max_error:.2e}")
        print(f"  RMS ошибка: {rms_error:.2e}")
        print(f"  Время: {time_ms:.2f} мс")
        print(f"  cond(A): {solver.condition_number:.2f}")

    Visualization.save_results_to_csv(results, f'results/exp1_{equation_name}.csv')
    Visualization.plot_equation_comparison(results, eq['name'],
                                           f'results/exp1_{equation_name}.png')

    return results


def run_convergence_study(equation_name='poisson', basis='polynomial'):
    """Эксперимент 2: Исследование сходимости"""
    print("\n" + "=" * 80)
    print(f"ЭКСПЕРИМЕНТ 2: СХОДИМОСТЬ ({equation_name})")
    print("=" * 80)

    eq = TestEquations.get_equation(equation_name)
    x = np.linspace(0, 1, 200)
    u_exact = eq['exact'](x)
    f = eq['f']

    n_values = [3, 5, 7, 10]
    methods = ['collocation', 'least_squares', 'galerkin', 'malyshev']

    results_by_n = {}

    for n in n_values:
        print(f"\nN = {n}")
        results_by_n[n] = []

        for method_key in methods:
            solver = ProjectionMethods(n_funcs=n, basis_type=basis)
            method_map = {
                'collocation': solver.collocation,
                'least_squares': solver.least_squares,
                'galerkin': solver.galerkin,
                'malyshev': solver.malyshev
            }

            coefficients, time_ms = method_map[method_key](
                f, x, eq['has_first_deriv'], eq['has_variable_coef']
            )
            u_approx = solver.get_solution(x)

            max_error = Metrics.max_error(u_exact, u_approx)

            results_by_n[n].append({
                'method': method_key,
                'n_funcs': n,
                'max_error': max_error,
                'time_ms': time_ms,
                'condition_number': solver.condition_number
            })

            print(f"  {method_key:15s}: Max Error = {max_error:.2e}")

    Visualization.plot_convergence(results_by_n, eq['name'],
                                   f'results/exp2_convergence_{equation_name}.png')

    return results_by_n


def run_basis_comparison(equation_name='poisson', n_funcs=5):
    """Эксперимент 3: Сравнение базисных функций"""
    print("\n" + "=" * 80)
    print(f"ЭКСПЕРИМЕНТ 3: БАЗИСНЫЕ ФУНКЦИИ ({equation_name})")
    print("=" * 80)

    eq = TestEquations.get_equation(equation_name)
    x = np.linspace(0, 1, 200)
    u_exact = eq['exact'](x)
    f = eq['f']

    bases = ['polynomial', 'legendre', 'chebyshev', 'trigonometric']
    methods = ['galerkin', 'collocation', 'malyshev']

    all_results = []

    for basis in bases:
        print(f"\nБазис: {basis}")

        for method_key in methods:
            solver = ProjectionMethods(n_funcs=n_funcs, basis_type=basis)
            method_map = {
                'collocation': solver.collocation,
                'galerkin': solver.galerkin,
                'malyshev': solver.malyshev
            }

            try:
                coefficients, time_ms = method_map[method_key](
                    f, x, eq['has_first_deriv'], eq['has_variable_coef']
                )
                u_approx = solver.get_solution(x)
                residual = solver.get_residual(f, x, eq['has_first_deriv'],
                                               eq['has_variable_coef'])

                max_error = Metrics.max_error(u_exact, u_approx)
                rms_error = Metrics.rms_error(u_exact, u_approx)
                max_residual = Metrics.max_residual(residual)

                all_results.append({
                    'equation': equation_name,
                    'method': method_key,
                    'basis': basis,
                    'n_funcs': n_funcs,
                    'max_error': max_error,
                    'rms_error': rms_error,
                    'max_residual': max_residual,
                    'time_ms': time_ms,
                    'condition_number': solver.condition_number
                })

                print(f"  {method_key:15s}: Max Error = {max_error:.2e}")
            except Exception as e:
                print(f"  {method_key:15s}: Ошибка - {e}")
                all_results.append({
                    'equation': equation_name,
                    'method': method_key,
                    'basis': basis,
                    'n_funcs': n_funcs,
                    'max_error': np.inf,
                    'rms_error': np.inf,
                    'max_residual': np.inf,
                    'time_ms': 0,
                    'condition_number': np.inf
                })

    Visualization.save_results_to_csv(all_results,
                                      f'results/exp3_basis_{equation_name}.csv')

    return all_results


def main():
    """Главная функция исследования"""
    print("=" * 80)
    print("СРАВНИТЕЛЬНЫЙ АНАЛИЗ ПРОЕКЦИОННЫХ МЕТОДОВ")
    print("Научный проект МЧА | БГУИР + T-Academy")
    print("=" * 80)
    print(f"Дата начала: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    os.makedirs('results', exist_ok=True)

    # Эксперимент 1: Базовое сравнение (уравнение Пуассона с полиномиальным решением)
    results_1 = run_single_equation_comparison(
        equation_name='poisson',
        n_funcs=5,
        basis='polynomial'
    )

    # Эксперимент 2: Сходимость
    results_2 = run_convergence_study(
        equation_name='poisson',
        basis='polynomial'
    )

    # Эксперимент 3: Сравнение базисов
    results_3 = run_basis_comparison(
        equation_name='poisson',
        n_funcs=5
    )

    print("\n" + "=" * 80)
    print("ИССЛЕДОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 80)
    print(f"Дата завершения: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("Результаты сохранены в папке: results/")
    print()
    print("Для защиты подготовьте:")
    print("  1. Графики сравнения методов (exp1_*.png)")
    print("  2. Графики сходимости (exp2_*.png)")
    print("  3. Таблицы результатов (exp*.csv)")
    print("  4. Текстовый анализ из отчёта")
    print("=" * 80)


if __name__ == "__main__":
    main()