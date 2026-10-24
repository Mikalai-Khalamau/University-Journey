from __future__ import annotations

from src.domain.value_objects.fractal_params import IFSParams, JuliaParams, MandelbrotParams


class FractalBuilder:
    def __init__(self) -> None:
        self._kind = "mandelbrot"
        self._values: dict = {"width": 800, "height": 600, "max_iter": 300, "gamma": 2.2}

    def mandelbrot(self) -> "FractalBuilder":
        self._kind = "mandelbrot"
        return self

    def julia(self) -> "FractalBuilder":
        self._kind = "julia"
        return self

    def ifs(self) -> "FractalBuilder":
        self._kind = "ifs"
        return self

    def center(self, x: float, y: float) -> "FractalBuilder":
        self._values["center_x"] = x
        self._values["center_y"] = y
        return self

    def zoom(self, scale: float) -> "FractalBuilder":
        self._values["scale"] = scale
        return self

    def dimensions(self, width: int, height: int) -> "FractalBuilder":
        self._values["width"] = width
        self._values["height"] = height
        return self

    def build(self):
        if self._kind == "mandelbrot":
            return MandelbrotParams(**self._values)
        if self._kind == "julia":
            return JuliaParams(**self._values)
        return IFSParams(**self._values)
