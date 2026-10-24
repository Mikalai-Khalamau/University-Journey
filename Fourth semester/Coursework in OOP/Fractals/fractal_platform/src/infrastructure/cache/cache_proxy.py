from __future__ import annotations

from collections import OrderedDict
from dataclasses import asdict

import numpy as np

from src.domain.interfaces.generator import IFractalGenerator
from src.domain.value_objects.fractal_params import FractalParams


class FractalCacheProxy(IFractalGenerator):
    def __init__(self, target: IFractalGenerator, max_size: int = 32) -> None:
        self._target = target
        self._cache: OrderedDict[str, np.ndarray] = OrderedDict()
        self._max_size = max_size

    def generate(self, params: FractalParams) -> np.ndarray:
        key = str(asdict(params))
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        image = self._target.generate(params)
        self._cache[key] = image
        if len(self._cache) > self._max_size:
            self._cache.popitem(last=False)
        return image
