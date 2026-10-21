# ESPHome: local Bluetooth control for Best / Broan-NuTone range hoods

Control a **Best** range hood (the "Best Kitchen" app) from Home Assistant **without the cloud**, using a cheap ESP32 running ESPHome.

## Supported models

| Model | File | What works over Bluetooth |
|---|---|---|
| **HBN1306SS** | `best-hood.yaml` | everything below |
| **WCS1306SS** | `best-hood-wcs1306ss.yaml` | fan (4 speeds), light **on/off**, SmartSense. This model has no light-level or delay-off characteristic over Bluetooth: Best's app reaches those through its cloud. |

Other Best / Broan-NuTone hoods using the same app may work: please open an issue with your model, working or not.

With `best-hood.yaml` you get in Home Assistant:

| Entity | What it does |
|---|---|
| Fan | 4 speeds, off |
| Light | 3 levels (brightness is mapped to level 1-3) |
| SmartSense | the hood's automatic mode |
| Delay off | the hood's delayed stop |
| Bluetooth | is the ESP32 connected to the hood |
| Model, Wi-Fi signal, Restart, Reconnect | diagnostics |

Changes made with the hood's own buttons show up in Home Assistant right away. The phone app keeps working alongside the ESP32.

## What you need

- An ESP32 with Bluetooth (tested: ESP-WROOM-32 "esp32dev"), powered near the hood (a few metres).
- ESPHome (the Home Assistant app or the CLI).

## Install

1. Copy the file for your model (see the table above) into your ESPHome folder.
2. Add to your ESPHome `secrets.yaml`: `wifi_ssid`, `wifi_password`, `best_hood_api_key` (generate one in the ESPHome dashboard), `best_hood_ap_password`.
3. Put your hood's Bluetooth address in `hood_mac` (see below).
4. Install on the ESP32, then add the device in Home Assistant (it is discovered automatically).

### Find your hood's Bluetooth address

The hood only appears on Bluetooth **after** it hears the wake-up advertisement. Flash the file once with the placeholder address, then watch the ESP32 logs for a minute. As long as the ESP32 is not connected, it prints every hood whose name starts with `BEST`:

```
[I][hood]: Found 'BEST WCS1306SS' at XX:XX:XX:XX:XX:XX (RSSI -62)
```

Put that address in `hood_mac` and install again. Until then, `Connection open error, status=133` lines are normal: the ESP32 is trying to reach the placeholder address.

Shortcut: on our HBN1306SS the Bluetooth address is the hood's Wi-Fi MAC + 2 (for example Wi-Fi `…:A0` → Bluetooth `…:A2`), so your router may already show it.

Nothing shows up? Keep the ESP32 within a few metres of the hood and close the Best Kitchen app on your phone while testing.

## How it works

The protocol was found by analysing the Best Kitchen app:

1. **Wake-up advertisement.** The hood is invisible on Bluetooth until it sees an advertisement with company ID `0x5665` and the bytes `E4 D6 14 27 35 47`. The ESP32 broadcasts it all the time. These 6 bytes are **not an address**: they are a fixed constant hard-coded in the Best Kitchen app (`[228, 214, 20, 39, 53, 71]`), the same for every hood and every phone, so you don't need to change them.
2. **Pairing without bonding.** Reads fail until the link is encrypted, but the hood drops the connection if asked to store a bond. "Just Works" encryption **without bonding** (`auth_req_mode: no_bond`) works, so it is redone on every connection.
3. **Values** are single ASCII digits in GATT service `47e36221-a32f-4980-bf17-341fd4f20000`:

| Characteristic (…suffix) | Meaning |
|---|---|
| 21001 | fan on/off (0/1) |
| 21005 | fan speed (0 = off, 1-4) |
| 21020 | light on/off (0/1), also on the WCS1306SS |
| 21026 | light level (0 = off, 1-3), not on the WCS1306SS |
| 21040 | SmartSense (0/1) |
| 21050 | delay off (0/1), not on the WCS1306SS |
| 11065 | model |

Writes need a response. The hood notifies every change.

**Safety:** the ESP32 never writes anything before it has received the hood's current values, so an ESP32 reboot never switches the hood off.

## Known limits

- Tested on **one** HBN1306SS (September 2026) and **one** WCS1306SS (October 2026, thanks to the user who reported it in [issue #1](https://github.com/WheapLabs/esphome-best-hood/issues/1)).
- The wake-up bytes work on both models. If your hood stays invisible, please report it.
- ESPHome logs `Cannot poll, not connected` for a characteristic your hood doesn't have, even while the link is fine. On the WCS1306SS, use its own file so these lines don't appear.
- A hood firmware update could change the protocol.
- The hood's Wi-Fi/cloud control is not used.

## License

MIT — © 2026 WheapLabs. Not affiliated with Best or Broan-NuTone.
