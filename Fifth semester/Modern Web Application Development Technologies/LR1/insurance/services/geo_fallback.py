"""City coordinates when Nominatim is unreachable (offline / lab network)."""
from __future__ import annotations

# Belarus branch demo cities (seed_data) + Latin aliases
CITY_COORDS: dict[str, tuple[float, float]] = {
    "минск": (53.9006, 27.5590),
    "minsk": (53.9006, 27.5590),
    "гродно": (53.6693, 23.8131),
    "grodno": (53.6693, 23.8131),
    "брест": (52.0976, 23.7341),
    "brest": (52.0976, 23.7341),
    "гомель": (52.4345, 30.9754),
    "gomel": (52.4345, 30.9754),
    "витебск": (55.1904, 30.2049),
    "vitebsk": (55.1904, 30.2049),
    "могилёв": (53.8940, 30.3303),
    "могилев": (53.8940, 30.3303),
    "mogilev": (53.8940, 30.3303),
    "бобруйск": (53.1387, 29.2214),
    "bobruisk": (53.1387, 29.2214),
    "барановичи": (53.1327, 26.0139),
    "baranovichi": (53.1327, 26.0139),
    "пинск": (52.1229, 26.0951),
    "pinsk": (52.1229, 26.0951),
    "орша": (54.5153, 30.4244),
    "orsha": (54.5153, 30.4244),
}


def coords_for_city(city: str) -> tuple[float, float] | None:
    key = (city or "").strip().lower()
    return CITY_COORDS.get(key)
