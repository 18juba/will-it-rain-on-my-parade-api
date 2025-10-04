from fastapi import FastAPI, Query
from services.nominatim.NominatimService import NominatimService

app = FastAPI()

@app.get("/local_info")
def get_local_info(lat: str = Query(..., description="Latitude"), lon: str = Query(..., description="Longitude")):
    address = {
        "location": NominatimService.LocationData(lat, lon),
    }
    return address


@app.get("/dashboard")
def get_dashboard(lat: str = Query(..., description="Latitude"), lon: str = Query(..., description="Longitude")):
    dashboard_data = {
        "data": {
            "location_card": NominatimService.LocationData(lat, lon),
        }
    }
    return dashboard_data
