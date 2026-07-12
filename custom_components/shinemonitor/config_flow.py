"""Config flow for ShineMonitor."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

import voluptuous as vol
from shinemonitor_api import KNOWN_APPS, AppProfile, ShineMonitorAuthError
from shinemonitor_api.aio import AsyncShineMonitorAPI

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers.httpx_client import get_async_client

from .const import CONF_APP_PROFILE, DEFAULT_APP_PROFILE, DOMAIN

_LOGGER = logging.getLogger(__name__)

_APP_PROFILE_OPTIONS = {name: name.capitalize() for name in KNOWN_APPS}

_USER_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Optional(CONF_APP_PROFILE, default=DEFAULT_APP_PROFILE): vol.In(
            _APP_PROFILE_OPTIONS
        ),
    }
)


class ShineMonitorConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ShineMonitor."""

    VERSION = 1

    async def _validate(self, username: str, password: str, app_profile: str) -> None:
        app = AppProfile.from_name(app_profile)
        api = AsyncShineMonitorAPI(app=app, client=get_async_client(self.hass))
        await api.login(username, password)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        if user_input is not None:
            username = user_input[CONF_USERNAME]
            app_profile = user_input.get(CONF_APP_PROFILE, DEFAULT_APP_PROFILE)
            await self.async_set_unique_id(username.lower())
            self._abort_if_unique_id_configured()
            try:
                await self._validate(username, user_input[CONF_PASSWORD], app_profile)
            except ShineMonitorAuthError as err:
                _LOGGER.warning("ShineMonitor login failed: %s", err)
                errors["base"] = "invalid_auth"
            except Exception:  # noqa: BLE001
                _LOGGER.exception("Unexpected error during ShineMonitor login")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=username, data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=_USER_SCHEMA, errors=errors
        )

    async def async_step_reauth(
        self, entry_data: Mapping[str, Any]
    ) -> ConfigFlowResult:
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        entry = self._get_reauth_entry()
        if user_input is not None:
            try:
                await self._validate(
                    entry.data[CONF_USERNAME],
                    user_input[CONF_PASSWORD],
                    entry.data.get(CONF_APP_PROFILE, DEFAULT_APP_PROFILE),
                )
            except ShineMonitorAuthError:
                errors["base"] = "invalid_auth"
            else:
                return self.async_update_reload_and_abort(
                    entry, data={**entry.data, CONF_PASSWORD: user_input[CONF_PASSWORD]}
                )

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=vol.Schema({vol.Required(CONF_PASSWORD): str}),
            errors=errors,
            description_placeholders={"username": entry.data[CONF_USERNAME]},
        )
