from dataclasses import dataclass
from typing import Tuple

from shared.exceptions.validation_error import ValidationError

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
            ValidationError: If the IP address format is invalid
        """
        try:
            octets = tuple(int(octet) for octet in ip_string.split('.'))
            if len(octets) != 4:
                raise ValidationError(f"Invalid IP address format: {ip_string}")
            
            for octet in octets:
                if octet < 0 or octet > 255:
                    raise ValidationError(f"Invalid IP address octet: {octet}")
                    
            return cls(octets=octets)  # type: ignore
            
        except (ValueError, IndexError):
            raise ValidationError(f"Invalid IP address format: {ip_string}")
    
    def __str__(self) -> str:
        return '.'.join(str(octet) for octet in self.octets) 