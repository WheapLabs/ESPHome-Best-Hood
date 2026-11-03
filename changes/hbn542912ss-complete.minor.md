### Added

- `extra_settings: "true"` adds the light colour temperature and the SmartSense mode, sensitivity,
  light and light delay found on the HBN542912SS. Off by default: the entities are then hidden and
  never read or written, so other hoods work as before. Found by the contributor in
  [#16](https://github.com/WheapLabs/esphome-best-hood/issues/16)
  ([#17](https://github.com/WheapLabs/esphome-best-hood/pull/17)).

### Fixed

- HBN542912SS: the fan speed set from Home Assistant now reaches the hood. With more than 4 fan
  speeds, `best-hood.yaml` writes and reads the speed on characteristic `21017` instead of `21005`,
  which this model ignores; the new `fan_speed_char` setting can force either one. Hoods with 4
  speeds are unchanged. Found and tested by the contributor in
  [#12](https://github.com/WheapLabs/esphome-best-hood/issues/12)
  ([#17](https://github.com/WheapLabs/esphome-best-hood/pull/17)).

### Changed

- The automatic check validates the file with ESPHome 2026.10.2, the latest release.
