import googlemaps
import pytz
from datetime import datetime
from core.settings import GOOGLE_API, TIME_ZONE

timezone = pytz.timezone(TIME_ZONE)


def calculate_distance_and_duration(start_address, end_address):
    gmaps = googlemaps.Client(key=GOOGLE_API)
    try:
        directions_result = gmaps.directions(start_address, end_address, mode="driving",
                                             departure_time=datetime.now(timezone))
        if len(directions_result) > 0:
            # Парсим расстояние из ответа API
            distance = directions_result[0]['legs'][0]['distance']['text']
            duration_value = directions_result[0]['legs'][0]['duration']['value']
            duration = directions_result[0]['legs'][0]['duration']['text']
            return f'Distance: {distance}. Estimated Time of Arrival: {duration}', duration_value
        else:
            return "Маршрут не найден."

    except Exception as e:
        return f"Ошибка при запросе маршрута: {e}"
