# Digital Twin-Driven Micromagnetic Field Inversion for ITSC Fault Diagnosis in Power Transformers — Code and Data

---

This repository accompanies the manuscript and provides:

1. A runnable Python implementation of the two custom algorithms described
   in the manuscript.
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


## License

- Code: MIT (see `LICENSE`).
- Data: CC-BY-4.0, with one noted exception for a small excerpt of
  IEC 60404-2 standard data (see `data/DATA_LICENSE.md`).
