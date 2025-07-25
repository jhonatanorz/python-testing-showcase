import requests

from geolocation.domain.geolocation import Geolocation
from geolocation.domain.ip_address import IpAddress
from geolocation.domain.geolocation_repository import GeolocationRepository
from shared.exceptions.repository_error import RepositoryError

class FreeIpApiRepository(GeolocationRepository):
    """Implementation of GeolocationRepository using the Free IP API."""
    
    _URL = "https://freeipapi.com/api/json/{ip}"

    def __init__(self):
        """Initialize the repository with a requests session."""
        self._session = requests.Session()

    def get_location_by_ip(self, ip: IpAddress) -> Geolocation:
        """
        Get geolocation information for an IP address from Free IP API.
        
        Args:
            ip: The IP address to look up
            
        Returns:
            A Geolocation instance containing the location information
            
        Raises:
            RepositoryError: If the API request fails or returns invalid data
        """
        try:
            url = self._URL.format(ip=str(ip))
            
            response = self._session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return Geolocation.from_dict(data)
            
        except requests.RequestException as e:
            raise RepositoryError(f"Failed to fetch geolocation data: {str(e)}")
        except (ValueError, TypeError) as e:
            raise RepositoryError(f"Invalid response data: {str(e)}")
        except Exception as e:
            raise RepositoryError(f"Unexpected error: {str(e)}") 