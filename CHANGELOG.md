# Changelog

All notable changes to this project are listed here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions will follow
[Semantic Versioning](https://semver.org/). No version has been tagged yet.

## [Unreleased]

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
