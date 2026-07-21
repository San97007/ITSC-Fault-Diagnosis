# Raw Data Description (please complete before final submission)

This file documents the two raw Hall-sensor data-acquisition archives
already present in this repository. **The bracketed fields below must be
filled in by the authors** — they cannot be inferred from the archive
filenames alone, and an undocumented binary archive does not, by itself,
satisfy a reviewer/editor request for dataset transparency.

## `/220-36V 20T NO FAULTS.rar`

- **Condition:** Healthy (no ITSC fault) baseline
- **Transformer configuration:** 220/36 V, 20-turn LV winding (matches
  Table 2 prototype parameters)
- **Acquisition date:** [please specify]
- **Instrumentation:** [please specify, e.g. "12x S49E Hall sensors +
  NI USB-6341 DAQ card" — confirm against Section 4.2 of the manuscript]
- **Sampling rate:** [please specify, e.g. Hz]
- **Duration / number of samples per channel:** [please specify]
- **File format inside the archive:** [please specify, e.g. one CSV per
  sensor, or one multi-column CSV with a timestamp column + 12 sensor
  columns; include column headers if applicable]
- **Channel-to-sensor mapping:** [please specify, e.g. "column 1 = S1 at
  z = 8 mm ... column 12 = S12 at z = 192 mm", consistent with the sensor
  positions used in `code/dipole_model.py::sensor_positions_mm()`]
- **Corresponding manuscript table/figure:** [e.g. healthy-state columns
  of Table "tab:persensor", Fig. 10 healthy curve]

## `/data/20241113.rar`

- **Condition(s) covered:** [please specify — which ITSC fault
  location(s)/severity level(s), or multiple trials matching Table 1]
- **Acquisition date:** 2024-11-13 (from filename)
- **Instrumentation:** [please specify]
- **Sampling rate:** [please specify]
- **Duration / number of samples per channel per trial:** [please specify]
- **File format inside the archive:** [please specify]
- **Channel-to-sensor mapping:** [please specify]
- **Trial-ID mapping:** [please specify how files/folders inside the
  archive map to Trial 1-6 in Table 1, and/or to the z = 130 mm case in
  Table 3]

## Recommended follow-up

Once completed, consider extracting the raw archives into individual,
clearly named CSV files (e.g. `raw/healthy_S01.csv`,
`raw/trial3_fault_S07.csv`) rather than a single compressed archive —
this makes the data browsable directly on GitHub/Zenodo without
requiring a download and unrar step, which further improves
reproducibility.
