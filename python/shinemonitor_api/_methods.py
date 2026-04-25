"""GENERATED — do not edit. Run `python scripts/codegen.py`."""
# mypy: disable-error-code=attr-defined

from __future__ import annotations

from typing import Any

from . import _actions


class SyncActionsMixin:
    """GENERATED — do not edit."""

    def update_token(self) -> Any:
        """Call action `updateToken` (chapter 2)."""
        url = _actions.url_update_token(self._config, self._require_auth())
        return _actions.parse_update_token(self._get_json(url))

    def query_account_info(self) -> Any:
        """Call action `queryAccountInfo` (chapter 2)."""
        url = _actions.url_query_account_info(self._config, self._require_auth())
        return _actions.parse_query_account_info(self._get_json(url))

    def update_password(self, *, oldPwd: str, newPwd: str) -> Any:
        """Call action `updatePassword` (chapter 2)."""
        url = _actions.url_update_password(
            self._config, self._require_auth(), oldPwd=oldPwd, newPwd=newPwd
        )
        return _actions.parse_update_password(self._get_json(url))

    def query_plants(
        self,
        *,
        status: int | None = None,
        orderBy: str | None = None,
        plantName: str | None = None,
        page: int | None = None,
        pagesize: int | None = None,
    ) -> Any:
        """Call action `queryPlants` (chapter 3)."""
        url = _actions.url_query_plants(
            self._config,
            self._require_auth(),
            status=status,
            orderBy=orderBy,
            plantName=plantName,
            page=page,
            pagesize=pagesize,
        )
        return _actions.parse_query_plants(self._get_json(url))

    def query_plant_info(self, *, plantid: int) -> Any:
        """Call action `queryPlantInfo` (chapter 3)."""
        url = _actions.url_query_plant_info(
            self._config, self._require_auth(), plantid=plantid
        )
        return _actions.parse_query_plant_info(self._get_json(url))

    def query_plant_count(self) -> Any:
        """Call action `queryPlantCount` (chapter 3)."""
        url = _actions.url_query_plant_count(self._config, self._require_auth())
        return _actions.parse_query_plant_count(self._get_json(url))

    def query_plant_energy_day(self, *, plantid: int, date: str) -> Any:
        """Call action `queryPlantEnergyDay` (chapter 3)."""
        url = _actions.url_query_plant_energy_day(
            self._config, self._require_auth(), plantid=plantid, date=date
        )
        return _actions.parse_query_plant_energy_day(self._get_json(url))

    def query_plant_energy_month(self, *, plantid: int, date: str) -> Any:
        """Call action `queryPlantEnergyMonth` (chapter 3)."""
        url = _actions.url_query_plant_energy_month(
            self._config, self._require_auth(), plantid=plantid, date=date
        )
        return _actions.parse_query_plant_energy_month(self._get_json(url))

    def query_plant_energy_year(self, *, plantid: int, date: str) -> Any:
        """Call action `queryPlantEnergyYear` (chapter 3)."""
        url = _actions.url_query_plant_energy_year(
            self._config, self._require_auth(), plantid=plantid, date=date
        )
        return _actions.parse_query_plant_energy_year(self._get_json(url))

    def query_plant_energy_total(self, *, plantid: int) -> Any:
        """Call action `queryPlantEnergyTotal` (chapter 3)."""
        url = _actions.url_query_plant_energy_total(
            self._config, self._require_auth(), plantid=plantid
        )
        return _actions.parse_query_plant_energy_total(self._get_json(url))

    def query_plant_active_ouput_power_current(self, *, plantid: int) -> Any:
        """Call action `queryPlantActiveOuputPowerCurrent` (chapter 3)."""
        url = _actions.url_query_plant_active_ouput_power_current(
            self._config, self._require_auth(), plantid=plantid
        )
        return _actions.parse_query_plant_active_ouput_power_current(
            self._get_json(url)
        )

    def query_collectors(
        self, *, page: int | None = None, pagesize: int | None = None
    ) -> Any:
        """Call action `queryCollectors` (chapter 4)."""
        url = _actions.url_query_collectors(
            self._config, self._require_auth(), page=page, pagesize=pagesize
        )
        return _actions.parse_query_collectors(self._get_json(url))

    def query_collector_info(self, *, pn: str) -> Any:
        """Call action `queryCollectorInfo` (chapter 4)."""
        url = _actions.url_query_collector_info(
            self._config, self._require_auth(), pn=pn
        )
        return _actions.parse_query_collector_info(self._get_json(url))

    def query_collector_status(self, *, pn: str) -> Any:
        """Call action `queryCollectorStatus` (chapter 4)."""
        url = _actions.url_query_collector_status(
            self._config, self._require_auth(), pn=pn
        )
        return _actions.parse_query_collector_status(self._get_json(url))

    def query_collector_devices(self, *, pn: str) -> Any:
        """Call action `queryCollectorDevices` (chapter 4)."""
        url = _actions.url_query_collector_devices(
            self._config, self._require_auth(), pn=pn
        )
        return _actions.parse_query_collector_devices(self._get_json(url))

    def query_devices(
        self, *, page: int | None = None, pagesize: int | None = None
    ) -> Any:
        """Call action `queryDevices` (chapter 5)."""
        url = _actions.url_query_devices(
            self._config, self._require_auth(), page=page, pagesize=pagesize
        )
        return _actions.parse_query_devices(self._get_json(url))

    def web_query_device_es(self) -> Any:
        """Call action `webQueryDeviceEs` (chapter 5)."""
        url = _actions.url_web_query_device_es(self._config, self._require_auth())
        return _actions.parse_web_query_device_es(self._get_json(url))

    def query_device_count(self) -> Any:
        """Call action `queryDeviceCount` (chapter 5)."""
        url = _actions.url_query_device_count(self._config, self._require_auth())
        return _actions.parse_query_device_count(self._get_json(url))

    def query_device_info(self, *, pn: str, devcode: int, devaddr: int, sn: str) -> Any:
        """Call action `queryDeviceInfo` (chapter 5)."""
        url = _actions.url_query_device_info(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
        )
        return _actions.parse_query_device_info(self._get_json(url))

    def query_device_last_data(
        self, *, pn: str, devcode: int, devaddr: int, sn: str
    ) -> Any:
        """Call action `queryDeviceLastData` (chapter 5)."""
        url = _actions.url_query_device_last_data(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
        )
        return _actions.parse_query_device_last_data(self._get_json(url))

    def query_sp_device_last_data(
        self, *, pn: str, devcode: int, devaddr: int, sn: str
    ) -> Any:
        """Call action `querySPDeviceLastData` (chapter 5)."""
        url = _actions.url_query_sp_device_last_data(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
        )
        return _actions.parse_query_sp_device_last_data(self._get_json(url))

    def query_device_data_one_day(
        self, *, pn: str, devcode: int, devaddr: int, sn: str, date: str
    ) -> Any:
        """Call action `queryDeviceDataOneDay` (chapter 5)."""
        url = _actions.url_query_device_data_one_day(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
            date=date,
        )
        return _actions.parse_query_device_data_one_day(self._get_json(url))

    def query_device_status(
        self, *, pn: str, devcode: int, devaddr: int, sn: str
    ) -> Any:
        """Call action `queryDeviceStatus` (chapter 5)."""
        url = _actions.url_query_device_status(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
        )
        return _actions.parse_query_device_status(self._get_json(url))

    def query_device_warning(
        self, *, pn: str, devcode: int, devaddr: int, sn: str
    ) -> Any:
        """Call action `queryDeviceWarning` (chapter 5)."""
        url = _actions.url_query_device_warning(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
        )
        return _actions.parse_query_device_warning(self._get_json(url))

    def ctrl_device(
        self, *, pn: str, devcode: int, devaddr: int, sn: str, id: str, val: str
    ) -> Any:
        """Call action `ctrlDevice` (chapter 5)."""
        url = _actions.url_ctrl_device(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
            id=id,
            val=val,
        )
        return _actions.parse_ctrl_device(self._get_json(url))

    def query_device_energy_day(
        self, *, pn: str, devcode: int, devaddr: int, sn: str, date: str
    ) -> Any:
        """Call action `queryDeviceEnergyDay` (chapter 6)."""
        url = _actions.url_query_device_energy_day(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
            date=date,
        )
        return _actions.parse_query_device_energy_day(self._get_json(url))

    def query_device_energy_month(
        self, *, pn: str, devcode: int, devaddr: int, sn: str, date: str
    ) -> Any:
        """Call action `queryDeviceEnergyMonth` (chapter 6)."""
        url = _actions.url_query_device_energy_month(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
            date=date,
        )
        return _actions.parse_query_device_energy_month(self._get_json(url))

    def query_device_energy_year(
        self, *, pn: str, devcode: int, devaddr: int, sn: str, date: str
    ) -> Any:
        """Call action `queryDeviceEnergyYear` (chapter 6)."""
        url = _actions.url_query_device_energy_year(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
            date=date,
        )
        return _actions.parse_query_device_energy_year(self._get_json(url))

    def query_device_energy_total(
        self, *, pn: str, devcode: int, devaddr: int, sn: str
    ) -> Any:
        """Call action `queryDeviceEnergyTotal` (chapter 6)."""
        url = _actions.url_query_device_energy_total(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
        )
        return _actions.parse_query_device_energy_total(self._get_json(url))

    def query_device_active_ouput_power_current(
        self, *, pn: str, devcode: int, devaddr: int, sn: str
    ) -> Any:
        """Call action `queryDeviceActiveOuputPowerCurrent` (chapter 6)."""
        url = _actions.url_query_device_active_ouput_power_current(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
        )
        return _actions.parse_query_device_active_ouput_power_current(
            self._get_json(url)
        )

    def query_camera_info(self, *, cameraid: int) -> Any:
        """Call action `queryCameraInfo` (chapter 11)."""
        url = _actions.url_query_camera_info(
            self._config, self._require_auth(), cameraid=cameraid
        )
        return _actions.parse_query_camera_info(self._get_json(url))

    def upload_img(self, *, fmt: str) -> Any:
        """Call action `uploadImg` (chapter 84)."""
        url = _actions.url_upload_img(self._config, self._require_auth(), fmt=fmt)
        return _actions.parse_upload_img(self._get_json(url))


