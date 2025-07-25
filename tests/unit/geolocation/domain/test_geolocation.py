import pytest

from geolocation.domain.geolocation import Geolocation


class TestGeolocationCreation:
    """Test cases for Geolocation creation and validation."""

    def test_should_create_geolocation_with_valid_data(self):
        """Test creating a Geolocation with valid data."""
        location = Geolocation(
            country="United States",
            city="New York",
            latitude=40.7128,
            longitude=-74.0060
        )
        
        assert location.country == "United States"
        assert location.city == "New York"
        assert location.latitude == 40.7128
        assert location.longitude == -74.0060

    def test_should_create_geolocation_from_valid_dict(self):
        """Test creating a Geolocation from a valid dictionary."""
        data = {
            "countryName": "United States",
            "cityName": "New York",
            "latitude": "40.7128",
            "longitude": "-74.0060"
        }
        
        location = Geolocation.from_dict(data)
        
        assert location.country == "United States"
        assert location.city == "New York"
        assert location.latitude == 40.7128
        assert location.longitude == -74.0060

    def test_should_raise_error_when_dict_has_missing_keys(self):
        """Test validation of required dictionary keys."""
        invalid_data_cases = [
            {},  # Empty dict
            {"countryName": "US"},  # Missing most fields
            {  # Missing longitude
                "countryName": "US",
                "cityName": "NY",
                "latitude": "40.7128"
            },
            {  # Missing latitude
                "countryName": "US",
                "cityName": "NY",
                "longitude": "-74.0060"
            },
            {  # Missing city
                "countryName": "US",
                "latitude": "40.7128",
                "longitude": "-74.0060"
            },
            {  # Missing country
                "cityName": "NY",
                "latitude": "40.7128",
                "longitude": "-74.0060"
            }
        ]
        
        for invalid_data in invalid_data_cases:
            with pytest.raises(KeyError):
                Geolocation.from_dict(invalid_data)

    def test_should_raise_error_when_coordinates_are_invalid(self):
        """Test validation of coordinate values."""
        invalid_data_cases = [
            {  # Non-numeric latitude
                "countryName": "US",
                "cityName": "NY",
                "latitude": "invalid",
                "longitude": "-74.0060"
            },
            {  # Non-numeric longitude
                "countryName": "US",
                "cityName": "NY",
                "latitude": "40.7128",
                "longitude": "invalid"
            }
        ]
        
        for invalid_data in invalid_data_cases:
            with pytest.raises(ValueError):
                Geolocation.from_dict(invalid_data)


class TestGeolocationStringRepresentation:
    """Test cases for Geolocation string representation."""

    def test_should_format_string_representation_correctly(self):
        """Test string representation of a Geolocation."""
        test_cases = [
            (
                Geolocation("United States", "New York", 40.7128, -74.0060),
                "Location: New York, United States (40.7128, -74.006)"
            ),
            (
                Geolocation("Japan", "Tokyo", 35.6762, 139.6503),
                "Location: Tokyo, Japan (35.6762, 139.6503)"
            ),
            (
                Geolocation("Brazil", "Rio de Janeiro", -22.9068, -43.1729),
                "Location: Rio de Janeiro, Brazil (-22.9068, -43.1729)"
            )
        ]
        
        for location, expected in test_cases:
            assert str(location) == expected


class TestGeolocationImmutability:
    """Test cases for Geolocation immutability."""

    def test_should_be_immutable(self):
        """Test that Geolocation instances are immutable."""
        location = Geolocation("US", "NY", 40.7128, -74.0060)
        
        with pytest.raises(Exception):  # dataclass frozen=True raises AttributeError or FrozenInstanceError
            location.country = "Canada"
            
        with pytest.raises(Exception):
            location.city = "Toronto"
            
        with pytest.raises(Exception):
            location.latitude = 43.6532
            
        with pytest.raises(Exception):
            location.longitude = -79.3832 