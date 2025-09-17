import random
import string
import requests


def generate_random_string(length):
    """Генерирует случайную строку фиксированной длины"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def create_unique_courier(base_url):
    """
    Создает уникального курьера и возвращает кортеж с логином, паролем и именем.
    :param base_url: Базовый URL API
    :return: Кортеж (логин, пароль, имя)
    """
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f"{base_url}courier", json=payload)
    if response.status_code != 201:
        raise Exception("Не удалось зарегистрировать курьера.")

    return login, password, first_name