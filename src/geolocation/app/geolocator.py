from geolocation.domain.geolocation import Geolocation
from geolocation.domain.ip_address import IpAddress
from geolocation.domain.geolocation_repository import GeolocationRepository
from geolocation.infra.free_ip_api_repository import FreeIpApiRepository
from shared.exceptions.repository_error import RepositoryError as GeolocationError

class IpAddressGeolocator:
    """A class to get geolocation information for IP addresses."""
    
    def __init__(self, repository: GeolocationRepository | None = None):
        """
        Initialize the IpAddressGeolocator.
        
        Args:
            repository: Optional GeolocationRepository implementation. 
                      If not provided, uses FreeIpApiRepository by default.
        """
        self._repository = repository or FreeIpApiRepository()

    def get_location(self, ip: str | IpAddress) -> Geolocation:
        """
        Get geolocation information for an IP address.
        
        Args:
            ip: The IP address to look up (either as string or IpAddress object)
            
        Returns:
            A Geolocation instance containing the location information
            
        Raises:
            GeolocationError: If the IP is invalid or the repository operation fails
        """
        try:
            ip_address = ip if isinstance(ip, IpAddress) else IpAddress.from_string(ip)
            return self._repository.get_location_by_ip(ip_address)
            
        except Exception as e:
            raise GeolocationError(str(e))


def main():
    """Example usage of the IpAddressGeolocator."""
    test_cases = [
        "187.190.76.70",                    # Mexico
        "8.8.8.8",                          # Google DNS
        IpAddress.from_string("1.1.1.1"),   # Cloudflare DNS
    ]
    
    geolocator = IpAddressGeolocator()
    for ip in test_cases:
        try:
            location = geolocator.get_location(ip)
            print(f"IP: {ip} -> {location}")
        except GeolocationError as e:
            print(f"Error for IP {ip}: {e}")

if __name__ == "__main__":
    main()