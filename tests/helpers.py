import requests
import random
import string

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
    response = requests.post(f"{base_url}/courier", json=payload)
    if response.status_code == 201:
        return login, password, first_name
    else:
        return [], [], []