{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import aiohttp\
import base64\
import json\
from datetime import datetime, timezone, timedelta\
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed\
from homeassistant.components.persistent_notification import async_create\
from .const import *\
\
def get_token_status(token):\
    payload = token.split(".")[1]\
    payload += "=" * (-len(payload) % 4)\
    data = json.loads(base64.urlsafe_b64decode(payload))\
    exp = datetime.fromtimestamp(data["exp"], tz=timezone.utc)\
    now = datetime.now(tz=timezone.utc)\
\
    if exp < now:\
        return "expired"\
    if exp < now + timedelta(days=7):\
        return "expiring"\
    return "ok"\
\
class MegaCoordinator(DataUpdateCoordinator):\
    def __init__(self, hass, config):\
        super().__init__(\
            hass,\
            name="mega_energy",\
            update_interval=timedelta(hours=6),\
        )\
        self.config = config\
        self.costs = \{\}\
        self.raw = \{\}\
        self.token_status = "ok"\
        self.notified = set()\
\
    async def _async_update_data(self):\
        status = get_token_status(self.config[CONF_TOKEN])\
        self.token_status = status\
\
        if status in ["expiring", "expired"] and status not in self.notified:\
            async_create(\
                self.hass,\
                f"Mega token status: \{status\}. Vernieuw je token via integratie-instellingen.",\
                title="Mega Energy",\
            )\
            self.notified.add(status)\
\
        if status == "expired":\
            raise UpdateFailed("Mega token verlopen")\
\
        now = datetime.now()\
        async with aiohttp.ClientSession() as session:\
            for market in ["EL", "GAS"]:\
                for interval in ["YEAR", "MONTH", "DAY"]:\
                    url = (\
                        f"\{BASE_URL\}/\{self.config[CONF_CUSTOMER_ID]\}/"\
                        f"contract/\{self.config[CONF_CONTRACT_ID]\}/"\
                        f"points/\{self.config[CONF_POINT_ID]\}/consumptions"\
                    )\
\
                    params = \{\
                        "intervalType": interval,\
                        "intervalValue": now.year,\
                        "postalCode": self.config[CONF_POSTAL_CODE],\
                        "marketCode": market,\
                        "dgoGln": self.config[CONF_DGO_GLN],\
                    \}\
\
                    headers = \{\
                        "Authorization": f"Bearer \{self.config[CONF_TOKEN]\}",\
                        "Accept": "application/json",\
                    \}\
\
                    async with session.get(url, headers=headers, params=params) as resp:\
                        data = await resp.json()\
                        total = round(\
                            sum(i.get("estimated_cost", 0) for i in data.get("consumptions", [])), 2\
                        )\
                        key = f"\{market\}_\{interval\}"\
                        self.costs[key] = total\
                        self.raw[key] = data.get("consumptions", [])\
}