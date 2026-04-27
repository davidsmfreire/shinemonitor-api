"""Read inverter configuration via `queryDeviceCtrlField`.

Lists every settable field for each connected device with current value
and (when applicable) the enumerated options. Pair the printed `id` with
`api.ctrl_device(id=..., val=...)` to write a new value.
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
        payload = api.query_device_ctrl_field(
            pn=device.wifi_pin,
            devcode=device.device_code,
            devaddr=device.device_address,
            sn=device.serial_number,
        )

        for field in payload.get("dat", {}).get("field", []):
            line = f"  {field['id']:40s} = {field.get('val', '')!r}"
            if unit := field.get("unit"):
                line += f" {unit}"
            print(line)

            for opt in field.get("item", []) or []:
                marker = " <--" if str(opt["key"]) == str(field.get("val")) else ""
                print(f"      {opt['key']}: {opt['val']}{marker}")


if __name__ == "__main__":
    main()
