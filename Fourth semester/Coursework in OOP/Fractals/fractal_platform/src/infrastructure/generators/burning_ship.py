from __future__ import annotations

import numpy as np

from src.domain.value_objects.fractal_params import BurningShipParams
from src.infrastructure.generators.base_generator import BaseFractalGenerator


class BurningShipGenerator(BaseFractalGenerator):
    def _compute(self, params: BurningShipParams) -> np.ndarray:
        x = np.linspace(
            params.center_x - params.scale / 2,
            params.center_x + params.scale / 2,
            params.width,
        )
        y = np.linspace(
            params.center_y + params.scale / 2,
            params.center_y - params.scale / 2,
            params.height,
        )
        c = x[None, :] + 1j * y[:, None]

        z_r = np.zeros((params.height, params.width), dtype=np.float64)
        z_i = np.zeros((params.height, params.width), dtype=np.float64)
        c_r = c.real.copy()
        c_i = c.imag.copy()

        div_time = np.full((params.height, params.width), params.max_iter, dtype=np.int32)
        mask = np.ones((params.height, params.width), dtype=bool)

        for i in range(params.max_iter):
            az_r = np.abs(z_r)
            az_i = np.abs(z_i)

            new_r = az_r * az_r - az_i * az_i + c_r
            new_i = 2.0 * az_r * az_i + c_i

            z_r[mask] = new_r[mask]
            z_i[mask] = new_i[mask]

            escaped = (z_r * z_r + z_i * z_i > 4.0) & mask
            div_time[escaped] = i
            mask[escaped] = False

            if not mask.any():
                break

        return div_time.astype(np.float64)