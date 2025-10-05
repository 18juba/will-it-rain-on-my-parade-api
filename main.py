from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from services.openmeteo.WeatherService import WeatherService
from services.nominatim.NominatimService import NominatimService

from datetime import date

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/local_info")
def get_local_info(lat: str = Query(..., description="Latitude"), lon: str = Query(..., description="Longitude")):
    address = {
        "location": NominatimService.LocationData(lat, lon),
    }
    return address


@app.get("/dashboard")
def get_dashboard(lat: float = Query(..., description="Latitude"), lon: float = Query(..., description="Longitude")):
    dashboard_data = {
        "data": {
            "location_card": NominatimService.LocationData(lat, lon),
            "hourly_data": WeatherService.get_hourly_data(lat, lon)
        }
    }
    return dashboard_data
