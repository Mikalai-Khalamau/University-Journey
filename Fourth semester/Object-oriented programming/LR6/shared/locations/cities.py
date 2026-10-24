from typing import Dict, Tuple
from decimal import Decimal


CITIES: Dict[str, Tuple[Decimal, Decimal]] = {
    "минск": (Decimal('53.9'), Decimal('27.5667')),
    "minsk": (Decimal('53.9'), Decimal('27.5667')),
    "лондон": (Decimal('51.5074'), Decimal('-0.1278')),
    "london": (Decimal('51.5074'), Decimal('-0.1278')),
    "токио": (Decimal('35.6762'), Decimal('139.6503')),
    "tokyo": (Decimal('35.6762'), Decimal('139.6503')),
    "шанхай": (Decimal('31.2304'), Decimal('121.4737')),
    "shanghai": (Decimal('31.2304'), Decimal('121.4737')),
    "варшава": (Decimal('52.2297'), Decimal('21.0122')),
    "warsaw": (Decimal('52.2297'), Decimal('21.0122')),
}


def get_city_coordinates(city_name: str) -> Tuple[Decimal, Decimal]:
    city_lower = city_name.lower().strip()
    if city_lower in CITIES:
        return CITIES[city_lower]
    raise ValueError(f"City '{city_name}' not found")


def is_city_name(query: str) -> bool:
    return query.lower().strip() in CITIES