from dataclasses import dataclass

@dataclass(frozen=True)
class Geolocation:
    """Immutable value object representing geographical location data."""
    
    country: str
    city: str
    latitude: float
    longitude: float

    @classmethod
    def from_dict(cls, data: dict) -> "Geolocation":
        """
        Create a Geolocation instance from a dictionary.
        
        Args:
            data: Dictionary containing location data
            
        Returns:
            A new Geolocation instance
        """
        return cls(
            country=data["countryName"],
            city=data["cityName"],
            latitude=float(data["latitude"]),
            longitude=float(data["longitude"])
        )

    def __str__(self) -> str:
        return f"Location: {self.city}, {self.country} ({self.latitude}, {self.longitude})" 