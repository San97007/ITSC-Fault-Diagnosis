"""
run_inversion_demo.py
-----------------------
Reproduces the methodology behind Table 1 ("Inversion Accuracy of
Inter-Turn Short Circuit Fault Parameters") and the per-trial statistical
evaluation table (mean/std/95% CI over N_r = 10 independent PSO restarts).

Workflow
--------
For each of the six test cases in data/table1_inversion_trials.csv:
  1. Generate synthetic "measured" sensor readings by evaluating the
     dipole forward model at the K selected sensor positions for the
     known target (z_obs, M_obs), then adding Gaussian measurement noise
     with sigma = 5 mT (S49E sensor noise spec).
  2. Invert (z_h, M) from the noisy readings using PSO with the exact
     hyperparameters in data/table_pso_parameters.csv (10 independent
     restarts, best-of-restarts selection).
  3. Report the recovered (z_cal, M_cal), the location/severity errors
     e_z and e_M, and the mean +/- std / 95% CI across the 10 restarts.

Note on reproducing the manuscript's exact published numbers
--------------------------------------------------------------
This script implements the *method* exactly as described (forward model,
objective function, PSO configuration). It does not have access to the
authors' original COMSOL-simulated or physically measured sensor
waveforms, so the "measured" data here are synthetically generated from
the forward model plus sensor noise, which is by construction internally
consistent but will not reproduce the manuscript's published (z_cal,
M_cal) values digit-for-digit. Before final Zenodo deposit, the authors
should replace the synthetic data-generation step in `simulate_measurement()`
with their original DAQ-exported sensor readings (see
data/table_persensor_domaingap.csv for the format used for raw per-sensor
exports elsewhere in this dataset).
"""

import csv
import os
import numpy as np
from scipy import stats

from dipole_model import dipole_field, sensor_positions_mm, DEFAULT_R0_MM, DEFAULT_CALIBRATION_CONSTANT
from pso_optimizer import PSOConfig, optimize

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
SENSOR_NOISE_SIGMA_MT = 5.0
N_SENSORS = 12
N_RESTARTS_FOR_STATS = 10  # matches manuscript's N_r


def load_trials(path):
    trials = []
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["trial"] == "avg":
                continue
            trials.append({
                "trial": int(row["trial"]),
                "z_obs": float(row["z_obs_mm"]),
                "M_obs": float(row["M_obs_mT"]),
            })
    return trials


def active_sensors_for_fault(z_h, all_positions, k_range=(4, 6)):
    """
    Emulate the adaptive sensor-selection outcome: choose the K sensors
    nearest the fault location, with K increasing from 4 to 6 as the fault
    moves toward the winding ends (consistent with the reported examples
    in data/table_sensor_selection_examples.csv). This is a simplified
    stand-in for the full Algorithm 1 pipeline in sensor_selection.py,
    used here only to determine which sensor subset feeds the inversion.
    """
    distances = np.abs(all_positions - z_h)
    order = np.argsort(distances)
    k = 4 if 40 < z_h < 160 else 6 if (z_h < 30 or z_h > 170) else 5
    return all_positions[np.sort(order[:k])]


def simulate_measurement(z_obs, M_obs, sensor_pos, rng):
    """Synthetic measurement generator (see module docstring)."""
    b_true = dipole_field(z_obs, M_obs, sensor_pos)
    noise = rng.normal(0.0, SENSOR_NOISE_SIGMA_MT, size=b_true.shape)
    return b_true + noise


def make_objective(b_meas, sensor_pos, sigma=SENSOR_NOISE_SIGMA_MT):
    w = 1.0 / sigma ** 2

    def objective(params):
        z_h, M = params
        b_model = dipole_field(z_h, M, sensor_pos)
        return np.sum(w * (b_meas - b_model) ** 2)

    return objective


def run_trial(trial, all_sensor_positions, rng, n_restarts=N_RESTARTS_FOR_STATS):
    z_obs, M_obs = trial["z_obs"], trial["M_obs"]
    sensor_pos = active_sensors_for_fault(z_obs, all_sensor_positions)

    ez_list, eM_list = [], []
    z_cal_best, M_cal_best, best_fit = None, None, np.inf

    for _ in range(n_restarts):
        b_meas = simulate_measurement(z_obs, M_obs, sensor_pos, rng)
        objective = make_objective(b_meas, sensor_pos)

        cfg = PSOConfig(n_restarts=1, seed=int(rng.integers(0, 1_000_000)))
        result = optimize(objective, cfg)
        z_cal, M_cal = result.best_position

        ez = abs(z_cal - z_obs) / 200.0 * 100.0     # Z = 200 mm winding height
        eM = abs(M_cal - M_obs) / M_obs * 100.0
        ez_list.append(ez)
        eM_list.append(eM)

        if result.best_fitness < best_fit:
            best_fit = result.best_fitness
            z_cal_best, M_cal_best = z_cal, M_cal

    ez_arr, eM_arr = np.array(ez_list), np.array(eM_list)
    ci_ez = stats.t.interval(0.95, len(ez_arr) - 1, loc=ez_arr.mean(),
                              scale=ez_arr.std(ddof=1) / np.sqrt(len(ez_arr)))
    ci_eM = stats.t.interval(0.95, len(eM_arr) - 1, loc=eM_arr.mean(),
                              scale=eM_arr.std(ddof=1) / np.sqrt(len(eM_arr)))

    return {
        "trial": trial["trial"],
        "z_obs": z_obs, "M_obs": M_obs,
        "z_cal": z_cal_best, "M_cal": M_cal_best,
        "ez_mean": ez_arr.mean(), "ez_std": ez_arr.std(ddof=1), "ez_ci95": ci_ez,
        "eM_mean": eM_arr.mean(), "eM_std": eM_arr.std(ddof=1), "eM_ci95": ci_eM,
    }


def main():
    trials = load_trials(os.path.join(DATA_DIR, "table1_inversion_trials.csv"))
    all_sensor_positions = sensor_positions_mm(N_SENSORS)
    rng = np.random.default_rng(42)

    print(f"{'Trial':>5} {'z_obs':>7} {'M_obs':>8} {'z_cal':>7} {'M_cal':>8} "
          f"{'e_z(%) mean+-std':>20} {'e_M(%) mean+-std':>20}")

    all_ez, all_eM = [], []
    for trial in trials:
        res = run_trial(trial, all_sensor_positions, rng)
        all_ez.append(res["ez_mean"])
        all_eM.append(res["eM_mean"])
        print(f"{res['trial']:>5} {res['z_obs']:>7.1f} {res['M_obs']:>8.1f} "
              f"{res['z_cal']:>7.1f} {res['M_cal']:>8.1f} "
              f"{res['ez_mean']:>8.2f}+-{res['ez_std']:<8.2f} "
              f"{res['eM_mean']:>8.2f}+-{res['eM_std']:<8.2f}")

    print(f"\nAverage across trials: e_z = {np.mean(all_ez):.2f}%, "
          f"e_M = {np.mean(all_eM):.2f}%")
    print("\n(Compare against the manuscript's published Table 1 / statistics "
          "table in data/; see module docstring regarding synthetic vs. "
          "original measurement data.)")


if __name__ == "__main__":
    main()
