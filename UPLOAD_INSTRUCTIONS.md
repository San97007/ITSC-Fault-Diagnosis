# How to upload this supplement to San97007/ITSC-Fault-Diagnosis

This folder contains only the files that are **new or changed** relative
to what is currently live at
https://github.com/San97007/ITSC-Fault-Diagnosis (checked 2026-07-20).
It is meant to be merged into the existing repository, not used to
replace it wholesale.

## What is currently missing from the live repository

Comparing the live repository against the manuscript's Section 4.4
("Ablation Study") and its three new tables, the following were not yet
present:

- `code/run_ablation_sensor_selection.py`
- `code/run_ablation_inversion_method.py`
- `data/table_ablation_sensor.csv`
- `data/table_ablation_pso.csv`
- `data/table_ablation_dt.csv`
- `manuscript_ablation_study_section.tex` (the LaTeX text for Section 4.4 itself)
- An up-to-date `README.md` and `data/data_dictionary.md` that reference the
  above, and that document the two raw `.rar` archives you already
  uploaded (`220-36V 20T NO FAULTS.rar` and `data/20241113.rar`), which
  were not described anywhere in the repository.

## Upload steps (GitHub web UI, no git command line needed)

1. Go to https://github.com/San97007/ITSC-Fault-Diagnosis
2. Open the `code/` folder → "Add file" → "Upload files" → drag in
   `run_ablation_sensor_selection.py` and `run_ablation_inversion_method.py`
   from this supplement's `code/` folder → commit directly to `main`.
3. Open the `data/` folder → "Add file" → "Upload files" → drag in
   `table_ablation_sensor.csv`, `table_ablation_pso.csv`,
   `table_ablation_dt.csv`, and `RAW_DATA_README.md` from this
   supplement's `data/` folder → commit.
4. Still in `data/`, click on the existing `data_dictionary.md` → pencil
   (edit) icon → select all → paste in the contents of this supplement's
   `data/data_dictionary.md` → commit.
5. Go to the repository root → click on the existing `README.md` →
   pencil icon → select all → paste in the contents of this supplement's
   `README.md` → commit.
6. At the repository root → "Add file" → "Upload files" → drag in
   `manuscript_ablation_study_section.tex` → commit.
7. **Clean-up:** open the file literally named `data set` (1 byte, empty
   placeholder) at the repository root → trash-can/delete icon → commit
   the deletion. It carries no information and could itself be read as
   evidence of an incompletely prepared repository.
8. **Fill in `data/RAW_DATA_README.md`** with the real acquisition
   details for your two `.rar` archives (sampling rate, channel mapping,
   trial IDs — see the bracketed placeholders in that file).

## After uploading: get a DOI (required by the Editor's letter)

The Editor's decision letter explicitly requires deposit in "a
recognised DOI-assigning repository (e.g. zenodo)" — a GitHub link alone
does not satisfy this. Once steps 1-8 above are done:

1. Go to https://zenodo.org → log in with your GitHub account.
2. In Zenodo, go to your GitHub account settings (https://zenodo.org/account/settings/github/)
   and toggle ON the `San97007/ITSC-Fault-Diagnosis` repository.
3. Back on GitHub, go to the repository → "Releases" → "Create a new
   release" → tag it (e.g. `v1.1`) → publish.
4. Zenodo automatically archives that release and mints a DOI within a
   few minutes (check https://zenodo.org/account/settings/github/ or
   your Zenodo uploads page).
5. Send me the resulting DOI (format `10.5281/zenodo.XXXXXXX`) and I
   will insert it into the Response to Editor Comments and the
   manuscript's Data/Code Availability sections in place of the current
   placeholder text.
