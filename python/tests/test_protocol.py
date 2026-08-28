"""Sansio-only tests — pure functions, no I/O."""

from __future__ import annotations

import hashlib
from datetime import date

import pytest

from shinemonitor_api import (
    AppProfile,
    AuthState,
    ShineMonitorAuthError,
    ShineMonitorError,
)
from shinemonitor_api._protocol import (
    ProtocolConfig,
    daily_data_url,
    devices_url,
    last_data_url,
    login_url,
    parse_devices,
    parse_last,
    parse_login,
    query_devices_url,
)
from shinemonitor_api.models import DeviceIdentifier


def _sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest().lower()


def _params_from(url: str) -> dict[str, str]:
    _, _, qs = url.partition("?")
    return dict(pair.split("=", 1) for pair in qs.split("&"))


def test_login_url_signs_with_password_hash() -> None:
    cfg = ProtocolConfig(
        base_url="http://mock/public/",
        suffix_context="&source=1",
        company_key="ck",
    )
    url = login_url(cfg, "demo", "pass")
    params = _params_from(url)
    assert params["action"] == "authSource"
    assert params["usr"] == "demo"
    assert params["company-key"] == "ck"
    base_action = "&action=authSource&usr=demo&company-key=ck&source=1"
    expected = _sha1(params["salt"] + _sha1("pass") + base_action)
    assert params["sign"] == expected


def test_login_url_encodes_spaces_in_username() -> None:
    cfg = ProtocolConfig(
        base_url="http://mock/public/", suffix_context="&source=1", company_key="ck"
    )
    url = login_url(cfg, "First Last", "pass")
    params = _params_from(url)
    assert params["usr"] == "First+Last"
    base_action = "&action=authSource&usr=First+Last&company-key=ck&source=1"
    expected = _sha1(params["salt"] + _sha1("pass") + base_action)
    assert params["sign"] == expected


def test_authed_url_signs_with_token_and_secret() -> None:
    cfg = ProtocolConfig(
        base_url="http://mock/public/", suffix_context="&source=1", company_key="ck"
    )
    auth = AuthState(token="T", secret="S", expire=600)
    url = devices_url(cfg, auth)
    params = _params_from(url)
    assert params["token"] == "T"
    base_action = "&action=webQueryDeviceEs&source=1"
    expected = _sha1(params["salt"] + "S" + "T" + base_action)
    assert params["sign"] == expected


def test_last_data_url_includes_device_params() -> None:
    cfg = ProtocolConfig(
        base_url="http://mock/public/", suffix_context="", company_key="ck"
    )
    auth = AuthState(token="T", secret="S", expire=600)
    device = DeviceIdentifier(sn="SN1", pn="PN1", devaddr=1, devcode=42, devalias=None)
    url = last_data_url(cfg, auth, device)
    params = _params_from(url)
    assert params["pn"] == "PN1"
    assert params["sn"] == "SN1"
    assert params["devcode"] == "42"
    assert params["devaddr"] == "1"


def test_daily_data_url_uses_iso_date() -> None:
    cfg = ProtocolConfig(
        base_url="http://mock/public/", suffix_context="", company_key="ck"
    )
    auth = AuthState(token="T", secret="S", expire=600)
    url = daily_data_url(cfg, auth, date(2026, 4, 25), "SN", "PN", 99, 1)
    assert "&date=2026-04-25" in url


def test_watchpower_profile_suffix_context() -> None:
    assert AppProfile.WATCHPOWER._suffix_context() == (
        "&i18n=en_US&lang=en_US&source=1&_app_client_=android"
        "&_app_id_=wifiapp.volfw.watchpower&_app_version_=1.0.6.3"
    )


def test_renoclient_profile_fields() -> None:
    p = AppProfile.RENOCLIENT
    assert p.app_id == "com.eybond.renoclient"
    assert p.app_version == "1.3.2.0"
    assert p.company_key == "bnrl_frRFjEz8Mkn"


def test_renoclient_suffix_context() -> None:
    assert AppProfile.RENOCLIENT._suffix_context() == (
        "&i18n=en_US&lang=en_US&source=1&_app_client_=android"
        "&_app_id_=com.eybond.renoclient&_app_version_=1.3.2.0"
    )


def test_from_name_returns_preset_case_insensitive() -> None:
    assert AppProfile.from_name("renoclient") is AppProfile.RENOCLIENT
    assert AppProfile.from_name("WatchPower") is AppProfile.WATCHPOWER


def test_from_name_unknown_raises_value_error() -> None:
    with pytest.raises(ValueError):
        AppProfile.from_name("nope")


def test_to_config_maps_profile_fields() -> None:
    cfg = AppProfile.RENOCLIENT._to_config()
    assert cfg.company_key == "bnrl_frRFjEz8Mkn"
    assert cfg.base_url == "http://android.shinemonitor.com/public/"
    assert "&_app_id_=com.eybond.renoclient" in cfg.suffix_context


def test_custom_profile_defaults_to_shared_key_and_host() -> None:
    p = AppProfile(app_id="com.foo.bar", app_version="2.0.0")
    assert p.company_key == "bnrl_frRFjEz8Mkn"
    assert p.base_url == "http://android.shinemonitor.com/public/"
    assert "&_app_id_=com.foo.bar" in p._suffix_context()


