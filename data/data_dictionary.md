# Data Dictionary

This directory contains the tabular data reported in the manuscript
"Digital Twin-Driven Micromagnetic Field Inversion for ITSC Fault
Diagnosis in Power Transformers" (Wang & Wang). Each file corresponds to
one table (or sub-table) in the manuscript. See `DATA_LICENSE.md` for
licensing.

| File | Manuscript reference | Contents | Provenance |
|---|---|---|---|
| `table1_inversion_trials.csv` | Table 1 | Six synthetic validation trials: target vs. calculated fault location `z` and dipole moment `M`, with location/severity errors `e_z`, `e_M` | Authors' PSO inversion validation runs |
| `table_bh_curve_50W470.csv` | Table (B-H, tab:BH) | Nine H-B-mu_r data points for grade 50W470 silicon steel | Digitized from IEC 60404-2; see `DATA_LICENSE.md` |
| `table2_transformer_parameters.csv` | Table 2 | Prototype transformer electrical/geometric parameters | Authors' experimental prototype specification |
| `table_mesh_parameters.csv` | Table (tab:mesh) | FEM mesh element sizes per model region | Authors' COMSOL model configuration |
| `table_sensor_selection_examples.csv` | Table (tab:sensor_selection) | Selected sensor subsets `K` for three representative fault locations | Output of Algorithm 1 (sensor selection) as reported in the manuscript |
| `table_pso_parameters.csv` | Table (tab:pso) | Complete PSO hyperparameter configuration | Authors' PSO implementation configuration |
| `table_statistics_CI.csv` | Table (tab:statistics) | Per-trial mean +/- std and 95% CI of `e_z`, `e_M` across 10 independent PSO restarts | Authors' statistical robustness evaluation |
| `table_noise_robustness.csv` | Table (tab:noise) | Average inversion errors at SNR = 30/20/10 dB and no-noise baseline | Authors' noise-robustness evaluation |
| `table_domaingap.csv` | Table (tab:domaingap) | Aggregate MAE/RMSE/MRE/cosine-similarity between simulated and measured leakage flux, healthy vs. ITSC | Authors' DT fidelity validation |
| `table_persensor_domaingap.csv` | Table (tab:persensor) | Per-sensor (S1-S12) simulated vs. measured leakage flux density and errors, healthy and ITSC (z=130 mm) states | Authors' Hall-sensor DAQ measurements + DT simulation output |
| `table_strategy_comparison.csv` | Table (tab:strategy) | Inversion errors under physical-only / virtual-only / physical-virtual fusion strategies (ablation-style comparison) | Authors' ablation-style comparison across the six trials |
| `table3_final_inversion_result.csv` | Table 3 | Experimental vs. inverted fault location/severity for the physical validation case | Authors' physical transformer ITSC experiment |
| `table_dt_update_cycle.csv` | Table (tab:dtcycle) | Digital twin parameter update categories, frequencies, and trigger conditions | Authors' DT synchronization design |

## Important note on raw waveform data

The tables above are the **summary/derived statistics** reported in the
manuscript. The underlying **raw time-series DAQ exports** from the 12
S49E Hall sensors (NI USB-6341 acquisition card) that were used to compute
`table_persensor_domaingap.csv` and `table3_final_inversion_result.csv`
are not included in this initial deposit. If the journal or reviewers
require the raw waveform files for full reproducibility, the authors
should export them from the original DAQ software (typically as
timestamped CSV or TDMS files, one file per sensor per trial) and add them
under a new `data/raw/` subdirectory, referencing the specific trial and
sensor in the filename (e.g. `raw/trial5_S1_healthy.csv`).
