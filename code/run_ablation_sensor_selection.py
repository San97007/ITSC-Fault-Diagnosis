"""
run_ablation_sensor_selection.py
-----------------------------------
Reproduces the sensor-selection ablation reported in Table
"tab:ablation_sensor" of the manuscript (Section 4.4, Ablation Study).

Compares three sensor configurations, holding K=4 fixed across all six
trials in data/table1_inversion_trials.csv:
  (A) all 12 sensors (no selection),
  (B) the 4 sensors nearest the fault (stand-in for Algorithm 1's
      selection outcome -- see run_sensor_selection_demo.py for the
      full utility-based algorithm),
  (C) 4 randomly chosen sensors.

See the module docstring in run_inversion_demo.py regarding the
synthetic-measurement caveat: replace with real DAQ data before final
deposit if available.
"""
import numpy as np, os
from dipole_model import dipole_field, sensor_positions_mm
from pso_optimizer import PSOConfig, optimize
from run_inversion_demo import load_trials, DATA_DIR

N_SENSORS = 12; SIGMA = 5.0; K = 4
all_pos = sensor_positions_mm(N_SENSORS)
trials = load_trials(os.path.join(DATA_DIR, "table1_inversion_trials.csv"))

def nearest_k(z_h, k):
    d = np.abs(all_pos - z_h); order = np.argsort(d); return np.sort(order[:k])
def simulate(z_obs, M_obs, idx, rng):
    pos = all_pos[idx]; b = dipole_field(z_obs, M_obs, pos) + rng.normal(0, SIGMA, size=pos.shape)
    return pos, b
def pso_invert(pos, b, rng, n_restarts=10):
    w = 1.0/SIGMA**2
    def obj(params):
        zh, M = params
        return np.sum(w*(b - dipole_field(zh, M, pos))**2)
    cfg = PSOConfig(n_restarts=n_restarts, seed=int(rng.integers(0,1_000_000)))
    r = optimize(obj, cfg)
    return r.best_position

configs = ["all12", "selected", "random"]
results = {c: {"ez": [], "eM": []} for c in configs}
per_trial_rows = []

for trial in trials:
    z_obs, M_obs = trial["z_obs"], trial["M_obs"]
    all_idx = np.arange(N_SENSORS)
    sel_idx = nearest_k(z_obs, K)
    rng_r = np.random.default_rng(hash((trial["trial"], "rand")) % (2**32))
    rand_idx = np.sort(rng_r.choice(N_SENSORS, size=K, replace=False))
    idx_map = {"all12": all_idx, "selected": sel_idx, "random": rand_idx}

    row = {"trial": trial["trial"], "z_obs": z_obs, "M_obs": M_obs}
    for cname, idx in idx_map.items():
        ez_list, eM_list = [], []
        for rep in range(3):  # 3 repeats for stability (each already does 10 PSO restarts internally... expensive)
            rng = np.random.default_rng(2000*trial["trial"] + rep + (0 if cname=="all12" else 1000 if cname=="selected" else 2000))
            pos, b = simulate(z_obs, M_obs, idx, rng)
            zh, M = pso_invert(pos, b, rng, n_restarts=5)  # reduce restarts for speed in this sweep
            ez_list.append(abs(zh - z_obs) / 200 * 100)
            eM_list.append(abs(M - M_obs) / M_obs * 100)
        ez_m, eM_m = np.mean(ez_list), np.mean(eM_list)
        results[cname]["ez"].append(ez_m)
        results[cname]["eM"].append(eM_m)
        row[f"ez_{cname}"] = round(ez_m, 2)
        row[f"eM_{cname}"] = round(eM_m, 2)
    per_trial_rows.append(row)

print("Per-trial (K=4 fixed):")
for row in per_trial_rows:
    print(row)

print("\nAverages:")
for c in configs:
    print(c, "e_z=", round(np.mean(results[c]["ez"]),2), "e_M=", round(np.mean(results[c]["eM"]),2))
