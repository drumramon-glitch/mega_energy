import base64
import json
import logging
from datetime import datetime, timezone, timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.components.persistent_notification import async_create
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import *

_LOGGER = logging.getLogger(__name__)

def get_token_status(token: str) -> str:
    payload = token.split(".")[1]
    payload += "=" * (-len(payload) % 4)
    data = json.loads(base64.urlsafe_b64decode(payload))
    exp = datetime.fromtimestamp(data["exp"], tz=timezone.utc)
    now = datetime.now(tz=timezone.utc)
    if exp < now:
        return "expired"
    if exp < now + timedelta(days=7):
        return "expiring"
    return "ok"

class MegaCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(hours=6),
        )
        self.entry = entry
        self.config = entry.data
        self.costs: dict[str, float] = {}
        self.raw: dict[str, list] = {}
        self.token_status = "ok"
        self._notified = set()

    async def _async_setup(self) -> None:
        """One-time setup (HA 2024.8+)."""
        status = get_token_status(self.config[CONF_TOKEN])
        self.token_status = status
        if status in ["expiring", "expired"] and status not in self._notified:
            async_create(
                self.hass,
                f"Mega token status: {status}. Vernieuw je token via integratie-instellingen.",
                title="Mega Energy",
            )
            self._notified.add(status)
        if status == "expired":
            # Laat first refresh mislukken zodat HA automatisch retry/reauth triggert
            raise UpdateFailed("Mega token verlopen")

    async def _async_update_data(self):
        """Fetch periodic data."""
        session = async_get_clientsession(self.hass)  # gedeelde sessie
        now = datetime.now()
        params_common = {
            "postalCode": self.config[CONF_POSTAL_CODE],
            "dgoGln": self.config[CONF_DGO_GLN],
        }
        headers = {
            "Authorization": f"Bearer {self.config[CONF_TOKEN]}",
            "Accept": "application/json",
        }

        for market in ["EL", "GAS"]:
            for interval in ["YEAR", "MONTH", "DAY"]:
                url = (
                    f"{BASE_URL}/{self.config[CONF_CUSTOMER_ID]}/"
                    f"contract/{self.config[CONF_CONTRACT_ID]}/"
                    f"points/{self.config[CONF_POINT_ID]}/consumptions"
                )
                params = {
                    **params_common,
                    "intervalType": interval,
                    "intervalValue": now.year,
                    "marketCode": market,
                }

                async with session.get(url, headers=headers, params=params) as resp:
                    if resp.status != 200:
                        text = await resp.text()
                        raise UpdateFailed(f"{resp.status} from Mega: {text}")

                    data = await resp.json()
                    total = round(
                        sum(i.get("estimated_cost", 0) for i in data.get("consumptions", [])),
                        2,
                    )
                    key = f"{market}_{interval}"
                    self.costs[key] = total
                    self.raw[key] = data.get("consumptions", [])
