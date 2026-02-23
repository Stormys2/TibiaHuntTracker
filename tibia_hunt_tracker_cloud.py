import requests
import os

# Configuration
RAILWAY_API_URL = 'https://tibiahunttracker.up.railway.app/'
JWT_TOKEN = os.getenv('JWT_TOKEN')  # Assuming the JWT token is stored in an environment variable

# Helper function to make API requests
def api_request(endpoint, method='GET', data=None):
    headers = {'Authorization': f'Bearer {JWT_TOKEN}', 'Content-Type': 'application/json'}
    url = f'{RAILWAY_API_URL}/{endpoint}'
    response = requests.request(method, url, json=data, headers=headers)
    return response.json() if response.status_code == 200 else response.text

# Register new user
def register(username, password):
    data = {'username': username, 'password': password}
    return api_request('register', 'POST', data)

# Login user and retrieve JWT
def login(username, password):
    data = {'username': username, 'password': password}
    return api_request('login', 'POST', data)

# Get all hunts
def get_hunts():
    return api_request('hunts')

# Save a new hunt
def save_hunt(hunt_data):
    return api_request('hunts', 'POST', hunt_data)

# Delete a hunt
def delete_hunt(hunt_id):
    return api_request(f'hunts/{hunt_id}', 'DELETE')

# Example usage:
if __name__ == '__main__':
    # Register a new user
    print(register('testuser', 'testpass'))
    # Login user
    print(login('testuser', 'testpass'))
    # Get hunts
    print(get_hunts())
    # Save a hunt
    print(save_hunt({'id': 1, 'description': 'First hunt'}))
    # Delete a hunt
    print(delete_hunt(1))
