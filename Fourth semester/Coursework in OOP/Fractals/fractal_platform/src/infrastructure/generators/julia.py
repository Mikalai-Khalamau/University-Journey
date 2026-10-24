from __future__ import annotations

import numpy as np

from src.domain.value_objects.fractal_params import JuliaParams
from src.infrastructure.generators.base_generator import BaseFractalGenerator


class JuliaGenerator(BaseFractalGenerator):
    def _compute(self, params: JuliaParams) -> np.ndarray:
        x = np.linspace(-params.scale / 2, params.scale / 2, params.width)
        y = np.linspace(-params.scale / 2, params.scale / 2, params.height)
        z = x[None, :] + 1j * y[:, None]
        c = complex(params.c_re, params.c_im)
        div_time = np.zeros(z.shape, dtype=np.int32)
        mask = np.ones(z.shape, dtype=bool)
        for i in range(params.max_iter):
            z[mask] = z[mask] * z[mask] + c
            escaped = np.abs(z) > 2
            newly_escaped = escaped & mask
            div_time[newly_escaped] = i
            mask &= ~escaped
            if not mask.any():
                break
        div_time[div_time == 0] = params.max_iter
        return div_time.astype(np.float64)
