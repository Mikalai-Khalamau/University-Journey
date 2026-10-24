from src.application.services.fractal_builder import FractalBuilder
from src.presentation.api.dependencies import generate_use_case


def main() -> None:
    params = FractalBuilder().mandelbrot().dimensions(1024, 768).zoom(2.4).build()
    fractal_id = generate_use_case.execute(params)
    print(f"Generated fractal: {fractal_id}")


if __name__ == "__main__":
    main()
