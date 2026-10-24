from __future__ import annotations

import numpy as np

from src.domain.value_objects.fractal_params import MandelbrotParams
from src.infrastructure.generators.base_generator import BaseFractalGenerator


class MandelbrotGenerator(BaseFractalGenerator):
    def _compute(self, params: MandelbrotParams) -> np.ndarray:
        x = np.linspace(params.center_x - params.scale / 2, params.center_x + params.scale / 2, params.width)
        y = np.linspace(params.center_y - params.scale / 2, params.center_y + params.scale / 2, params.height)
        c = x[None, :] + 1j * y[:, None]
        z = np.zeros_like(c)
        div_time = np.zeros(c.shape, dtype=np.int32)
        mask = np.ones(c.shape, dtype=bool)

        for i in range(params.max_iter):
            z[mask] = z[mask] * z[mask] + c[mask]
            escaped = np.abs(z) > 2
            newly_escaped = escaped & mask
            div_time[newly_escaped] = i
            mask &= ~escaped
            if not mask.any():
                break

        div_time[div_time == 0] = params.max_iter

        return div_time.astype(np.float64)


