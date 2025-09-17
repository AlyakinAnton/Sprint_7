import pytest


@pytest.fixture(scope="session")
def base_url():
    """Возвращает базовую ссылку на API."""
    return "https://qa-scooter.praktikum-services.ru/api/v1/"