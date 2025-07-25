import pytest
from dataclasses import FrozenInstanceError

from geolocation.domain.ip_address import IpAddress
from shared.exceptions.validation_error import ValidationError


class TestIpAddressCreation:
    """Test cases for IpAddress creation and validation."""

    def test_should_raise_error_when_ip_has_invalid_format(self):
        """Test validation of IP address string format."""
        invalid_ips = [
            "192.168.1",  # Missing octet
            "192.168.1.1.1",  # Extra octet
            "192.168.1.",  # Empty octet
            "192.168..1",  # Empty octet
            "192.168",  # Too few octets
            "a.b.c.d",  # Non-numeric
            "192.168.1.abc",  # Mixed numeric/non-numeric
            "",  # Empty string
            "192,168,1,1",  # Wrong separator
        ]
        
        for invalid_ip in invalid_ips:
            with pytest.raises(ValidationError, match="Invalid IP address format"):
                IpAddress.from_string(invalid_ip)

    def test_should_raise_error_when_octets_out_of_range(self):
        """Test validation of octet values."""
        invalid_ips = [
            "256.1.2.3",  # > 255
            "1.256.2.3",
            "1.2.256.3",
            "1.2.3.256",
            "-1.2.3.4",  # Negative
            "1.-2.3.4",
            "1.2.-3.4",
            "1.2.3.-4",
        ]
        
        for invalid_ip in invalid_ips:
            with pytest.raises(ValidationError, match="Invalid IP address octet"):
                IpAddress.from_string(invalid_ip)

    def test_should_create_ip_from_valid_string(self):
        """Test creating an IP address from a valid string."""
        ip = IpAddress.from_string("192.168.1.1")
        assert ip.octets == (192, 168, 1, 1)

   
    def test_should_create_ip_from_valid_octets(self):
        """Test creating an IP address from valid octets."""
        ip = IpAddress(octets=(192, 168, 1, 1))
        assert ip.octets == (192, 168, 1, 1)


    """Test cases for IpAddress string representation."""

    def test_should_convert_ip_to_string_correctly(self):
        """Test string representation of an IP address."""
        test_cases = [
            ((192, 168, 1, 1), "192.168.1.1"),
            ((8, 8, 8, 8), "8.8.8.8"),
            ((127, 0, 0, 1), "127.0.0.1"),
            ((255, 255, 255, 255), "255.255.255.255"),
            ((0, 0, 0, 0), "0.0.0.0"),
        ]
        
        for octets, expected in test_cases:
            ip = IpAddress(octets=octets)
            assert str(ip) == expected

class TestIpAddressImmutability:
    """Test cases for IpAddress immutability."""

    def test_should_be_immutable(self):
        """Test that IpAddress instances are immutable."""
        ip = IpAddress(octets=(192, 168, 1, 1))
        with pytest.raises(FrozenInstanceError):
            ip.octets = (192, 168, 1, 2)  # type: ignore

    def test_should_have_immutable_octets(self):
        """Test that the octets tuple is immutable."""
        ip = IpAddress(octets=(192, 168, 1, 1))
        with pytest.raises(TypeError):  # Tuple is immutable
            ip.octets[0] = 10  # type: ignore 