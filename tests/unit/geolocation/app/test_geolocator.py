import pytest
from unittest.mock import Mock

from geolocation.app.geolocator import IpAddressGeolocator
from geolocation.domain.ip_address import IpAddress
from geolocation.domain.geolocation import Geolocation
from shared.exceptions.repository_error import RepositoryError

@pytest.fixture
def mock_repository():
    return Mock()

@pytest.fixture
def geolocator(mock_repository):
    return IpAddressGeolocator(repository=mock_repository)

def test_get_location_with_invalid_ip_raises_error(geolocator):
    with pytest.raises(RepositoryError):
        geolocator.get_location("invalid.ip.address")

def test_get_location_when_repository_fails(geolocator, mock_repository):
    test_ip = "8.8.8.8"
    
    mock_repository.get_location_by_ip.side_effect = Exception("API Error")
    
    with pytest.raises(RepositoryError) as exc_info:
        geolocator.get_location(test_ip)
    
    assert "API Error" in str(exc_info.value) 

def test_get_location_with_valid_ip_string(geolocator, mock_repository):
    
    test_ip = "8.8.8.8"
    expected_location = Geolocation(
        country="US",
        city="Mountain View",
        latitude=37.4056,
        longitude=-122.0775
    )

    mock_repository.get_location_by_ip.return_value = expected_location
    
    result = geolocator.get_location(test_ip)
    
    assert result == expected_location
    mock_repository.get_location_by_ip.assert_called_once()

def test_get_location_with_ip_address_object(geolocator, mock_repository):
    test_ip = IpAddress.from_string("1.1.1.1")
  
    expected_location = Geolocation(
        country="US",
        city="Los Angeles",
        latitude=34.0522,
        longitude=-118.2437
    )
  
    mock_repository.get_location_by_ip.return_value = expected_location
    
    result = geolocator.get_location(test_ip)
    
    # Assert
    assert result == expected_location
    mock_repository.get_location_by_ip.assert_called_once_with(test_ip)