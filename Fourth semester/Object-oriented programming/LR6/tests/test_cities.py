import pytest
from decimal import Decimal
from shared.locations.cities import get_city_coordinates, is_city_name, CITIES

class TestCities:
    @pytest.mark.parametrize("city, expected_lat, expected_lon", [
        ("Минск", Decimal('53.9'), Decimal('27.5667')),
        ("минск", Decimal('53.9'), Decimal('27.5667')),
        ("Лондон", Decimal('51.5074'), Decimal('-0.1278')),
        ("Tokyo", Decimal('35.6762'), Decimal('139.6503')),
    ])
    def test_get_city_coordinates(self, city, expected_lat, expected_lon):
        lat, lon = get_city_coordinates(city)
        assert lat == expected_lat
        assert lon == expected_lon

    def test_invalid_city_raises(self):
        with pytest.raises(ValueError, match="not found"):
            get_city_coordinates("Нью-Йорк")

    @pytest.mark.parametrize("query", ["Варшава", "warsaw", " Shanghai "])
    def test_is_city_name_true(self, query):
        assert is_city_name(query) is True

    def test_is_city_name_false(self):
        assert is_city_name("Париж") is False