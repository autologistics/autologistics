from .samsara_api import get_vehicle_from_id
from .base import get_all_updates, check_speed, check_location, calculate_eta_status, get_formatted_message, \
    login_to_system, go_to_remover, save_update, get_details, get_assets

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_api_samsara_info():
    print('Samsara')
    updates = get_all_updates()
    messages = []
    for update in updates:
        vehicle_id = update.vehicle_id
        name = update.name
        data = get_vehicle_from_id(name, vehicle_id)  # (name, fuel, speed, updated, location)
        live_share = update.live_share
        link = update.link
        broker = update.broker
        destination = update.destination
        planned_time = update.planned_time
        speed = data['speed']
        status = check_speed(speed)
        fuel = data['fuel']
        current_location = data['current_location']
        eta, eta_value = check_location(current_location, destination)
        eta_status = calculate_eta_status(eta_value, planned_time)
        updated_at = data['updated_at']
        message = get_formatted_message(name, link, live_share, destination, planned_time, status, fuel, eta, eta_value,
                                        eta_status, updated_at, current_location, broker)
        print(message)
        messages.append(tuple(message))
        save_update(update, name, vehicle_id, current_location, eta, eta_status, status, fuel, link, live_share,
                    updated_at)
    return tuple(messages)


def get_selenium_info():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    login_to_system(driver)
    go_to_remover(driver)
    info = get_assets(driver)
    messages = get_details(info, driver)
    driver.close()
    driver.quit()
    return tuple(messages)


def get_search_samsara_info(update):
    vehicle_id = update.vehicle_id
    name = update.name
    data = get_vehicle_from_id(name, vehicle_id)  # (name, fuel, speed, updated, location)
    live_share = update.live_share
    link = update.link
    broker = update.broker
    destination = update.destination
    planned_time = update.planned_time
    speed = data['speed']
    status = check_speed(speed)
    fuel = data['fuel']
    current_location = data['current_location']
    eta, eta_value = check_location(current_location, destination)
    eta_status = calculate_eta_status(eta_value, planned_time)
    updated_at = data['updated_at']
    message = get_formatted_message(name, link, live_share, destination, planned_time, status, fuel, eta, eta_value,
                                    eta_status, updated_at, current_location, broker)
    save_update(update, name, vehicle_id, current_location, eta, eta_status, status, fuel, link, live_share,
                updated_at)
    return message
