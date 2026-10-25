# Changelog

All notable changes to this project are listed here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions follow
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Documentation

- README (EN/FR): add the confirmed HBN65366SS model and update WCS1306SS notes for v1.0.1.

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

[Unreleased]: https://github.com/WheapLabs/esphome-best-hood/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/WheapLabs/esphome-best-hood/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/WheapLabs/esphome-best-hood/releases/tag/v1.0.0
