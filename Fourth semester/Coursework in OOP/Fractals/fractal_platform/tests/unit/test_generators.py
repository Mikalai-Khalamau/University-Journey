from src.domain.value_objects.fractal_params import IFSParams, MandelbrotParams
from src.infrastructure.generators.ifs import IFSFractalGenerator
from src.infrastructure.generators.mandelbrot import MandelbrotGenerator


def test_mandelbrot_shape():
    params = MandelbrotParams(width=120, height=80, max_iter=50)
    image = MandelbrotGenerator().generate(params)
    assert image.shape == (80, 120, 3)


def test_ifs_shape():
    params = IFSParams(width=120, height=80, max_iter=1, samples=5000)
    image = IFSFractalGenerator().generate(params)
    assert image.shape == (80, 120, 3)
