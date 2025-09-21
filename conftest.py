import pytest
from tests.helpers import create_unique_courier

@pytest.fixture
def registered_courier(request):
    base_url = request.config.getoption('--base-url') or "https://qa-scooter.praktikum-services.ru/api/v1/"
    login, password, first_name = create_unique_courier(base_url)
    return login, password, first_name