### Fixed

- HBN542912SS: the fan speed set from Home Assistant now reaches the hood. With more than 4 fan
  speeds, `best-hood.yaml` writes and reads the speed on characteristic `21017` instead of `21005`,
  which this model ignores; the new `fan_speed_char` setting can force either one. Hoods with 4
  speeds are unchanged. Found and tested by the contributor in
  [#12](https://github.com/WheapLabs/esphome-best-hood/issues/12)
  ([#17](https://github.com/WheapLabs/esphome-best-hood/pull/17)).

### Documentation

- README: the HBN542912SS is listed as fully working; `21017` and the colour temperature values of
  `21090` (0 = warmest to 7 = coolest) are documented.
