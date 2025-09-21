# tests/test_api.py
import requests
import pytest
import allure
from helpers import create_unique_courier
from data import BASE_URL

# ======== РЕГИСТРАЦИЯ КУРЬЕРА ========

class TestRegistration:
    @allure.title("Создание курьера проходит успешно")
    def test_create_courier_successfully(self):
        login, password, first_name = create_unique_courier(BASE_URL)
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(f"{BASE_URL}/courier", json=payload)

        with allure.step("Проверяю статус ответа"):
            assert login is not None, "Логин не был создан"
            assert password is not None, "Пароль не был создан"
            assert first_name is not None, "Имя не было создано"
            assert response.status_code == 201
            assert response.json()["ok"] is True

    @allure.title("Ошибка при регистрации без обязательных полей")
    def test_create_courier_without_required_fields(self):
        with allure.step("Отправляю запрос без обязательных полей"):
            response = requests.post(f"{BASE_URL}/courier", json={})
        with allure.step("Проверяю статус ответа"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Ошибка при создании дублирующего курьера")
    def test_create_duplicate_courier(self):
        login, password, first_name = create_unique_courier(BASE_URL)
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(f"{BASE_URL}/courier", json=payload)

        with allure.step("Проверяю статус ответа"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для создания учетной записи"

# ====== АВТОРИЗАЦИЯ КУРЬЕРА ========

class TestAuthentication:
    @allure.title("Успешная авторизация курьера")
    def test_successful_authorization(self, registered_courier):
        login, password, _ = registered_courier
        with allure.step("Осуществляю авторизацию"):
            response = requests.post(f"{BASE_URL}/courier/login", json={"login": login, "password": password})
        with allure.step("Проверяю статус ответа"):
            assert response.status_code == 200
            assert "id" in response.json()

    @allure.title("Ошибка при авторизации с неверными данными")
    def test_incorrect_authorization(self):
        with allure.step("Отправляю запрос с неверными данными"):
            response = requests.post(f"{BASE_URL}/courier/login", json={"login": "wrong_login", "password": "wrong_password"})
        with allure.step("Проверяю статус ответа"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Ошибка при авторизации с отсутствием обязательных полей")
    def test_empty_authorization(self):
        with allure.step("Отправляю запрос без обязательных полей"):
            response = requests.post(f"{BASE_URL}/courier/login", json={})
        with allure.step("Проверяю статус ответа"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Ошибка при авторизации несуществующего пользователя")
    def test_non_existent_user_authorization(self):
        with allure.step("Пытаюсь авторизоваться несуществующим пользователем"):
            response = requests.post(f"{BASE_URL}/courier/login", json={"login": "non_existing_user", "password": "random_password"})
        with allure.step("Проверяю статус ответа"):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для входа"

# ======== СОЗДАНИЕ ЗАКАЗА ========

ORDER_PAYLOADS = [
    ({"firstName": "John", "lastName": "Doe", "address": "ул. Ленина, дом 1", "metroStation": "1", "phone": "+79991234567", "rentTime": 1, "deliveryDate": "2025-01-01", "color": ["BLACK"]}, "Создание заказа с одним цветом"),
    ({"firstName": "Jane", "lastName": "Smith", "address": "ул. Пушкина, дом 1", "metroStation": "2", "phone": "+79997654321", "rentTime": 2, "deliveryDate": "2025-01-02", "color": ["BLACK", "GREY"]}, "Создание заказа с двумя цветами"),
    ({"firstName": "Bob", "lastName": "Brown", "address": "ул. Некрасова, дом 1", "metroStation": "3", "phone": "+79995554444", "rentTime": 3, "deliveryDate": "2025-01-03"}, "Создание заказа без выбора цвета"),
]

class TestOrders:
    @pytest.mark.parametrize("payload,title", ORDER_PAYLOADS)
    @allure.title("{title}")
    def test_create_order(self, payload, title):
        with allure.step("Создаю заказ"):
            response = requests.post(f"{BASE_URL}/orders", json=payload)
        with allure.step("Проверяю статус ответа"):
            assert response.status_code == 201
            assert "track" in response.json()

    @allure.title("Получение списка заказов")
    def test_get_orders_list(self):
        with allure.step("Получаю список заказов"):
            response = requests.get(f"{BASE_URL}/orders")
        with allure.step("Проверяю статус ответа"):
            assert response.status_code == 200
            assert isinstance(response.json()["orders"], list)