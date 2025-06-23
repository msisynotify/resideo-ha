import requests
import time
import base64
import json

# Replace with your actual credentials

CLIENT_CREDENTIALS = "nKPKnoI9"
# {"access_token":"ZtdwpKPccOSxhaAOoppDvZGKHIxM","refresh_token":"3Syy46Hw3K9LeQmlahc6WBlZ58uyDCL7","expires_in":"1799", "token_type":"Bearer"}
LOCATION = "4478246"
DEVICEID = "LCC-48A2E6B796C4"
GROUP_ID = "0"

class TokenManager:
    CLIENT_ID = "QEXUDmRWk8QsTUhA8GQAsAP2TH1GJTU0"
    CLIENT_SECRET = "jVmLTID0B8eIG0Kh"
    AUTH_CODE: "ChwUgy7M"
    ACCESS_TOKEN = "CKuDGcT6LFxRP0qOqUAeRysT1XMm"
    ACCESS_TOKEN_URL = "https://api.honeywell.com/oauth2/token"
    REFRESH_TOKEN = "zuepyOU2psPjVX9Er2cfrjxbciOpvSXp"
    REDIRECT_URI = "http://localhost:8080/"

    def __init__(self):
        self.access_token = None
        self.expiry_time = None

    def get_token(self):
        if not self.access_token or time.time() > self.expiry_time:
            self.refresh_token()
        return self.access_token

    @pyscript_executor
    def refresh_token(self):
        auth = base64.b64encode(f"{self.CLIENT_ID}:{self.CLIENT_SECRET}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self.REFRESH_TOKEN,
            'redirect_uri': self.REDIRECT_URI
        }
        response = requests.post(self.ACCESS_TOKEN_URL, headers=headers, data=data)
        if response.status_code == 200:
            token_info = response.json()
            self.access_token = token_info['access_token']
            self.expiry_time = time.time() + int(token_info['expires_in'])
        else:
            raise Exception('Failed to refresh token: {}'.format(response.content))

@pyscript_executor
def get_devices(token_manager):
    bearer = token_manager.get_token()
    headers = {"Authorization": f"Bearer {bearer}"}
    response = requests.get(f"https://api.honeywell.com/v2/devices?apikey={TokenManager.CLIENT_ID}&locationId={LOCATION}&type=regular", headers=headers)
    devices = response.json()
    return devices

@pyscript_executor
def get_thermostat_data(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"https://api.honeywell.com/v2/devices/thermostats/{DEVICEID}?apikey={TokenManager.CLIENT_ID}&locationId={LOCATION}", headers=headers)
    return response.json()

@pyscript_executor
def get_sensor_data(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"https://api.honeywell.com/v2/devices/thermostats/{DEVICEID}/group/{GROUP_ID}/rooms?apikey={TokenManager.CLIENT_ID}&locationId={LOCATION}", headers=headers)
    return response.json()

@pyscript_executor
def get_schedules(access_token, device_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"https://api.honeywellhome.com/v2/devices/schedule/{device_id}?apikey={TokenManager.CLIENT_ID}&locationId={LOCATION}&type=regular", headers=headers)
    return response.json()
    