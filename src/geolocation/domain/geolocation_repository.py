from abc import ABC, abstractmethod
from geolocation.domain.geolocation import Geolocation
from geolocation.domain.ip_address import IpAddress

class GeolocationRepository(ABC):
    """Interface for geolocation data access."""
    
    @abstractmethod
    def get_location_by_ip(self, ip: IpAddress) -> Geolocation:
        """
        Get geolocation information for an IP address.
        
        Args:
            ip: The IP address to look up
            
        Returns:
            A Geolocation instance containing the location information
            
        Raises:
            RepositoryError: If there's an error fetching the geolocation data
        """
        pass 