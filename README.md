# Digital Twin-Driven Micromagnetic Field Inversion for ITSC Fault Diagnosis in Power Transformers — Code and Data

**说明（中文）：** 本仓库是论文《Digital Twin-Driven Micromagnetic Field Inversion for
ITSC Fault Diagnosis in Power Transformers》（Wang & Wang）配套的代码与数据集，
用于满足期刊关于 Code/Data Availability 的要求，可直接打包上传 Zenodo 生成 DOI。
详见下方英文说明与 `CODE_DATA_AVAILABILITY_STATEMENT.md` 中可直接粘贴进稿件的文字。

---

This repository accompanies the manuscript and provides:

1. A runnable Python implementation of the two custom algorithms described
   in the manuscript:
   - **Composite utility-based sensor selection** (Algorithm 1, Section
     "Multi-sensor Information Fusion of Micromagnetic Field").
   - **PSO-based ITSC fault inversion** (Section "ITSC Diagnosis Based on
     Particle Swarm Optimization"), using the exact hyperparameters in
     Table "Complete PSO Parameter Configuration".
2. All summary/derived data tables reported in the manuscript, as CSV
   files with a data dictionary.
3. A build description for the COMSOL digital-twin finite-element model.
4. Draft Code/Data Availability text for the manuscript.

## Repository structure

```
.
├── README.md                          <- this file
├── LICENSE                            <- MIT license (code)
├── CODE_DATA_AVAILABILITY_STATEMENT.md<- text to paste into the manuscript
├── code/
│   ├── dipole_model.py                <- forward model (Eq. dipole)
│   ├── pso_optimizer.py               <- generic PSO engine (Table tab:pso config)
│   ├── sensor_selection.py            <- Algorithm 1
│   ├── run_inversion_demo.py          <- reproduces Table 1 / statistics table
│   ├── run_noise_robustness.py        <- reproduces Table tab:noise
│   ├── run_sensor_selection_demo.py   <- reproduces Table tab:sensor_selection
│   └── requirements.txt
├── data/
│   ├── data_dictionary.md             <- describes every CSV file
│   ├── DATA_LICENSE.md                <- CC-BY-4.0 (with one noted exception)
│   └── table*.csv                     <- one file per manuscript table
└── comsol/
    └── model_description.md           <- FEM digital-twin build description
```

## Requirements

```bash
pip install -r code/requirements.txt   # numpy>=1.24, scipy>=1.10
```
Python 3.9+ recommended.

## Running the code

```bash
cd code

# Algorithm 1: composite utility-based sensor selection
python run_sensor_selection_demo.py

# PSO fault inversion (reproduces the six-trial validation methodology)
python run_inversion_demo.py

# Noise robustness sweep (30/20/10 dB SNR)
python run_noise_robustness.py
```

Each script prints its results to stdout and documents, in its own
docstring, exactly which manuscript equation/table it corresponds to.

## IMPORTANT — read before treating this as a full reproduction package

This code faithfully implements the **methods** described in the
manuscript (forward model, sensor-selection algorithm, PSO configuration).
It does **not** have access to the authors' original COMSOL simulation
files or raw Hall-sensor DAQ exports, which were not available at the time
this package was assembled. Consequently:

- `run_inversion_demo.py` and `run_noise_robustness.py` generate
  synthetic "measured" sensor data using the forward model plus Gaussian
  sensor noise (sigma = 5 mT, per the S49E datasheet), rather than reading
  real DAQ files. Results are internally consistent but will **not**
  reproduce the manuscript's published numbers digit-for-digit.
- `run_sensor_selection_demo.py` uses illustrative synthetic P_i/V_i/DS_i
  criterion profiles, since the manuscript reports only the selection
  *outcome* (Table tab:sensor_selection), not the underlying raw
  correlation/variance/symmetry values.
- The forward-model calibration constant `C` (see `dipole_model.py`) uses
  a principled default (`C = r0^3`, so that `M` represents approximately
  the peak flux density at the sensor nearest the fault) rather than a
  value fitted to the authors' internal DT calibration, which was not
  reported in the manuscript at a level of detail sufficient to invert it
  exactly.

**Before final Zenodo deposit, the corresponding author should:**
1. Add the original per-sensor DAQ exports (raw time-series or the
   per-trial readings used to build `data/table_persensor_domaingap.csv`
   and `data/table1_inversion_trials.csv`) under `data/raw/`.
2. Replace the synthetic-data generators in `run_inversion_demo.py`,
   `run_noise_robustness.py`, and `run_sensor_selection_demo.py` with
   loaders that read the real DAQ files.
3. If available, add the native COMSOL `.mph` model file (or an export
   script) under `comsol/`.
4. Re-run all three demo scripts and confirm the printed results now
   match the manuscript's published tables; update this README's
   "IMPORTANT" section accordingly once they do.

Doing so converts this package from "algorithm reference implementation"
to a fully reproducing package, which is what reviewers and the editor
are asking for.

## Citation

If you use this code or data, please cite the manuscript (final citation
to be added upon publication) and this Zenodo record (DOI to be added
after upload — Zenodo assigns it automatically when you publish).

## License

- Code: MIT (see `LICENSE`).
- Data: CC-BY-4.0, with one noted exception for a small excerpt of
  IEC 60404-2 standard data (see `data/DATA_LICENSE.md`).
