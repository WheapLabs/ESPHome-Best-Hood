# Changelog

All notable changes to this project are listed here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions follow
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- A check on every pull request: `esphome config` on `best-hood*.yaml` with throwaway
  secrets, and a secret scan (gitleaks).

## [1.1.0] - 2026-10-26

### Removed

- `best-hood-wcs1306ss.yaml`: with the GATT cache fix of v1.0.1, a WCS1306SS
  works fully with `best-hood.yaml` (fan with 4 speeds, light on/off and
  levels, delay off, SmartSense;
  [#1](https://github.com/WheapLabs/esphome-best-hood/issues/1),
  [#8](https://github.com/WheapLabs/esphome-best-hood/pull/8)). If you use
  the old file, switch to `best-hood.yaml`.

### Documentation

- README (EN/FR): one file, `best-hood.yaml`, for the three confirmed models
  (HBN1306SS, HBN65366SS, WCS1306SS); add the HBN65366SS and WCS1306SS notes.

## [1.0.1] - 2026-10-24

### Fixed

- Both files raise ESP-IDF's GATT characteristic cache
  (`CONFIG_BT_GATTC_MAX_CACHE_CHAR: "100"`). The default of 40 silently hid
  the last characteristics of hoods that have more: on an HBN65366SS (54
  characteristics) the light level (`21026`) and delay-off (`21050`) were
  missing and logged `Cannot poll, not connected`
  ([#5](https://github.com/WheapLabs/esphome-best-hood/pull/5)).

## [1.0.0] - 2026-10-21

### Added

- `best-hood.yaml`: local Bluetooth control of the Best HBN1306SS with an
  ESP32 (fan with 4 speeds, light with 3 levels, SmartSense, delay-off,
  connection and diagnostics), no cloud.
- `best-hood-wcs1306ss.yaml` for the WCS1306SS: fan, light on/off and
  SmartSense, the only features it offers over Bluetooth
  ([#1](https://github.com/WheapLabs/esphome-best-hood/issues/1), [#2](https://github.com/WheapLabs/esphome-best-hood/pull/2)).
- English and French README with the protocol notes.
- This changelog and a pull request template.

### Fixed

- "Find your hood's Bluetooth address": each nearby `BEST…` hood and its
  address are now logged while the ESP32 is not connected
  ([#2](https://github.com/WheapLabs/esphome-best-hood/pull/2)).

[Unreleased]: https://github.com/WheapLabs/esphome-best-hood/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/WheapLabs/esphome-best-hood/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/WheapLabs/esphome-best-hood/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/WheapLabs/esphome-best-hood/releases/tag/v1.0.0
