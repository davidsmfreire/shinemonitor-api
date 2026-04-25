"""Pull a live snapshot for every inverter on the account, async."""

import asyncio
import os

from dotenv import load_dotenv
from shinemonitor_api.aio import AsyncShineMonitorAPI

load_dotenv()
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]


async def main() -> None:
    async with AsyncShineMonitorAPI() as api:
        await api.login(USERNAME, PASSWORD)
        devices = await api.get_devices()
        snapshots = await asyncio.gather(
            *(api.get_last_data(device) for device in devices)
        )
        for device, snapshot in zip(devices, snapshots):
            print(f"{device.device_alias or device.serial_number}: {snapshot.main}")


if __name__ == "__main__":
    asyncio.run(main())