class AsyncActionsMixin:
    """GENERATED — do not edit."""

    async def update_token(self) -> Any:
        """Call action `updateToken` (chapter 2)."""
        url = _actions.url_update_token(self._config, self._require_auth())
        return _actions.parse_update_token(await self._get_json(url))

    async def query_account_info(self) -> Any:
        """Call action `queryAccountInfo` (chapter 2)."""
        url = _actions.url_query_account_info(self._config, self._require_auth())
        return _actions.parse_query_account_info(await self._get_json(url))

    async def update_password(self, *, oldPwd: str, newPwd: str) -> Any:
        """Call action `updatePassword` (chapter 2)."""
        url = _actions.url_update_password(
            self._config, self._require_auth(), oldPwd=oldPwd, newPwd=newPwd
        )
        return _actions.parse_update_password(await self._get_json(url))

    async def query_plants(
        self,
        *,
        status: int | None = None,
        orderBy: str | None = None,
        plantName: str | None = None,
        page: int | None = None,
        pagesize: int | None = None,
    ) -> Any:
        """Call action `queryPlants` (chapter 3)."""
        url = _actions.url_query_plants(
            self._config,
            self._require_auth(),
            status=status,
            orderBy=orderBy,
            plantName=plantName,
            page=page,
            pagesize=pagesize,
        )
        return _actions.parse_query_plants(await self._get_json(url))

    async def query_plant_info(self, *, plantid: int) -> Any:
        """Call action `queryPlantInfo` (chapter 3)."""
        url = _actions.url_query_plant_info(
            self._config, self._require_auth(), plantid=plantid
        )
        return _actions.parse_query_plant_info(await self._get_json(url))

    async def query_plant_count(self) -> Any:
        """Call action `queryPlantCount` (chapter 3)."""
        url = _actions.url_query_plant_count(self._config, self._require_auth())
        return _actions.parse_query_plant_count(await self._get_json(url))

    async def query_plant_energy_day(self, *, plantid: int, date: str) -> Any:
        """Call action `queryPlantEnergyDay` (chapter 3)."""
        url = _actions.url_query_plant_energy_day(
            self._config, self._require_auth(), plantid=plantid, date=date
        )
        return _actions.parse_query_plant_energy_day(await self._get_json(url))

    async def query_plant_energy_month(self, *, plantid: int, date: str) -> Any:
        """Call action `queryPlantEnergyMonth` (chapter 3)."""
        url = _actions.url_query_plant_energy_month(
            self._config, self._require_auth(), plantid=plantid, date=date
        )
        return _actions.parse_query_plant_energy_month(await self._get_json(url))

    async def query_plant_energy_year(self, *, plantid: int, date: str) -> Any:
        """Call action `queryPlantEnergyYear` (chapter 3)."""
        url = _actions.url_query_plant_energy_year(
            self._config, self._require_auth(), plantid=plantid, date=date
        )
        return _actions.parse_query_plant_energy_year(await self._get_json(url))

    async def query_plant_energy_total(self, *, plantid: int) -> Any:
        """Call action `queryPlantEnergyTotal` (chapter 3)."""
        url = _actions.url_query_plant_energy_total(
            self._config, self._require_auth(), plantid=plantid
        )
        return _actions.parse_query_plant_energy_total(await self._get_json(url))

    async def query_plant_active_ouput_power_current(self, *, plantid: int) -> Any:
        """Call action `queryPlantActiveOuputPowerCurrent` (chapter 3)."""
        url = _actions.url_query_plant_active_ouput_power_current(
            self._config, self._require_auth(), plantid=plantid
        )
        return _actions.parse_query_plant_active_ouput_power_current(
            await self._get_json(url)
        )

    async def query_collectors(
        self, *, page: int | None = None, pagesize: int | None = None
    ) -> Any:
        """Call action `queryCollectors` (chapter 4)."""
        url = _actions.url_query_collectors(
            self._config, self._require_auth(), page=page, pagesize=pagesize
        )
        return _actions.parse_query_collectors(await self._get_json(url))

    async def query_collector_info(self, *, pn: str) -> Any:
        """Call action `queryCollectorInfo` (chapter 4)."""
        url = _actions.url_query_collector_info(
            self._config, self._require_auth(), pn=pn
        )
        return _actions.parse_query_collector_info(await self._get_json(url))

    async def query_collector_status(self, *, pn: str) -> Any:
        """Call action `queryCollectorStatus` (chapter 4)."""
        url = _actions.url_query_collector_status(
            self._config, self._require_auth(), pn=pn
        )
        return _actions.parse_query_collector_status(await self._get_json(url))

    async def query_collector_devices(self, *, pn: str) -> Any:
        """Call action `queryCollectorDevices` (chapter 4)."""
        url = _actions.url_query_collector_devices(
            self._config, self._require_auth(), pn=pn
        )
        return _actions.parse_query_collector_devices(await self._get_json(url))

    async def query_devices(
        self, *, page: int | None = None, pagesize: int | None = None
    ) -> Any:
        """Call action `queryDevices` (chapter 5)."""
        url = _actions.url_query_devices(
            self._config, self._require_auth(), page=page, pagesize=pagesize
        )
        return _actions.parse_query_devices(await self._get_json(url))

    async def web_query_device_es(self) -> Any:
        """Call action `webQueryDeviceEs` (chapter 5)."""
        url = _actions.url_web_query_device_es(self._config, self._require_auth())
        return _actions.parse_web_query_device_es(await self._get_json(url))

    async def query_device_count(self) -> Any:
        """Call action `queryDeviceCount` (chapter 5)."""
        url = _actions.url_query_device_count(self._config, self._require_auth())
        return _actions.parse_query_device_count(await self._get_json(url))

    async def query_device_info(
        self, *, pn: str, devcode: int, devaddr: int, sn: str
    ) -> Any:
        """Call action `queryDeviceInfo` (chapter 5)."""
        url = _actions.url_query_device_info(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
        )
        return _actions.parse_query_device_info(await self._get_json(url))

    async def query_device_last_data(
        self, *, pn: str, devcode: int, devaddr: int, sn: str
    ) -> Any:
        """Call action `queryDeviceLastData` (chapter 5)."""
        url = _actions.url_query_device_last_data(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
        )
        return _actions.parse_query_device_last_data(await self._get_json(url))

    async def query_sp_device_last_data(
        self, *, pn: str, devcode: int, devaddr: int, sn: str
    ) -> Any:
        """Call action `querySPDeviceLastData` (chapter 5)."""
        url = _actions.url_query_sp_device_last_data(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
        )
        return _actions.parse_query_sp_device_last_data(await self._get_json(url))

    async def query_device_data_one_day(
        self, *, pn: str, devcode: int, devaddr: int, sn: str, date: str
    ) -> Any:
        """Call action `queryDeviceDataOneDay` (chapter 5)."""
        url = _actions.url_query_device_data_one_day(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
            date=date,
        )
        return _actions.parse_query_device_data_one_day(await self._get_json(url))

    async def query_device_status(
        self, *, pn: str, devcode: int, devaddr: int, sn: str
    ) -> Any:
        """Call action `queryDeviceStatus` (chapter 5)."""
        url = _actions.url_query_device_status(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
        )
        return _actions.parse_query_device_status(await self._get_json(url))

    async def query_device_warning(
        self, *, pn: str, devcode: int, devaddr: int, sn: str
    ) -> Any:
        """Call action `queryDeviceWarning` (chapter 5)."""
        url = _actions.url_query_device_warning(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
        )
        return _actions.parse_query_device_warning(await self._get_json(url))

    async def ctrl_device(
        self, *, pn: str, devcode: int, devaddr: int, sn: str, id: str, val: str
    ) -> Any:
        """Call action `ctrlDevice` (chapter 5)."""
        url = _actions.url_ctrl_device(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
            id=id,
            val=val,
        )
        return _actions.parse_ctrl_device(await self._get_json(url))

    async def query_device_energy_day(
        self, *, pn: str, devcode: int, devaddr: int, sn: str, date: str
    ) -> Any:
        """Call action `queryDeviceEnergyDay` (chapter 6)."""
        url = _actions.url_query_device_energy_day(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
            date=date,
        )
        return _actions.parse_query_device_energy_day(await self._get_json(url))

    async def query_device_energy_month(
        self, *, pn: str, devcode: int, devaddr: int, sn: str, date: str
    ) -> Any:
        """Call action `queryDeviceEnergyMonth` (chapter 6)."""
        url = _actions.url_query_device_energy_month(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
            date=date,
        )
        return _actions.parse_query_device_energy_month(await self._get_json(url))

    async def query_device_energy_year(
        self, *, pn: str, devcode: int, devaddr: int, sn: str, date: str
    ) -> Any:
        """Call action `queryDeviceEnergyYear` (chapter 6)."""
        url = _actions.url_query_device_energy_year(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
            date=date,
        )
        return _actions.parse_query_device_energy_year(await self._get_json(url))

    async def query_device_energy_total(
        self, *, pn: str, devcode: int, devaddr: int, sn: str
    ) -> Any:
        """Call action `queryDeviceEnergyTotal` (chapter 6)."""
        url = _actions.url_query_device_energy_total(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
        )
        return _actions.parse_query_device_energy_total(await self._get_json(url))

    async def query_device_active_ouput_power_current(
        self, *, pn: str, devcode: int, devaddr: int, sn: str
    ) -> Any:
        """Call action `queryDeviceActiveOuputPowerCurrent` (chapter 6)."""
        url = _actions.url_query_device_active_ouput_power_current(
            self._config,
            self._require_auth(),
            pn=pn,
            devcode=devcode,
            devaddr=devaddr,
            sn=sn,
        )
        return _actions.parse_query_device_active_ouput_power_current(
            await self._get_json(url)
        )

    async def query_camera_info(self, *, cameraid: int) -> Any:
        """Call action `queryCameraInfo` (chapter 11)."""
        url = _actions.url_query_camera_info(
            self._config, self._require_auth(), cameraid=cameraid
        )
        return _actions.parse_query_camera_info(await self._get_json(url))

    async def upload_img(self, *, fmt: str) -> Any:
        """Call action `uploadImg` (chapter 84)."""
        url = _actions.url_upload_img(self._config, self._require_auth(), fmt=fmt)
        return _actions.parse_upload_img(await self._get_json(url))
