"""Read inverter configuration via `queryDeviceCtrlField` + `queryDeviceCtrlValue`.

`queryDeviceCtrlField` returns the schema (id, name, unit, allowed
options) for every settable field on a device. `queryDeviceCtrlValue`
returns the current value for each id. Joining them gives a complete
settings snapshot. Pair the printed `id` with `api.ctrl_device(id=...,
val=...)` to write a new value.
"""

import os

from dotenv import load_dotenv
from shinemonitor_api import ShineMonitorAPI

load_dotenv()
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]


def main() -> None:
    api = ShineMonitorAPI()
    api.login(USERNAME, PASSWORD)

    for device in api.get_devices():
        print(f"\n=== {device.device_alias or device.serial_number} ===")
        schema = api.query_device_ctrl_field(
            pn=device.wifi_pin,
            devcode=device.device_code,
            devaddr=device.device_address,
            sn=device.serial_number,
        )
        values = api.query_device_ctrl_value(
            pn=device.wifi_pin,
            devcode=device.device_code,
            devaddr=device.device_address,
            sn=device.serial_number,
        )

        current = {
            f["id"]: f.get("val", "") for f in values.get("dat", {}).get("field", [])
        }

        for field in schema.get("dat", {}).get("field", []):
            fid = field["id"]
            val = current.get(fid, "")
            line = f"  {fid:40s} = {val!r}"
            if unit := field.get("unit"):
                line += f" {unit}"
            print(line)

            for opt in field.get("item", []) or []:
                marker = " <--" if str(opt["key"]) == str(val) else ""
                print(f"      {opt['key']}: {opt['val']}{marker}")


if __name__ == "__main__":
    main()
