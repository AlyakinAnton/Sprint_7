import pytest
from utils import create_unique_courier
import requests


@pytest.mark.usefixtures("base_url")
class TestApi:
    @pytest.fixture(autouse=True)
    def setup(self, base_url):
        self.base_url = base_url

    def test_create_courier_successfully(self):
        """Создать курьера"""
        _, _, _ = create_unique_courier(self.base_url)

    def test_duplicate_courier_creation_fails(self):
        """Нельзя создать дублирующего курьера"""
        login, password, first_name = create_unique_courier(self.base_url)
        duplicate_response = requests.post(
            f"{self.base_url}courier",
            json={"login": login, "password": password, "firstName": first_name},
        )
        assert duplicate_response.status_code == 400, \
            f"Повторная регистрация принята: {duplicate_response.text}"

    def test_authenticate_valid_credentials(self):
        """Авторизация курьера с правильными данными"""
        login, password, _ = create_unique_courier(self.base_url)
        auth_response = requests.post(
            f"{self.base_url}courier/login",
            json={"login": login, "password": password},
        )
        assert auth_response.status_code == 200, \
            f"Авторизация провалилась: {auth_response.text}"

    def test_invalid_authentication(self):
        """Авторизация с неправильными данными должна отказать"""
        login, password, _ = create_unique_courier(self.base_url)
        invalid_auth_response = requests.post(
            f"{self.base_url}courier/login",
            json={"login": login + "_invalid", "password": password},
        )
        assert invalid_auth_response.status_code == 400, \
            f"Неправильная проверка аутентификации: {invalid_auth_response.text}"

    def test_create_order_with_color(self):
        """Создание заказа с выбором цвета"""
        order_payload = {
            "firstName": "John",
            "lastName": "Doe",
            "address": "ул. Ленина, дом 1",
            "metroStation": "1",
            "phone": "+79991234567",
            "rentTime": 1,
            "deliveryDate": "2025-01-01",
            "color": ["BLACK"],
        }
        response = requests.post(f"{self.base_url}orders", json=order_payload)
        assert response.status_code == 201, f"Ошибка создания заказа: {response.text}"
        assert "track" in response.json(), "Трек-код не присутствует в ответе"

    def test_create_order_without_color(self):
        """Создание заказа без выбора цвета"""
        order_payload = {
            "firstName": "Jane",
            "lastName": "Smith",
            "address": "ул. Пушкина, дом 1",
            "metroStation": "2",
            "phone": "+79997654321",
            "rentTime": 2,
            "deliveryDate": "2025-01-02",
        }
        response = requests.post(f"{self.base_url}orders", json=order_payload)
        assert response.status_code == 201, f"Ошибка создания заказа: {response.text}"
        assert "track" in response.json(), "Трек-код не присутствует в ответе"

    def test_get_orders_list(self):
        """Получение списка заказов"""
        response = requests.get(f"{self.base_url}orders")
        assert response.status_code == 200, f"Ошибка получения списка заказов: {response.text}"
        assert isinstance(response.json().get("orders"), list), "Список заказов имеет неверный формат"