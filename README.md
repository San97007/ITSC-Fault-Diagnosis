# Digital Twin-Driven Micromagnetic Field Inversion for ITSC Fault Diagnosis in Power Transformers — Code and Data

This repository accompanies the manuscript and provides:

1. A runnable Python implementation of the two custom algorithms described
   in the manuscript:
   - *Composite utility-based sensor selection*(Algorithm 1, Section
     "Multi-sensor Information Fusion of Micromagnetic Field").
   - *PSO-based ITSC fault inversion*, using the exact hyperparameters in
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
├── manuscript_ablation_study_section.tex <- Section 4.4 text, ready to paste into the manuscript
├── code/
│   ├── dipole_model.py                <- forward model (Eq. dipole)
│   ├── pso_optimizer.py               <- generic PSO engine (Table tab:pso config)
│   ├── sensor_selection.py            <- Algorithm 1
│   ├── run_inversion_demo.py          <- reproduces Table 1 / statistics table
│   ├── run_noise_robustness.py        <- reproduces Table tab:noise
│   ├── run_sensor_selection_demo.py   <- reproduces Table tab:sensor_selection
│   ├── run_ablation_sensor_selection.py <- reproduces Table tab:ablation_sensor
│   ├── run_ablation_inversion_method.py <- reproduces Table tab:ablation_pso
│   └── requirements.txt
├── data/
│   ├── data_dictionary.md             <- describes every CSV file
│   ├── DATA_LICENSE.md                <- CC-BY-4.0 (with one noted exception)
│   └── table*.csv                     <- one file per manuscript table
└── comsol/
    └── model_description.md           <- FEM digital-twin build description
```

## Raw experimental data

Two raw Hall-sensor DAQ archives are included at the repository root and
under `data/`: `220-36V 20T NO FAULTS.rar` and `data/20241113.rar`.
**Please complete `data/RAW_DATA_README.md`** with the acquisition
details (sampling rate, channel mapping, trial IDs, etc.) for these
archives.

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

# Ablation study (Section 4.4): sensor selection module
python run_ablation_sensor_selection.py

# Ablation study (Section 4.4): inversion method module
python run_ablation_inversion_method.py
```


## Citation

If you use this code or data, please cite the manuscript (final citation
to be added upon publication) and this Zenodo record.

## License

- Code: MIT (see `LICENSE`).
- Data: CC-BY-4.0, with one noted exception for a small excerpt of
  IEC 60404-2 standard data (see `data/DATA_LICENSE.md`).
