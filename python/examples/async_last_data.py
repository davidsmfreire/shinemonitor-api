"""Pull a live snapshot for a known inverter, async."""

import asyncio
import os

from dotenv import load_dotenv
from shinemonitor_api.aio import AsyncShineMonitorAPI
from shinemonitor_api.models import DeviceIdentifier

load_dotenv()
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]
SERIAL_NUMBER = os.environ["SERIAL_NUMBER"]
WIFI_PN = os.environ["WIFI_PN"]
DEV_CODE = int(os.environ["DEV_CODE"])
DEV_ADDR = int(os.environ["DEV_ADDR"])


async def main() -> None:
    device = DeviceIdentifier(
        sn=SERIAL_NUMBER,
        pn=WIFI_PN,
        devcode=DEV_CODE,
        devaddr=DEV_ADDR,
        devalias=None,
    )
    async with AsyncShineMonitorAPI() as api:
        await api.login(USERNAME, PASSWORD)
        snapshot = await api.get_last_data(device)
        print(snapshot.main)


if __name__ == "__main__":
    asyncio.run(main())
