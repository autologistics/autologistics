import time

import pytz
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime, timedelta

from app.models import Update
from .google_api import calculate_distance_and_duration
from .samsara_api import get_vehicle_from_id
from core.settings import TIME_ZONE, LOGIN, PASSWORD, URL, REMOVER

timezone = pytz.timezone(TIME_ZONE)


# Функция для получения всех Ассетов
def get_all_updates():
    updates = [update for update in Update.objects.all()]
    return updates


# Функция для сохранения Ассета
def save_update(update, name, vehicle_id, current_location, eta, eta_status, status, fuel, link, live_share,
                updated_at):
    update.name = name
    update.vehicle_id = vehicle_id
    update.current_location = current_location
    update.eta = eta
    update.eta_status = eta_status
    update.status = status
    update.fuel = fuel
    update.link = link
    update.live_share = live_share
    update.updated_at = updated_at
    update.save()


def check_speed(speed):
    if speed == 'No Information':
        return 'No Information'
    elif speed <= 5:
        return 'Stationary'
    else:
        return 'Rolling'


def check_location(current_location, destination):
    if current_location == 'No Information' or current_location == 'No Information' and destination == '-' or destination is None:
        eta, eta_value = '-', '-'
    else:
        eta = calculate_distance_and_duration(current_location, destination)
        if type(eta) is list or type(eta) is tuple:
            eta, eta_value = eta
        else:
            return eta, '-'
    return eta, eta_value


def calculate_eta_status(eta_value, planned_time):
    if eta_value == '-' and planned_time is None or eta_value == '-' or planned_time is None:
        return '-'
    else:
        current_time = datetime.now(timezone)
        threshold_minutes = 5
        actual_time = current_time + timedelta(seconds=eta_value)
        if actual_time > planned_time + timedelta(minutes=threshold_minutes):
            eta_status = 'Late'
        else:
            eta_status = 'On Time'
        return eta_status


# Функция для получения форматированного сообщения
def get_formatted_message(name, link, live_share, destination, planned_time, status, fuel, eta, eta_value, eta_status,
                          updated_at, current_location, broker):

    text = f'''<b><a href="{link}">#{name}</a></b>
<b>Destination</b>: {destination}
<b>Current Location</b>: {current_location}
<b>Planned Time</b>: {planned_time}
<b>Duration Value</b>: {eta_value}
<b>ETA</b>: {eta}
<b>ETA Status</b>: {eta_status}
<b>Status</b>: {status}
<b>Fuel</b>: {fuel}
<b>Updated At</b>: {updated_at}
<b>Live Share</b>: {live_share}'''
    if eta_status == 'Late' and broker.mail:
        return text, True, name, broker.mail
    else:
        return text, False, name


# Функция для Авторизации в Самсаре
def login_to_system(driver):
    driver.get(URL)
    time.sleep(7)
    username_field = driver.find_element(By.CLASS_NAME, 'Input')
    username_field.send_keys(LOGIN)
    username_field.send_keys(Keys.ENTER)
    time.sleep(5)
    password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
    password_field.send_keys(PASSWORD)
    password_field.send_keys(Keys.ENTER)
    print('[+] Authorized')
    time.sleep(25)


# Фунция для удаления не нужных ссылок
def go_to_remover(driver):
    print('[+] Remover')
    updates = Update.objects.all()
    truck_numbers = [update.name for update in updates]
    driver.get(REMOVER)
    time.sleep(20)
    for truck_number in truck_numbers:
        search_field = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
        search_field.send_keys(truck_number)
        time.sleep(2)
        try:
            remove_button = driver.find_element(By.CSS_SELECTOR,
                                                'button[class="Button Button--md Button--danger"]')
            driver.execute_script("arguments[0].click();", remove_button)
            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
        except Exception as e:
            pass
        search_field.clear()


