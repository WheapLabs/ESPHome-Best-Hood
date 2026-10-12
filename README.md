# ESPHome: local Bluetooth control for Best / Broan-NuTone range hoods

Control a **Best HBN1306SS** range hood (the "Best Kitchen" app) from Home Assistant **without the cloud**, using a cheap ESP32 running ESPHome.

You get in Home Assistant:

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

1. Copy `best-hood.yaml` into your ESPHome folder.
2. Add to your ESPHome `secrets.yaml`: `wifi_ssid`, `wifi_password`, `best_hood_api_key` (generate one in the ESPHome dashboard), `best_hood_ap_password`.
3. Put your hood's Bluetooth address in `hood_mac` (see below).
4. Install on the ESP32, then add the device in Home Assistant (it is discovered automatically).

### Find your hood's Bluetooth address

The hood only appears on Bluetooth **after** it hears the wake-up advertisement, so flash the file once with any address, then look at the ESP32 logs: a device named `BEST HBN1306SS` shows up. Its address (on our unit, the hood's Wi-Fi MAC + 2) goes into `hood_mac`. Install again.

## How it works

The protocol was found by analysing the Best Kitchen app:

1. **Wake-up advertisement.** The hood is invisible on Bluetooth until it sees an advertisement with company ID `0x5665` and the bytes `E4 D6 14 27 35 47`. The ESP32 broadcasts it all the time. These 6 bytes are **not an address**: they are a fixed constant hard-coded in the Best Kitchen app (`[228, 214, 20, 39, 53, 71]`), the same for every hood and every phone, so you don't need to change them.
2. **Pairing without bonding.** Reads fail until the link is encrypted, but the hood drops the connection if asked to store a bond. "Just Works" encryption **without bonding** (`auth_req_mode: no_bond`) works, so it is redone on every connection.
3. **Values** are single ASCII digits in GATT service `47e36221-a32f-4980-bf17-341fd4f20000`:

| Characteristic (…suffix) | Meaning |
|---|---|
| 21001 | fan on/off (0/1) |
| 21005 | fan speed (0 = off, 1-4) |
| 21020 | light on/off (0/1) |
| 21026 | light level (0 = off, 1-3) |
| 21040 | SmartSense (0/1) |
| 21050 | delay off (0/1) |
| 11065 | model |

Writes need a response. The hood notifies every change.

**Safety:** the ESP32 never writes anything before it has received the hood's current values, so an ESP32 reboot never switches the hood off.

## Known limits

- Tested on **one** HBN1306SS (September 2026). Other Best / Broan-NuTone hoods using the same app may work — please open an issue with your model, working or not.
- We don't know yet if the wake-up bytes are the same for every hood. If yours stays invisible, please report it.
- A hood firmware update could change the protocol.
- The hood's Wi-Fi/cloud control is not used.

## License

MIT — © 2026 WheapLabs. Not affiliated with Best or Broan-NuTone.
