from src.application.services.fractal_builder import FractalBuilder


def test_builder_builds_mandelbrot():
    params = FractalBuilder().mandelbrot().dimensions(300, 200).build()
    assert params.fractal_type == "mandelbrot"
    assert params.width == 300
