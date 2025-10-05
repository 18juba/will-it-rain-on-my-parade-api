import requests
import pandas as pd
from .config import POWER_NASA_URL

class WeatherService:

    @staticmethod
    def get_data(lat, lon, start_date: str, end_date: str):
        params = {
            "start": start_date,
            "end": end_date,
            "latitude": lat,
            "longitude": lon,
            "community": "RE",
            "parameters": "T2M,WS2M,RH2M,PRECTOTCORR",
            "format": "JSON"
        }

        resposta = requests.get(POWER_NASA_URL, params=params)
        dados = resposta.json()

        parametros = dados["properties"]["parameter"]

        df = pd.DataFrame({
            "Data": list(parametros["T2M"].keys()),
            "Temperatura(°C)": list(parametros["T2M"].values()),
            "Vento(m/s)": list(parametros["WS2M"].values()),
            "Umidade(%)": list(parametros["RH2M"].values()),
            "Chuva(mm)": list(parametros["PRECTOTCORR"].values())
        })

        df["Data"] = pd.to_datetime(df["Data"], format="%Y%m%d")

        df.set_index("Data", inplace=True)

        return df.describe().to_dict()
    
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

    @staticmethod
    def WeatherData(lat, lon, start_date: str, end_date: str):
        return WeatherService.get_data(lat, lon, start_date, end_date)
