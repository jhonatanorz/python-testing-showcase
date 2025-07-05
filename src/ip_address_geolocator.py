import re
from dataclasses import dataclass
from typing import Dict, Optional, Tuple
import requests

class GeolocationError(Exception):
    """Custom exception for geolocation-related errors."""
    pass

@dataclass(frozen=True)
class IpAddress:
    """Immutable value object representing an IPv4 address."""
    
    octets: Tuple[int, int, int, int]
    
    @classmethod
    def from_string(cls, ip_string: str) -> "IpAddress":
        """
        Create an IpAddress instance from a string.
        
        Args:
            ip_string: String representation of an IPv4 address (e.g. "192.168.1.1")
            
        Returns:
            An IpAddress instance
            
        Raises:
            GeolocationError: If the IP address format is invalid
        """
        pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        if not pattern.match(ip_string):
            raise GeolocationError(f"Invalid IP address format: {ip_string}")
        
        try:
            octets = tuple(int(octet) for octet in ip_string.split('.'))
            for octet in octets:
                if octet < 0 or octet > 255:
                    raise GeolocationError(f"Invalid IP address octet: {octet}")
            return cls(octets=octets)  # type: ignore
        except ValueError:
            raise GeolocationError(f"Invalid IP address format: {ip_string}")
    
    def __str__(self) -> str:
        return '.'.join(str(octet) for octet in self.octets)

@dataclass(frozen=True)
class Geolocation:
    """Immutable value object representing geographical location data for an IP address."""
    
    country: str
    city: str
    latitude: float
    longitude: float

    def __str__(self) -> str:
        return f"Location: {self.city}, {self.country} ({self.latitude}, {self.longitude})"

    @classmethod
    def from_dict(cls, data: dict) -> "Geolocation":
        """
        Create a Geolocation instance from a dictionary.
        
        Args:
            data: Dictionary containing location data with keys: countryName, cityName, latitude, longitude
            
        Returns:
            A new Geolocation instance
        """
        return cls(
            country=data["countryName"],
            city=data["cityName"],
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"])
        )

class IpAddressGeolocator:
    """A class to get geolocation information for IP addresses."""
    
    _URL = "https://freeipapi.com/api/json/{ip}"

    def __init__(self):
        """Initialize the IpAddressGeolocator."""
        self._session = requests.Session()

    def get_location(self, ip: str | IpAddress) -> Geolocation:
        """
        Get geolocation information for an IP address.
        
        Args:
            ip: The IP address to look up (either as string or IpAddress object)
            
        Returns:
            A Geolocation instance containing the location information
            
        Raises:
            GeolocationError: If the IP is invalid or the API request fails
        """
        try:
            ip_address = ip if isinstance(ip, IpAddress) else IpAddress.from_string(ip)
            url = self._URL.format(ip=str(ip_address))
            
            response = self._session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return Geolocation.from_dict(data)
            
        except requests.RequestException as e:
            raise GeolocationError(f"Failed to fetch geolocation data: {str(e)}")
        except (ValueError, TypeError) as e:
            raise GeolocationError(f"Invalid response data: {str(e)}")
        except Exception as e:
            raise GeolocationError(f"Unexpected error: {str(e)}")


def main():
    """Example usage of the IpAddressGeolocator."""
    test_cases = [
        "187.190.76.70",                    # Mexico
        "8.8.8.8",                          # Google DNS
        IpAddress.from_string("1.1.1.1"),   # Cloudflare DNS
    ]
    
    for ip in test_cases:
        try:
            location = IpAddressGeolocator().get_location(ip)
            print(f"IP: {ip} -> {location}")
        except GeolocationError as e:
            print(f"Error for IP {ip}: {e}")

if __name__ == "__main__":
    main()