import requests
import random
import string
import pytest
import allure
from data import *


@pytest.fixture
def base_url():
    return "https://qa-scooter.praktikum-services.ru/api/v1/"


@pytest.fixture
def registered_courier(base_url):
    login, password, first_name = create_unique_courier(base_url)
    return login, password, first_name


def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def create_unique_courier(base_url):
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post(f'{base_url}/courier', json=payload)
    if response.status_code == 201:
        return login, password, first_name
    else:
        return [], [], []


# ==========================================
# Класс для тестов регистрации курьера
# ==========================================

class TestRegistration:
    @allure.title("Создание курьера проходит успешно")
    def test_create_courier_successfully(self, base_url):
        with allure.step("Создаю курьера"):
            login, password, first_name = create_unique_courier(base_url)
        with allure.step("Проверяю статус ответа"):
            assert login is not None, "Логин не был создан"
            assert password is not None, "Пароль не был создан"
            assert first_name is not None, "Имя не было создано"

    @allure.title("Ошибка при регистрации без обязательных полей")
    def test_create_courier_without_required_fields(self, base_url):
        with allure.step("Отправляю запрос без обязательных полей"):
            response = requests.post(f'{base_url}/courier', json={})
        with allure.step("Проверяю статус ответа"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Ошибка при регистрации с уже существующим логином")
    def test_create_duplicate_courier(self, base_url):
        with allure.step("Создаю первого курьера"):
            login, password, first_name = create_unique_courier(base_url)

        with allure.step("Пытаюсь повторно создать курьера с тем же логином"):
            payload = {
                "login": login,
                "password": password,
                "firstName": first_name
            }
            response = requests.post(f'{base_url}/courier', json=payload)

        with allure.step("Проверяю статус ответа"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"


# ==========================================
# Класс для тестов авторизации курьера
# ==========================================

class TestAuthentication:
    @allure.title("Ошибка при авторизации с неверными данными")
    def test_incorrect_authorization(self, base_url):
        with allure.step("Отправляю запрос с неверными данными"):
            response = requests.post(f'{base_url}/courier/login', json={"login": "wrong", "password": "wrong"})
        with allure.step("Проверяю статус ответа"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Успешная авторизация курьера")
    def test_successful_authorization(self, base_url, registered_courier):
        login, password, _ = registered_courier
        with allure.step("Осуществляю авторизацию"):
            response = requests.post(f'{base_url}/courier/login', json={"login": login, "password": password})
        with allure.step("Проверяю статус ответа"):
            assert response.status_code == 200
            assert "id" in response.json()


# ==========================================
# Класс для тестов работы с заказами
# ==========================================

class TestOrders:
    ORDER_PAYLOADS = [
        ({"firstName": "John", "lastName": "Doe", "address": "ул. Ленина, дом 1", "metroStation": "1",
          "phone": "+79991234567", "rentTime": 1, "deliveryDate": "2025-01-01", "color": ["BLACK"]},
         "Создание заказа с выбором цвета"),
        ({"firstName": "Jane", "lastName": "Smith", "address": "ул. Пушкина, дом 1", "metroStation": "2",
          "phone": "+79997654321", "rentTime": 2, "deliveryDate": "2025-01-02"}, "Создание заказа без выбора цвета"),
    ]

    @pytest.mark.parametrize("payload,title", ORDER_PAYLOADS)
    @allure.title("{title}")
    def test_create_order(self, base_url, payload, title):
        with allure.step("Создаю заказ"):
            response = requests.post(f'{base_url}/orders', json=payload)
        with allure.step("Проверяю статус ответа"):
            assert response.status_code == 201
            assert "track" in response.json()

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self, base_url):
        with allure.step("Получаю список заказов"):
            response = requests.get(f'{base_url}/orders')
        with allure.step("Проверяю статус ответа"):
            assert response.status_code == 200
            assert isinstance(response.json()["orders"], list)