def get_assets(driver):
    driver.get('https://cloud.samsara.com/')
    time.sleep(10)
    pages_element = driver.find_element(By.CLASS_NAME, "pages")
    page_count = int(pages_element.find_elements(By.TAG_NAME, 'button')[-1].get_attribute('data-value'))
    info = []
    while page_count >= 0:
        names = [name.text for name in driver.find_elements(By.CLASS_NAME, 'fleet-vehicle-name')]
        links = [link.get_attribute('href') for link in
                 driver.find_elements(By.CLASS_NAME, 'fleet-list-entry')]
        vehicle_ids = [vehicle_id.split('/')[6] for vehicle_id in links]

        for i in range(len(links) - 1):
            info.append({
                'name': names[i],
                'link': links[i],
                'vehicle_id': vehicle_ids[i]
            })
        try:
            driver.find_element(By.CLASS_NAME, 'next').click()
            time.sleep(10)
        except:
            pass
        page_count -= 1
        time.sleep(5)
    return tuple(info)


# Функция для получения Live Share
def get_live_share(destination, driver, chances=2):
    try:
        if destination is not None or destination!='-':
            button = driver.find_element(By.CSS_SELECTOR, 'button[class="Button Button--block Button--md"]')
            button.click()
            time.sleep(5)
            driver.find_element(By.CSS_SELECTOR, 'label[class="Checkbox"').click()
            driver.find_element(By.CSS_SELECTOR, 'div[class="Select-control"').click()
            address_input = driver.find_element(By.CSS_SELECTOR, 'input[role="combobox"]')
            address_input.send_keys(destination)
            time.sleep(5)

            select = driver.find_element(By.CSS_SELECTOR,
                                         'div[class="DropdownSelect-option Select-option is-focused"')
            select.click()
            time.sleep(10)
            button1 = driver.find_element(By.CSS_SELECTOR, 'button[class="Button Button--md Button--primary"]')
            button1.click()
            time.sleep(3)
            location_element = driver.find_element(By.TAG_NAME, 'input')
            location_link = location_element.get_attribute('value')  # Получение Ссылки
            button1 = driver.find_elements(By.CSS_SELECTOR, 'button[class="Button Button--md Button--primary"]')
            try:
                button1[1].click()
            except:
                button1[0].click()
            return location_link
        else:
            button = driver.find_element(By.CSS_SELECTOR, 'button[class="Button Button--block Button--md"]')
            time.sleep(3)
            button.click()
            time.sleep(5)
            button1 = driver.find_element(By.CSS_SELECTOR, 'button[class="Button Button--md Button--primary"]')
            button1.click()
            time.sleep(3)
            location_element = driver.find_element(By.TAG_NAME, 'input')
            location_link = location_element.get_attribute('value')  # Получение Ссылки
            button1 = driver.find_elements(By.CSS_SELECTOR, 'button[class="Button Button--md Button--primary"]')
            try:
                button1[1].click()
            except:
                button1[0].click()
            return location_link
    except:
        if chances != 0:
            return get_live_share(destination, driver, chances - 1)
        else:
            return 'Could not Create!!!'


# Функция для получения Детальной Информации
def get_details(info, driver):
    print('[+] Get Detail')
    messages = []
    for i in info:
        link = i['link']
        name = i['name']
        vehicle_id = i['vehicle_id']
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)
        time.sleep(5)
        truck, _ = Update.objects.get_or_create(name=name)
        data = get_vehicle_from_id(name, vehicle_id)
        destination = truck.destination
        if data['current_location'] == 'No Information':
            live_share = 'Could not Create!!!'
        else:
            live_share = get_live_share(destination, driver)
        broker = truck.broker
        planned_time = truck.planned_time
        speed = data['speed']
        status = check_speed(speed)
        fuel = data['fuel']
        current_location = data['current_location']
        eta, eta_value = check_location(current_location, destination)
        eta_status = calculate_eta_status(eta_value, planned_time)
        updated_at = data['updated_at']
        message = get_formatted_message(name, link, live_share, destination, planned_time, status, fuel, eta,
                                        eta_value,
                                        eta_status, updated_at, current_location, broker)
        messages.append(message)
        print(message)
        save_update(truck, name, vehicle_id, current_location, eta, eta_status, status, fuel, link, live_share,
                    updated_at)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    return messages
