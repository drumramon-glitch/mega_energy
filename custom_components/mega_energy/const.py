"""Constanten voor de Mega Energy integratie."""

from __future__ import annotations

from homeassistant.const import CONF_TOKEN

# Domeinnaam van de integratie (moet overeenkomen met manifest.json en mapnaam)
DOMAIN: str = "mega_energy"

# Config keys die je in de config_flow gebruikt
CONF_CUSTOMER_ID: str = "customer_id"
CONF_CONTRACT_ID: str = "contract_id"
CONF_POINT_ID: str = "point_id"
CONF_DGO_GLN: str = "dgo_gln"
CONF_POSTAL_CODE: str = "postal_code"

# Opties (OptionsFlow) — bijvoorbeeld polling-interval voor cloud_polling
CONF_SCAN_INTERVAL: str = "scan_interval"
DEFAULT_SCAN_INTERVAL: int = 300  # seconden (5 min), pas aan naar wens

# (Optioneel) Titles/labels voor UI of logging
INTEGRATION_TITLE: str = "Mega Energy Costs"

# (Optioneel) Data keys voor hass.data opslag (handig voor coordinators/clients)
DATA_COORDINATOR: str = "coordinator"
DATA_CLIENT: str = "client"

# (Optioneel) Versieschema van je config entries
CONFIG_VERSION: int = 1

# Export wat je publiek wil maken (niet verplicht, maar netjes)
__all__ = [
    "DOMAIN",
    "CONF_TOKEN",
    "CONF_CUSTOMER_ID",
    "CONF_CONTRACT_ID",
    "CONF_POINT_ID",
    "CONF_DGO_GLN",
    "CONF_POSTAL_CODE",
    "CONF_SCAN_INTERVAL",
    "DEFAULT_SCAN_INTERVAL",
    "INTEGRATION_TITLE",
    "DATA_COORDINATOR",
    "DATA_CLIENT",
    "CONFIG_VERSION",
]
