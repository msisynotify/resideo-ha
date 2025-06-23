import time
import base64
from homeassistant.helpers.aiohttp_client import async_get_clientsession

# your constants…
CLIENT_ID        = "QEXUDmRWk8QsTUhA8GQAsAP2TH1GJTU0"
CLIENT_SECRET    = "jVmLTID0B8eIG0Kh"
REFRESH_TOKEN    = "zuepyOU2psPjVX9Er2cfrjxbciOpvSXp"
REDIRECT_URI     = "http://localhost:8080/"
ACCESS_TOKEN_URL = "https://api.honeywell.com/oauth2/token"
LOCATION         = "4478246"

class TokenManager:
    def __init__(self):
        self.access_token = None
        self.expires_at   = 0.0
        self.CLIENT_ID = CLIENT_ID

    async def get_token(self):
        now = time.time()
        if not self.access_token or now >= self.expires_at:
            await self._refresh_token()
        return self.access_token

    async def _refresh_token(self):
        auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth}",
            "Content-Type":  "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type":    "refresh_token",
            "refresh_token": REFRESH_TOKEN,
            "redirect_uri":  REDIRECT_URI
        }
        session = async_get_clientsession(hass)             # ← pass hass here
        resp    = await session.post(ACCESS_TOKEN_URL, headers=headers, data=data)
        resp.raise_for_status()
        tok = await resp.json()
        self.access_token = tok["access_token"]
        self.expires_at   = time.time() + int(tok.get("expires_in", 0))


async def get_devices(token_manager):
    token   = await token_manager.get_token()
    session = async_get_clientsession(hass)
    url     = (
        f"https://api.honeywell.com/v2/devices"
        f"?apikey={token_manager.CLIENT_ID}"
        f"&locationId={LOCATION}"
        f"&type=regular"
    )
    resp    = await session.get(url, headers={"Authorization": f"Bearer {token}"})
    if resp.status == 401:
        await token_manager._refresh_token()
        token = token_manager.access_token
        resp  = await session.get(url, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()
    return await resp.json()


async def get_thermostat_data(token_manager):
    token   = await token_manager.get_token()
    session = async_get_clientsession(hass)
    url     = (
        f"https://api.honeywell.com/v2/devices/thermostats/{DEVICEID}"
        f"?apikey={token_manager.CLIENT_ID}&locationId={LOCATION}"
    )
    resp    = await session.get(url, headers={"Authorization": f"Bearer {token}"})
    if resp.status == 401:
        await token_manager._refresh_token()
        token = token_manager.access_token
        resp  = await session.get(url, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()
    return await resp.json()


async def get_sensor_data(token_manager):
    token   = await token_manager.get_token()
    session = async_get_clientsession(hass)
    url     = (
        f"https://api.honeywell.com/v2/devices/thermostats/{DEVICEID}"
        f"/group/{GROUP_ID}/rooms"
        f"?apikey={token_manager.CLIENT_ID}&locationId={LOCATION}"
    )
    resp    = await session.get(url, headers={"Authorization": f"Bearer {token}"})
    if resp.status == 401:
        await token_manager._refresh_token()
        token = token_manager.access_token
        resp  = await session.get(url, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()
    return await resp.json()


async def get_schedules(token_manager, device_id):
    token   = await token_manager.get_token()
    session = async_get_clientsession(hass)
    url     = (
        f"https://api.honeywellhome.com/v2/devices/schedule/{device_id}"
        f"?apikey={token_manager.CLIENT_ID}"
        f"&locationId={LOCATION}&type=regular"
    )
    resp    = await session.get(url, headers={"Authorization": f"Bearer {token}"})
    if resp.status == 401:
        await token_manager._refresh_token()
        token = token_manager.access_token
        resp  = await session.get(url, headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()
    return await resp.json()

