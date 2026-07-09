"""
run_noise_robustness.py
-------------------------
Reproduces the methodology behind the manuscript's noise-robustness table
(SNR = 30 dB, 20 dB, 10 dB vs. noise-free baseline).

SNR is defined per the manuscript as:
    SNR_dB = 20 * log10(B_bar / sigma_n)
where B_bar = 544 mT is the average dipole moment across the six test
cases (see data/table1_inversion_trials.csv) and sigma_n is the injected
noise standard deviation.

For each SNR level, Gaussian white noise with the corresponding sigma_n is
added to the simulated sensor readings for all six test cases, PSO
inversion is repeated with N_r = 10 independent restarts, and the average
e_z / e_M errors across all six trials are reported.
"""

import os
import numpy as np

from dipole_model import dipole_field, sensor_positions_mm
from pso_optimizer import PSOConfig, optimize
from run_inversion_demo import load_trials, active_sensors_for_fault, DATA_DIR, N_SENSORS

B_BAR_MT = 544.0  # average M_obs across the six trials, per manuscript


def sigma_n_for_snr(snr_db):
    return B_BAR_MT / (10 ** (snr_db / 20.0))


def invert_once(z_obs, M_obs, sensor_pos, sigma_n, rng):
    b_true = dipole_field(z_obs, M_obs, sensor_pos)
    b_meas = b_true + rng.normal(0.0, sigma_n, size=b_true.shape)

    w = 1.0 / sigma_n ** 2 if sigma_n > 0 else 1.0

    def objective(params):
        z_h, M = params
        b_model = dipole_field(z_h, M, sensor_pos)
        return np.sum(w * (b_meas - b_model) ** 2)

    cfg = PSOConfig(n_restarts=1, seed=int(rng.integers(0, 1_000_000)))
    result = optimize(objective, cfg)
    z_cal, M_cal = result.best_position
    ez = abs(z_cal - z_obs) / 200.0 * 100.0
    eM = abs(M_cal - M_obs) / M_obs * 100.0
    return ez, eM


def main():
    trials = load_trials(os.path.join(DATA_DIR, "table1_inversion_trials.csv"))
    all_sensor_positions = sensor_positions_mm(N_SENSORS)
    rng = np.random.default_rng(7)

    snr_levels = [None, 30, 20, 10]  # None = no-noise baseline (sensor spec sigma=5 mT)

    print(f"{'SNR':>10} {'sigma_n(mT)':>12} {'e_z mean(%)':>12} {'e_M mean(%)':>12}")
    for snr in snr_levels:
        sigma_n = 5.0 if snr is None else sigma_n_for_snr(snr)
        ez_all, eM_all = [], []
        for trial in trials:
            sensor_pos = active_sensors_for_fault(trial["z_obs"], all_sensor_positions)
            for _ in range(10):  # N_r independent restarts
                ez, eM = invert_once(trial["z_obs"], trial["M_obs"], sensor_pos, sigma_n, rng)
                ez_all.append(ez)
                eM_all.append(eM)
        label = "no noise" if snr is None else f"{snr} dB"
        print(f"{label:>10} {sigma_n:>12.1f} {np.mean(ez_all):>12.2f} {np.mean(eM_all):>12.2f}")


if __name__ == "__main__":
    main()
