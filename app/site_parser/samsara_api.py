import requests
import pytz
from core.settings import SAMSARA_API, TIME_ZONE
from datetime import datetime

timezone = pytz.timezone(TIME_ZONE)
headers = {
    "accept": "application/json",
    "authorization": f"Bearer  {SAMSARA_API}"
}


# TODO: Работа с API Самсары
def get_vehicle_from_id(name, vehicle_id):
    url = f"https://api.samsara.com/fleet/vehicles/stats?vehicleIds={vehicle_id}&types=gps,fuelPercents"
    data = list(requests.get(url, headers=headers).json()['data'])
    if not data:  # При отключенном устройстве
        return {
            'name': name,
            'fuel': 'No Information',
            'speed': 'No Information',
            'updated_at': datetime.now(tz=timezone),
            'current_location': 'No Information'
        }
    else:
        fuel = data[0]['fuelPercent']['value'] if 'fuelPercent' in data[0] else 'No Information'    # Получение Информации о Запасе Топлива
        updated_at = data[0]['gps']['time']  # Получение Информации об последнем обновлении
        speed = data[0]['gps']['speedMilesPerHour']  # Получение Информации о Скорости передвижение
        current_location = data[0]['gps']["reverseGeo"]["formattedLocation"]  # Получение информации о местонахождении
        return {
            'name': name,
            'fuel': fuel,
            'speed': speed,
            'updated_at': updated_at,
            'current_location': current_location
        }
