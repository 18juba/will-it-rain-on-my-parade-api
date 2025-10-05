import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from .config import OPEN_METEO_BASE_URL

from datetime import date

class WeatherService:

    @staticmethod
    def get_hourly_data(lat: float, lon: float):
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": [
                "temperature_2m", "relative_humidity_2m", "dew_point_2m",
                "precipitation", "precipitation_probability", "rain", "showers",
                "snowfall", "snow_depth", "weather_code", "pressure_msl",
                "surface_pressure", "wind_speed_10m", "wind_direction_10m",
                "wind_gusts_10m", "evapotranspiration", "et0_fao_evapotranspiration",
                "vapour_pressure_deficit", "cloud_cover_high", "visibility",
                "cloud_cover_mid", "cloud_cover_low", "cloud_cover",
                "wind_speed_80m", "wind_speed_120m", "wind_speed_180m",
                "wind_direction_80m", "wind_direction_120m", "wind_direction_180m",
                "temperature_80m", "temperature_120m", "temperature_180m",
                "soil_temperature_0cm", "soil_temperature_6cm", "soil_temperature_18cm",
                "soil_temperature_54cm", "soil_moisture_0_to_1cm",
                "soil_moisture_1_to_3cm", "apparent_temperature"
            ],
            "forecast_days": 16,
        }

        responses = openmeteo.weather_api(OPEN_METEO_BASE_URL, params=params)
        response = responses[0]
        hourly = response.Hourly()

        time_index = pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )

        data = {"date": time_index}
        for i, variable in enumerate(params["hourly"]):
            data[variable] = hourly.Variables(i).ValuesAsNumpy()

        df = pd.DataFrame(data)
        df = df.where(pd.notnull(df), 0)
        return df.to_dict(orient="records")
    
    def detect_extreme_events(hourly_data):
        alerts = []
        for d in hourly_data:
            event_list = []
            if d["temperature_2m"] is not None and d["temperature_2m"] > 35:
                event_list.append("Heatwave")
            if d["rain"] is not None and d["rain"] > 10:
                event_list.append("Heavy rain")
            if d["wind_speed_10m"] is not None and d["wind_speed_10m"] > 15:
                event_list.append("Strong wind")
            if event_list:
                alerts.append({"datetime": d["date"], "events": event_list})
        return alerts
    
    def WeatherData(lat, lon, date: date):
        
