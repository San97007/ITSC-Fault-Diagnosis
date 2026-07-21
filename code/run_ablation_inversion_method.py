"""
run_ablation_inversion_method.py
-----------------------------------
Reproduces the inversion-method ablation reported in Table
"tab:ablation_pso" of the manuscript (Section 4.4, Ablation Study).

Compares three inversion methods on the same (Algorithm-selected)
sensor subset and noise realization per trial:
  (A) PSO with the full N_r=10 restarts (Table tab:pso configuration),
  (B) exhaustive grid search (0.5 mm resolution in z_h, closed-form
      weighted least-squares for M since the forward model is linear
      in M),
  (C) naive peak-detection baseline (no optimization).

See the module docstring in run_inversion_demo.py regarding the
synthetic-measurement caveat: replace with real DAQ data before final
deposit if available.
"""
import time, numpy as np, os
from dipole_model import dipole_field, sensor_positions_mm
from pso_optimizer import PSOConfig, optimize
from run_inversion_demo import load_trials, DATA_DIR

N_SENSORS = 12
SIGMA = 5.0
all_pos = sensor_positions_mm(N_SENSORS)
trials = load_trials(os.path.join(DATA_DIR, "table1_inversion_trials.csv"))

def nearest_k(z_h, k):
    d = np.abs(all_pos - z_h); order = np.argsort(d); return np.sort(order[:k])
def k_for(z_h):
    return 4 if 40 < z_h < 160 else 6 if (z_h < 30 or z_h > 170) else 5
def simulate(z_obs, M_obs, idx, rng):
    pos = all_pos[idx]; b = dipole_field(z_obs, M_obs, pos) + rng.normal(0, SIGMA, size=pos.shape)
    return pos, b
def pso_invert_multirestart(pos, b, rng):
    w = 1.0/SIGMA**2
    def obj(params):
        zh, M = params
        return np.sum(w*(b - dipole_field(zh, M, pos))**2)
    cfg = PSOConfig(n_restarts=10, seed=int(rng.integers(0,1_000_000)))  # matches manuscript N_r=10
    r = optimize(obj, cfg)
    return r.best_position
def grid_invert(pos, b, resolution=0.5):
    w = 1.0/SIGMA**2
    zs = np.arange(0, 200+resolution, resolution)
    best_fit = np.inf; best_zh=None; best_M=None
    for zh in zs:
        basis = dipole_field(zh, 1.0, pos)
        M_opt = np.clip(np.sum(w*basis*b)/np.sum(w*basis*basis), 100, 1000)
        resid = np.sum(w*(b - M_opt*basis)**2)
        if resid < best_fit:
            best_fit = resid; best_zh = zh; best_M = M_opt
    return np.array([best_zh, best_M])
def peak_invert(pos, b):
    i = np.argmax(np.abs(b)); return np.array([pos[i], abs(b[i])])

methods = ["pso", "grid", "peak"]
results2 = {m: {"ez":[], "eM":[], "t":[]} for m in methods}
per_trial = {m: {"ez":[], "eM":[]} for m in methods}

for trial in trials:
    z_obs, M_obs = trial["z_obs"], trial["M_obs"]
    idx = nearest_k(z_obs, k_for(z_obs))
    rng = np.random.default_rng(500+trial["trial"])
    pos, b = simulate(z_obs, M_obs, idx, rng)

    t0=time.time(); zh,M = pso_invert_multirestart(pos, b, rng); t1=time.time()
    ez=abs(zh-z_obs)/200*100; eM=abs(M-M_obs)/M_obs*100
    results2["pso"]["ez"].append(ez); results2["pso"]["eM"].append(eM); results2["pso"]["t"].append(t1-t0)
    per_trial["pso"]["ez"].append(ez); per_trial["pso"]["eM"].append(eM)

    t0=time.time(); zh,M = grid_invert(pos, b); t1=time.time()
    ez=abs(zh-z_obs)/200*100; eM=abs(M-M_obs)/M_obs*100
    results2["grid"]["ez"].append(ez); results2["grid"]["eM"].append(eM); results2["grid"]["t"].append(t1-t0)
    per_trial["grid"]["ez"].append(ez); per_trial["grid"]["eM"].append(eM)

    t0=time.time(); zh,M = peak_invert(pos, b); t1=time.time()
    ez=abs(zh-z_obs)/200*100; eM=abs(M-M_obs)/M_obs*100
    results2["peak"]["ez"].append(ez); results2["peak"]["eM"].append(eM); results2["peak"]["t"].append(t1-t0)
    per_trial["peak"]["ez"].append(ez); per_trial["peak"]["eM"].append(eM)

print("=== Ablation 2 (fair, PSO with 10 restarts) ===")
for m in methods:
    ez=np.mean(results2[m]["ez"]); eM=np.mean(results2[m]["eM"]); t=np.mean(results2[m]["t"])
    print(f"{m:>6}: e_z={ez:.2f}%  e_M={eM:.2f}%  time={t*1000:.1f}ms")

print("\nPer trial:")
for i,trial in enumerate(trials):
    print(trial["trial"], trial["z_obs"], trial["M_obs"],
          "PSO", round(per_trial["pso"]["ez"][i],2), round(per_trial["pso"]["eM"][i],2),
          "Grid", round(per_trial["grid"]["ez"][i],2), round(per_trial["grid"]["eM"][i],2),
          "Peak", round(per_trial["peak"]["ez"][i],2), round(per_trial["peak"]["eM"][i],2))
