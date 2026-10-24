from __future__ import annotations
from dataclasses import asdict, dataclass, fields
from typing import Literal
from src.core.exceptions import ValidationError

_BASE_KEYS = {"fractal_type", "width", "height", "max_iter", "gamma"}


@dataclass(frozen=True, kw_only=True)
class FractalParams:
    fractal_type: str
    width: int
    height: int
    max_iter: int = 200
    gamma: float = 2.2

    def to_dict(self) -> dict:
        return asdict(self)

    def __post_init__(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValidationError("width and height must be positive")
        if self.max_iter <= 0:
            raise ValidationError("max_iter must be positive")
        if self.gamma <= 0:
            raise ValidationError("gamma must be positive")


@dataclass(frozen=True, kw_only=True)
class MandelbrotParams(FractalParams):
    fractal_type: Literal["mandelbrot"] = "mandelbrot"
    center_x: float = -0.5
    center_y: float = 0.0
    scale: float = 3.0


@dataclass(frozen=True, kw_only=True)
class JuliaParams(FractalParams):
    fractal_type: Literal["julia"] = "julia"
    c_re: float = -0.7
    c_im: float = 0.27015
    center_x: float = 0.0
    center_y: float = 0.0
    scale: float = 3.0


@dataclass(frozen=True, kw_only=True)
class BurningShipParams(FractalParams):
    fractal_type: Literal["burning_ship"] = "burning_ship"
    center_x: float = -0.5
    center_y: float = -0.5
    scale: float = 3.0


@dataclass(frozen=True, kw_only=True)
class IFSParams(FractalParams):
    fractal_type: Literal["ifs"] = "ifs"
    seed: int = 42
    samples: int = 200_000
    preset_name: str = "fern"
    variation_name: str = "swirl"
    custom_transforms: list[dict] | None = None

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.custom_transforms:
            required = {"a", "b", "c", "d", "e", "f", "weight"}
            for i, t in enumerate(self.custom_transforms):
                if not isinstance(t, dict):
                    raise ValidationError(f"Transform {i} must be a dict")
                missing = required - set(t.keys())
                if missing:
                    raise ValidationError(f"Transform {i} missing keys: {missing}")
                if t["weight"] <= 0:
                    raise ValidationError(f"Transform {i}: weight must be positive")


def _pick(data: dict, cls: type) -> dict:
    allowed = {f.name for f in fields(cls)}
    return {k: v for k, v in data.items() if k in allowed}


def build_fractal_params(data: dict) -> FractalParams:
    kind = data.get("fractal_type")
    if kind == "mandelbrot":
        payload = _pick(data, MandelbrotParams)
        payload.setdefault("center_x", -0.5)
        payload.setdefault("center_y", 0.0)
        payload.setdefault("scale", 3.0)
        return MandelbrotParams(**payload)
    if kind == "julia":
        payload = _pick(data, JuliaParams)
        payload.setdefault("c_re", -0.7)
        payload.setdefault("c_im", 0.27015)
        payload.setdefault("center_x", 0.0)
        payload.setdefault("center_y", 0.0)
        payload.setdefault("scale", 3.0)
        return JuliaParams(**payload)
    if kind == "burning_ship":
        payload = _pick(data, BurningShipParams)
        payload.setdefault("center_x", -0.5)
        payload.setdefault("center_y", -0.5)
        payload.setdefault("scale", 3.0)
        return BurningShipParams(**payload)
    if kind == "ifs":
        payload = _pick(data, IFSParams)
        payload.setdefault("seed", 42)
        payload.setdefault("samples", 200_000)
        payload.setdefault("preset_name", "fern")
        payload.setdefault("variation_name", "swirl")
        for key in ["preset_name", "variation_name", "custom_transforms"]:
            if key in data and data[key] is not None:
                payload[key] = data[key]
        return IFSParams(**payload)
    raise ValidationError(f"Unsupported fractal_type: {kind}")