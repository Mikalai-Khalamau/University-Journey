from __future__ import annotations

import math
import random
import numpy as np
from numpy import uint8
from src.domain.value_objects.fractal_params import IFSParams
from src.infrastructure.generators.base_generator import BaseFractalGenerator

def linear(x, y): return x, y


def sinusoidal(x, y): return math.sin(x), math.sin(y)


def spherical(x, y):
    r = x * x + y * y + 1e-9
    return x / r, y / r


def swirl(x, y):
    r = x * x + y * y + 1e-9
    return x * math.sin(r) - y * math.cos(r), x * math.cos(r) + y * math.sin(r)


def horseshoe(x, y):
    r = math.sqrt(x * x + y * y) + 1e-9
    return (x * x - y * y) / r, 2 * x * y / r


def polar(x, y):
    return math.atan2(y, x) / math.pi, math.sqrt(x * x + y * y) - 1


def handkerchief(x, y):
    theta = math.atan2(y, x)
    r = math.sqrt(x * x + y * y) + 1e-9
    return math.sin(theta + r) * r, math.cos(theta - r) * r


def heart(x, y):
    theta = math.atan2(y, x)
    r = math.sqrt(x * x + y * y) + 1e-9
    return math.sin(theta * r) * r, -math.cos(theta * r) * r


def disc(x, y):
    theta = math.atan2(y, x)
    r = math.sqrt(x * x + y * y) + 1e-9
    return math.sin(math.pi * r) * theta / math.pi, math.cos(math.pi * r) * theta / math.pi


def fisheye(x, y):
    r = math.sqrt(x * x + y * y) + 1e-9
    return 2 * y / (r + 1), 2 * x / (r + 1)


def tangent(x, y): return math.sin(x) / (math.cos(y) + 1e-9), math.atan(y)


def cross(x, y):
    d = (x * x - y * y) ** 2 + 1e-9
    return x / math.sqrt(d), y / math.sqrt(d)


TRANSFORMATIONS = {
    "linear": linear, "sinusoidal": sinusoidal, "spherical": spherical,
    "swirl": swirl, "horseshoe": horseshoe, "polar": polar,
    "handkerchief": handkerchief, "heart": heart, "disc": disc,
    "fisheye": fisheye, "tan": tangent, "cross": cross,
}

PRESETS = {
    "fern": {
        "transforms": [
            {"a": 0.0, "b": 0.0, "c": 0.0, "d": 0.16, "e": 0.0, "f": 0.0, "weight": 0.01},
            {"a": 0.85, "b": 0.04, "c": -0.04, "d": 0.85, "e": 0.0, "f": 1.6, "weight": 0.85},
            {"a": 0.2, "b": -0.26, "c": 0.23, "d": 0.22, "e": 0.0, "f": 1.6, "weight": 0.07},
            {"a": -0.15, "b": 0.28, "c": 0.26, "d": 0.24, "e": 0.0, "f": 0.44, "weight": 0.07},
        ],
        "view": {"x_min": -2.5, "x_max": 2.5, "y_min": 0, "y_max": 10},
        "forced_variation": "linear"
    },
    "spiral": {
        "transforms": [
            {"a": 0.7, "b": -0.3, "c": 0.3, "d": 0.7, "e": 0.8, "f": 0.8, "weight": 0.5},
            {"a": 0.7, "b": 0.3, "c": -0.3, "d": 0.7, "e": -0.8, "f": -0.8, "weight": 0.5},
        ],
        "view": {"x_min": -4, "x_max": 4, "y_min": -4, "y_max": 4},
        "forced_variation": "swirl"
    },
    "heart_flame": {
        "transforms": [
            {"a": 0.5, "b": 0.0, "c": 0.0, "d": 0.5, "e": 0.0, "f": 0.3, "weight": 0.4},
            {"a": 0.5, "b": 0.0, "c": 0.0, "d": 0.5, "e": -0.6, "f": -0.4, "weight": 0.3},
            {"a": 0.5, "b": 0.0, "c": 0.0, "d": 0.5, "e": 0.6, "f": -0.4, "weight": 0.3},
        ],
        "view": {"x_min": -3, "x_max": 3, "y_min": -3, "y_max": 3},
        "forced_variation": "heart"
    },
    "fisheye_grid": {
        "transforms": [
            {"a": 0.4, "b": 0.0, "c": 0.0, "d": 0.4, "e": 1.0, "f": 1.0, "weight": 0.25},
            {"a": 0.4, "b": 0.0, "c": 0.0, "d": 0.4, "e": -1.0, "f": 1.0, "weight": 0.25},
            {"a": 0.4, "b": 0.0, "c": 0.0, "d": 0.4, "e": -1.0, "f": -1.0, "weight": 0.25},
            {"a": 0.4, "b": 0.0, "c": 0.0, "d": 0.4, "e": 1.0, "f": -1.0, "weight": 0.25},
        ],
        "view": {"x_min": -4, "x_max": 4, "y_min": -4, "y_max": 4},
        "forced_variation": "fisheye"
    }
}


def _validate_transform(t: dict, idx: int) -> None:
    """Валидация одной трансформации."""
    required = {"a", "b", "c", "d", "e", "f", "weight"}
    missing = required - set(t.keys())
    if missing:
        raise ValueError(f"Transform {idx} missing keys: {missing}")
    if t["weight"] <= 0:
        raise ValueError(f"Transform {idx}: weight must be positive")
    for key in required - {"weight"}:
        if not isinstance(t[key], (int, float)):
            raise ValueError(f"Transform {idx}: {key} must be numeric")


