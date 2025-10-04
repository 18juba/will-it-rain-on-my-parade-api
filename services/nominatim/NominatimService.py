import requests
from .config import NOMINATIM_BASE_URL, USER_AGENT, TIMEOUT

class NominatimService:
    @staticmethod
    def reverse_geocode(lat, lon):
        """Search for an address based on latitude and longitude"""
        url = f"{NOMINATIM_BASE_URL}/reverse"
        params = {
            "lat": lat,
            "lon": lon,
            "format": "json",
            "addressdetails": 1,
        }
        headers = {"User-Agent": USER_AGENT}

        response = requests.get(url, params=params, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def LocationData(lat, lon):
        """Search for main location data in reverse_geocode"""
        result = NominatimService.reverse_geocode(lat, lon)
        address = result.get("address", {})

        country = address.get("country")
        state = address.get("state")
        city = address.get("city") or address.get("town") or address.get("village") or address.get("municipality")
        extra = result.get("display_name")

        location_data = {
            "country": country if country else None,
            "state": state if state else None,
            "city": city if city else None,
            "extra": extra if extra else None
        }

        return location_data