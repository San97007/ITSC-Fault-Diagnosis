"""
run_sensor_selection_demo.py
------------------------------
Demonstrates Algorithm 1 (composite utility-based sensor selection, see
sensor_selection.py) on the three representative fault locations reported
in data/table_sensor_selection_examples.csv (near bottom, mid-winding,
near top).

Note on input data
-------------------
The manuscript reports the *outcome* of the sensor-selection algorithm
(which sensors were selected) but does not publish the underlying raw
per-sensor P_i / V_i / DS_i criterion values that produced those outcomes.
This script therefore constructs physically motivated *synthetic*
criterion profiles -- Pearson correlation peaking near the fault location
and decaying with distance, low but spatially-varying measurement
variance, and a DS symmetry index following the same spatial pattern --
purely to illustrate and sanity-check the algorithm implementation.

Before final Zenodo deposit, the authors should replace
`synthetic_criteria()` below with their original per-sensor P_i, V_i, DS_i
values (e.g. exported from the same DAQ sessions used to build
data/table_persensor_domaingap.csv) so that the selection results are
fully reproducible from the original experimental data rather than from
an illustrative proxy.
"""

import numpy as np
from dipole_model import sensor_positions_mm
from sensor_selection import run_selection

N_SENSORS = 12


def synthetic_criteria(z_h, sensor_positions, rng):
    """Illustrative-only P_i, V_i, DS_i profiles peaked near the fault.

    Widths are chosen so that, after normalization, utility scores are
    sharply concentrated near the fault -- consistent with the manuscript
    reporting that only K = 4-6 (of N = 12) sensors capture 85% of the
    total diagnostic utility. Real experimental criterion data will have
    its own (unknown) sharpness and should replace this placeholder.
    """
    dz = np.abs(sensor_positions - z_h)
    P = np.exp(-(dz / 18.0) ** 2) + rng.normal(0, 0.01, size=dz.shape)
    V = 0.05 + 0.03 * (dz / dz.max()) + rng.normal(0, 0.003, size=dz.shape).clip(min=0)
    DS = np.exp(-(dz / 22.0) ** 2) + rng.normal(0, 0.01, size=dz.shape)
    return P, V, DS


def main():
    sensor_positions = sensor_positions_mm(N_SENSORS)
    sensor_labels = [f"S{i+1}" for i in range(N_SENSORS)]
    rng = np.random.default_rng(123)

    cases = {"near_bottom": 25, "mid_winding": 98, "near_top": 176}

    for name, z_h in cases.items():
        P, V, DS = synthetic_criteria(z_h, sensor_positions, rng)
        result = run_selection(P, V, DS)
        selected_labels = [sensor_labels[i] for i in result.selected_indices]
        print(f"{name:>12} (z_h = {z_h:>3} mm): K = {result.K}, "
              f"selected sensors = {selected_labels}")


if __name__ == "__main__":
    main()
