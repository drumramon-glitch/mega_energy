from __future__ import annotations

from typing import Any, Dict
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_TOKEN,
    CONF_CUSTOMER_ID,
    CONF_CONTRACT_ID,
    CONF_POINT_ID,
    CONF_DGO_GLN,
    CONF_POSTAL_CODE,
    CONF_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL,
)


class MegaEnergyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for Mega Energy."""
    VERSION = 1

    async def async_step_user(
        self, user_input: Dict[str, Any] | None = None
    ) -> FlowResult:
        errors: dict[str, str] = {}

        if user_input is not None:
            # TODO: valideer hier je gegevens (API-call). Bijvoorbeeld:
            # ok = await self._async_validate_credentials(self.hass, user_input)
            # if not ok:
            #     errors["base"] = "auth"
            # else:
            #    ...
            # Voor nu gaan we ervan uit dat de input geldig is.

            # Gebruik een uniek ID zodat dezelfde klant/contract niet dubbel geconfigureerd kan worden.
            unique_id = f"{user_input[CONF_CUSTOMER_ID]}_{user_input[CONF_CONTRACT_ID]}"
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title="Mega Energy",
                data={
                    CONF_TOKEN: user_input[CONF_TOKEN],
                    CONF_CUSTOMER_ID: user_input[CONF_CUSTOMER_ID],
                    CONF_CONTRACT_ID: user_input[CONF_CONTRACT_ID],
                    CONF_POINT_ID: user_input[CONF_POINT_ID],
                    CONF_DGO_GLN: user_input[CONF_DGO_GLN],
                    CONF_POSTAL_CODE: user_input[CONF_POSTAL_CODE],
                },
            )

        # Gebruik selectors waar relevant (token als password)
        data_schema = vol.Schema(
            {
                vol.Required(CONF_TOKEN): selector.TextSelector(
                    selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD, autocomplete="off")
                ),
                vol.Required(CONF_CUSTOMER_ID): str,
                vol.Required(CONF_CONTRACT_ID): str,
                vol.Required(CONF_POINT_ID): str,
                vol.Required(CONF_DGO_GLN): str,
                vol.Required(CONF_POSTAL_CODE): str,  # evt. valideren met regex voor BE: r"^\d{4}$"
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    # Voor YAML-imports als je die ooit ondersteunt:
    async def async_step_import(self, import_config: Dict[str, Any]) -> FlowResult:
        """Handle import from YAML."""
        return await self.async_step_user(import_config)

    # Voorbeeld van een async validatie-call (vul zelf in):
    async def _async_validate_credentials(self, hass: HomeAssistant, data: Dict[str, Any]) -> bool:
        """Validate token/IDs tegen je backend. Return True/False."""
        # bv. resp = await some_api.async_validate(...)
        # return resp.ok
        return True  # placeholder


class MegaEnergyOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options for Mega Energy."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input: Dict[str, Any] | None = None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Huidige waarde of default
        current_interval = self.config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)

        options_schema = vol.Schema(
            {
                vol.Required(CONF_SCAN_INTERVAL, default=current_interval): selector.NumberSelector(
                    selector.NumberSelectorConfig(min=60, max=3600, step=30, unit_of_measurement="s", mode=selector.NumberSelectorMode.BOX)
                )
            }
        )
        return self.async_show_form(step_id="init", data_schema=options_schema)


# Zorg dat Home Assistant weet hoe de options flow op te starten
async def async_get_options_flow(config_entry: config_entries.ConfigEntry):
    return MegaEnergyOptionsFlowHandler(config_entry)
``