def test_query_devices_url_action_and_paging() -> None:
    cfg = ProtocolConfig(
        base_url="http://mock/public/", suffix_context="&source=1", company_key="ck"
    )
    auth = AuthState(token="T", secret="S", expire=600)
    url = query_devices_url(cfg, auth, page=0, pagesize=50)
    params = _params_from(url)
    assert params["action"] == "queryDevices"
    assert params["page"] == "0"
    assert params["pagesize"] == "50"
    assert params["token"] == "T"


def test_parse_login_returns_auth_state() -> None:
    state = parse_login(
        {
            "err": 0,
            "desc": "ERR_NONE",
            "dat": {"token": "tok", "secret": "sec", "expire": 600, "role": 0},
        }
    )
    assert state == AuthState(token="tok", secret="sec", expire=600)


@pytest.mark.parametrize("err", [0x000F, 0x0010, 0x0019, 0x0105, 0x010E])
def test_auth_band_errors_raise_auth_error(err: int) -> None:
    with pytest.raises(ShineMonitorAuthError):
        parse_login({"err": err, "desc": "x"})


def test_non_auth_error_raises_generic() -> None:
    with pytest.raises(ShineMonitorError) as excinfo:
        parse_devices({"err": 0x0102, "desc": "ERR_DEVICE_NOT_FOUND"})
    assert excinfo.value.err == 0x0102
    assert excinfo.value.desc == "ERR_DEVICE_NOT_FOUND"


def test_parse_last_accepts_epoch_ms_gts() -> None:
    """Real responses sometimes return gts as a millisecond timestamp string."""
    from shinemonitor_api.models import _parse_gts

    parsed = _parse_gts("1777101032550")
    assert parsed.year == 2026


def test_parse_last_accepts_formatted_gts() -> None:
    from shinemonitor_api.models import _parse_gts

    parsed = _parse_gts("2026-04-25 09:00:00")
    assert parsed.year == 2026
    assert parsed.hour == 9


def test_parse_last_round_trips_main_fields() -> None:
    snapshot = parse_last(
        {
            "err": 0,
            "desc": "ERR_NONE",
            "dat": {
                "gts": "2026-04-25 09:00:00",
                "pars": {
                    "gd_": [
                        {"id": "gd_grid_rating_voltage", "val": "230.0"},
                        {"id": "gd_grid_rating_current", "val": "30.0"},
                        {"id": "gd_battery_rating_voltage", "val": "48.0"},
                        {"id": "gd_bse_input_voltage_read", "val": "230.0"},
                        {"id": "gd_ac_output_rating_current", "val": "30.0"},
                        {"id": "gd_bse_output_frequency_read", "val": "50.0"},
                        {"id": "gd_ac_output_rating_apparent_power", "val": "5000"},
                        {"id": "gd_ac_output_rating_active_power", "val": "5000"},
                    ],
                    "sy_": [
                        {"id": "sy_model", "val": "5KW"},
                        {"id": "sy_main_cpu1_firmware_version", "val": "01.23"},
                        {"id": "sy_main_cpu2_firmware_version", "val": "04.56"},
                    ],
                    "pv_": [{"id": "pv_input_current", "val": "12.5"}],
                    "bt_": [
                        {"id": "bt_grid_voltage", "val": "229.5"},
                        {"id": "bt_grid_frequency", "val": "50.0"},
                        {"id": "bt_voltage_1", "val": "180.2"},
                        {"id": "bt_input_power", "val": "1500"},
                        {"id": "bt_battery_voltage", "val": "52.4"},
                        {"id": "bt_battery_capacity", "val": "85"},
                        {"id": "bt_battery_charging_current", "val": "10.5"},
                        {"id": "bt_battery_discharge_current", "val": "0.0"},
                        {"id": "bt_ac_output_voltage", "val": "230.1"},
                        {"id": "bt_grid_AC_frequency", "val": "50.0"},
                        {"id": "bt_ac_output_apparent_power", "val": "1200"},
                        {"id": "bt_load_active_power_sole", "val": "1100"},
                        {"id": "bt_output_load_percent", "val": "22"},
                    ],
                },
            },
        }
    )
    assert snapshot.main.battery_capacity == 85
    assert snapshot.main.ac_output_active_power == 1100
    assert snapshot.system.model == "5KW"
    assert snapshot.timestamp.year == 2026


def test_parse_last_extracts_from_separate_bc_and_pv_blocks() -> None:
    snapshot = parse_last(
        {
            "err": 0,
            "desc": "ERR_NONE",
            "dat": {
                "gts": "2026-08-05 14:37:29",
                "pars": {
                    "pv_": [
                        {"id": "bt_voltage_1", "val": "129.4"},
                        {"id": "bt_input_power", "val": "0"},
                    ],
                    "sy_": [{"id": "sy_model", "val": "Off Grid"}],
                    "gd_": [{"id": "bt_grid_voltage", "val": "0.0"}],
                    "bt_": [
                        {"id": "bt_battery_voltage", "val": "49.3"},
                        {"id": "bt_battery_capacity", "val": "71"},
                    ],
                    "bc_": [
                        {"id": "bt_ac_output_voltage", "val": "230.0"},
                        {"id": "bt_grid_AC_frequency", "val": "50.0"},
                        {"id": "bt_load_active_power_sole", "val": "533"},
                        {"id": "bt_output_load_percent", "val": "12"},
                    ],
                },
            },
        }
    )
    assert snapshot.main.pv_input_voltage == 129.4
    assert snapshot.main.battery_capacity == 71
    assert snapshot.main.ac_output_voltage == 230.0
    assert snapshot.main.ac_output_frequency == 50.0
    assert snapshot.main.ac_output_active_power == 533
    assert snapshot.main.output_load_percent == 12
