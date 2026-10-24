from __future__ import annotations

import time
from uuid import UUID, uuid4

import numpy as np

from src.application.services.validator import FractalValidator
from src.domain.entities.fractal import Fractal
from src.domain.interfaces.repository import IFractalRepository
from src.domain.interfaces.storage import IImageStorage
from src.domain.value_objects.fractal_params import FractalParams
from src.domain.value_objects.image_metadata import ImageMetadata
from src.infrastructure.cache.cache_proxy import FractalCacheProxy
from src.infrastructure.factories.generator_factory import FractalGeneratorFactory
from src.infrastructure.processors.gamma_decorator import GammaCorrectionProcessor


class GenerateFractalUseCase:
    def __init__(
            self,
            repository: IFractalRepository,
            storage: IImageStorage,
            generator_factory: FractalGeneratorFactory,
            validator: FractalValidator,
    ) -> None:
        self.repository = repository
        self.storage = storage
        self.generator_factory = generator_factory
        self.validator = validator

    def execute(self, params: FractalParams, user_id: UUID, name: str, tags: list[str] | None = None) -> UUID:
        self.validator.validate(params)
        generator = FractalCacheProxy(self.generator_factory.create(params.fractal_type))

        started = time.perf_counter()
        raw_image = generator.generate(params)

        image = raw_image
        if params.gamma and abs(params.gamma - 1.0) > 1e-3:
            processor = GammaCorrectionProcessor(gamma=params.gamma)
            image = processor.process(image)
            print(f"[UseCase] Gamma correction applied: γ={params.gamma}")

        if image.dtype != np.uint8:
            image = np.clip(image * 255.0, 0, 255).astype(np.uint8)

        fractal_id = uuid4()
        file_path = self.storage.save(image, f"{user_id}_{fractal_id}.png")

        elapsed_ms = (time.perf_counter() - started) * 1000

        fractal = Fractal(
            id=fractal_id,
            user_id=user_id,
            name=name.strip() or "Без названия",
            fractal_type=params.fractal_type,
            params=params,
            metadata=ImageMetadata(width=params.width, height=params.height, gamma=params.gamma),
            file_path=str(file_path),
            generation_time_ms=elapsed_ms,
            tags=tags or ["basic"],
        )

        self.repository.save(fractal)
        return fractal_id