def _infer_view(transforms: list[dict], margin: float = 1.5) -> dict:
    """Авто-расчёт viewport по диапазонам e, f (сдвиги)."""
    e_vals = [t["e"] for t in transforms]
    f_vals = [t["f"] for t in transforms]
    e_min, e_max = min(e_vals), max(e_vals)
    f_min, f_max = min(f_vals), max(f_vals)

    e_range = (e_max - e_min) * margin + 2
    f_range = (f_max - f_min) * margin + 2
    e_center = (e_min + e_max) / 2
    f_center = (f_min + f_max) / 2

    return {
        "x_min": e_center - e_range / 2,
        "x_max": e_center + e_range / 2,
        "y_min": f_center - f_range / 2,
        "y_max": f_center + f_range / 2,
    }


class IFSFractalGenerator(BaseFractalGenerator):

    def _compute(self, params: IFSParams) -> np.ndarray:
        width, height = params.width, params.height
        iterations = getattr(params, 'samples', 200_000)
        seed = getattr(params, 'seed', 42)

        preset_name = getattr(params, 'preset_name', None)
        variation_name = getattr(params, 'variation_name', None)
        custom_transforms = getattr(params, 'custom_transforms', None)

        if preset_name == "custom" or not preset_name:
            if custom_transforms and isinstance(custom_transforms, list) and len(custom_transforms) > 0:
                for i, t in enumerate(custom_transforms):
                    _validate_transform(t, i)
                transforms = custom_transforms
                view = _infer_view(transforms)
            else:
                transforms = [{"a": 0.5, "b": 0.0, "c": 0.0, "d": 0.5, "e": 0.5, "f": 0.5, "weight": 1.0}]
                view = {"x_min": -2, "x_max": 2, "y_min": -2, "y_max": 2}
                preset_name = "custom_fallback"
        elif preset_name in PRESETS:
            preset = PRESETS[preset_name]
            transforms = preset["transforms"]
            view = preset["view"]
        else:
            preset = PRESETS["fern"]
            transforms = preset["transforms"]
            view = preset["view"]
            preset_name = "fern"

        STRICT_PRESETS = {"fern": "linear"}
        forced = PRESETS.get(preset_name, {}).get("forced_variation") if preset_name in PRESETS else None

        if preset_name in STRICT_PRESETS:
            final_variation = STRICT_PRESETS[preset_name]
        elif variation_name and variation_name in TRANSFORMATIONS:
            final_variation = variation_name
        elif forced:
            final_variation = forced
        else:
            final_variation = 'linear'

        var_func = TRANSFORMATIONS.get(final_variation, linear)

        hist_r = np.zeros((height, width), dtype=np.float64)
        hist_g = np.zeros((height, width), dtype=np.float64)
        hist_b = np.zeros((height, width), dtype=np.float64)
        hist_freq = np.zeros((height, width), dtype=np.float64)

        random.seed(seed)
        x, y = 0.0, 0.0

        warmup = 100 if final_variation != 'linear' else 50
        for _ in range(warmup):
            t = random.choices(transforms, weights=[tr["weight"] for tr in transforms])[0]
            x = t["a"] * x + t["b"] * y + t["e"]
            y = t["c"] * x + t["d"] * y + t["f"]
            x, y = var_func(x, y)

        points_drawn = 0
        default_colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)]

        for i in range(iterations):
            t = random.choices(transforms, weights=[tr["weight"] for tr in transforms])[0]
            new_x = t["a"] * x + t["b"] * y + t["e"]
            new_y = t["c"] * x + t["d"] * y + t["f"]
            x, y = new_x, new_y
            x, y = var_func(x, y)

            px = int((x - view["x_min"]) / (view["x_max"] - view["x_min"]) * width)
            py = int((view["y_max"] - y) / (view["y_max"] - view["y_min"]) * height)

            if 0 <= px < width and 0 <= py < height:
                color = t.get("color", default_colors[i % len(default_colors)])
                hist_r[py, px] += color[0]
                hist_g[py, px] += color[1]
                hist_b[py, px] += color[2]
                hist_freq[py, px] += 1
                points_drawn += 1


        if points_drawn < 100:
            for yy in range(height):
                for xx in range(width):
                    hist_r[yy, xx] = (xx / width) * 255
                    hist_g[yy, xx] = (yy / height) * 255
                    hist_b[yy, xx] = 128
                    hist_freq[yy, xx] = 1

        log_freq = np.log(hist_freq + 1)
        max_log = np.max(log_freq)
        intensity = log_freq / max_log if max_log > 1e-10 else np.zeros_like(log_freq)

        img = np.zeros((height, width, 3), dtype=uint8)
        for yy in range(height):
            for xx in range(width):
                if hist_freq[yy, xx] > 0:
                    r = int(np.clip((hist_r[yy, xx] / hist_freq[yy, xx]) * intensity[yy, xx], 0, 255))
                    g = int(np.clip((hist_g[yy, xx] / hist_freq[yy, xx]) * intensity[yy, xx], 0, 255))
                    b = int(np.clip((hist_b[yy, xx] / hist_freq[yy, xx]) * intensity[yy, xx], 0, 255))
                    img[yy, xx] = [r, g, b]
                else:
                    img[yy, xx] = [10, 10, 20]

        return img

    def get_supported_types(self) -> list[str]:
        return list(PRESETS.keys()) + ["custom"]