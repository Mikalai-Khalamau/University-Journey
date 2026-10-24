from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator


class GenerateRequest(BaseModel):
    fractal_type: Literal["mandelbrot", "julia", "burning_ship", "ifs"]
    width: int = Field(gt=0, le=4096)
    height: int = Field(gt=0, le=4096)
    max_iter: int = Field(default=300, gt=0, le=10000)
    gamma: float = Field(default=2.2, gt=0, le=8)
    center_x: float | None = None
    center_y: float | None = None
    scale: float | None = None
    c_re: float | None = None
    c_im: float | None = None
    seed: int | None = None
    samples: int | None = None
    name: str | None = Field(default=None, max_length=120)
    tags: list[str] = Field(default_factory=lambda: ["basic"])

    preset_name: str | None = Field(default=None, max_length=64)
    variation_name: str | None = Field(default=None, max_length=64)
    custom_transforms: list[dict] | None = Field(default=None, max_length=10)

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        if not v:
            return ["basic"]
        cleaned = []
        for tag in v:
            tag = tag.strip().lower()
            if tag and len(tag) <= 32:
                cleaned.append(tag)
        return cleaned or ["basic"]

    @field_validator('custom_transforms')
    @classmethod
    def validate_custom_transforms(cls, v):
        if v is None:
            return v
        if not isinstance(v, list):
            raise ValueError('custom_transforms must be a list')
        required_keys = {"a", "b", "c", "d", "e", "f", "weight"}
        for i, t in enumerate(v):
            if not isinstance(t, dict):
                raise ValueError(f'Transform {i} must be a dict')
            missing = required_keys - set(t.keys())
            if missing:
                raise ValueError(f'Transform {i} missing keys: {missing}')
            if t["weight"] <= 0:
                raise ValueError(f'Transform {i}: weight must be positive')
        return v


class ImportRequest(BaseModel):
    params: dict
    name: str | None = Field(default=None, max_length=120)


class UpdateFractalRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)


class UpdateTagsRequest(BaseModel):
    tags: list[str] = Field(min_length=1)

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v):
        cleaned = []
        for tag in v:
            tag = tag.strip().lower()
            if tag and len(tag) <= 32:
                cleaned.append(tag)
        if not cleaned:
            raise ValueError('At least one valid tag required')
        return cleaned


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=6, max_length=128)
    email: str | None = Field(default=None, max_length=120)


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=6, max_length=128)