import requests

# Base URL for the Railway API
BASE_URL = 'https://api.railway.app/'

# Store JWT token in memory
jwt_token = None

def register(username, password):
    url = BASE_URL + 'auth/register'
    response = requests.post(url, json={'username': username, 'password': password})
    return response.json()


def login(username, password):
    global jwt_token
    url = BASE_URL + 'auth/login'
    response = requests.post(url, json={'username': username, 'password': password})
    if response.status_code == 200:
        jwt_token = response.json().get('token')
    return response.json()


def fetch_hunts():
    url = BASE_URL + 'hunts'
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = requests.get(url, headers=headers)
    return response.json()


def save_hunt(hunt_data):
    url = BASE_URL + 'hunts'
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = requests.post(url, json=hunt_data, headers=headers)
    return response.json()


def delete_hunt(date, index):
    url = BASE_URL + f'hunts/{date}/{index}'
    headers = {'Authorization': f'Bearer {jwt_token}'}
    response = requests.delete(url, headers=headers)
    return response.json()