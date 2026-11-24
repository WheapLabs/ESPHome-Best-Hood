### Added

- Automatic Bluetooth watchdog: if the encrypted link to the hood stays down, the ESP32 retries a
  clean Bluetooth reconnect after 2 and 4 minutes, then performs a clean reboot after 6 minutes to
  reset the BLE stack without needing a power cycle (reboot is skipped while `hood_mac` is still
  the placeholder `AA:BB:CC:DD:EE:FF` during initial setup).

### Fixed

- Reset the cached fan speed on Bluetooth disconnect so the `Bluetooth` diagnostic sensor only
  reports connected again once encrypted readings actually resume.
