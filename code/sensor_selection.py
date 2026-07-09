"""
sensor_selection.py
--------------------
Implementation of Algorithm 1 ("Composite Utility-Based Sensor Selection")
from the manuscript, Section "Multi-sensor Information Fusion of
Micromagnetic Field".

Given, for each of N sensors, three raw criterion values:
    P_i  : Pearson correlation coefficient between the leakage magnetic
           field at the sensor location and the fault point (Eq. P).
    V_i  : fluctuation-variance-based reliability index (Eq. V_i = sigma_i^2 / mu_i).
    DS_i : Dempster-Shafer symmetry index (Eq. DS_i = rho_i * D_i).

the algorithm:
  1. min-max normalizes each criterion to [0, 1] (inverting V_i so that
     lower variance -> higher score), Eq. (norm);
  2. computes a composite utility score U_i = alpha*P~_i + beta*V~_i +
     gamma*DS~_i, Eq. (utility), with alpha=0.5, beta=0.3, gamma=0.2;
  3. selects the smallest top-K set of sensors whose cumulative utility
     reaches at least 85% of the total utility, Eq. (selection).
"""

from dataclasses import dataclass
from typing import Sequence, Tuple
import numpy as np


ALPHA_DEFAULT = 0.5
BETA_DEFAULT = 0.3
GAMMA_DEFAULT = 0.2
UTILITY_COVERAGE_THRESHOLD = 0.85


@dataclass
class SensorSelectionResult:
    utility_scores: np.ndarray       # U_i for all N sensors, in original order
    ranking: np.ndarray               # sensor indices sorted by descending utility
    selected_indices: np.ndarray      # indices of the K selected sensors (unordered)
    K: int


def _minmax_normalize(x: np.ndarray, invert: bool = False) -> np.ndarray:
    """Min-max normalize to [0, 1]; if invert=True, low values score high."""
    x = np.asarray(x, dtype=float)
    lo, hi = x.min(), x.max()
    if np.isclose(hi, lo):
        # Degenerate case: all sensors equally informative on this criterion.
        return np.ones_like(x) if not invert else np.ones_like(x)
    normed = (x - lo) / (hi - lo)
    return (1.0 - normed) if invert else normed


def composite_utility(P: Sequence[float], V: Sequence[float], DS: Sequence[float],
                       alpha: float = ALPHA_DEFAULT, beta: float = BETA_DEFAULT,
                       gamma: float = GAMMA_DEFAULT) -> np.ndarray:
    """Compute the composite utility score U_i for every sensor (Eq. utility)."""
    P = np.asarray(P, dtype=float)
    V = np.asarray(V, dtype=float)
    DS = np.asarray(DS, dtype=float)

    P_tilde = _minmax_normalize(P, invert=False)
    V_tilde = _minmax_normalize(V, invert=True)   # lower variance -> higher score
    DS_tilde = _minmax_normalize(DS, invert=False)

    return alpha * P_tilde + beta * V_tilde + gamma * DS_tilde


def select_sensors(U: np.ndarray, coverage: float = UTILITY_COVERAGE_THRESHOLD
                    ) -> Tuple[np.ndarray, int]:
    """
    Select the smallest set of top-ranked sensors whose cumulative utility
    reaches at least `coverage` (default 0.85) of the total, Eq. (selection).

    Returns (selected_indices, K).
    """
    order = np.argsort(U)[::-1]          # descending order of utility
    sorted_U = U[order]
    cumulative = np.cumsum(sorted_U) / np.sum(U)

    K = int(np.searchsorted(cumulative, coverage) + 1)
    K = max(1, min(K, len(U)))

    selected = np.sort(order[:K])
    return selected, K


def run_selection(P: Sequence[float], V: Sequence[float], DS: Sequence[float],
                   alpha: float = ALPHA_DEFAULT, beta: float = BETA_DEFAULT,
                   gamma: float = GAMMA_DEFAULT,
                   coverage: float = UTILITY_COVERAGE_THRESHOLD
                   ) -> SensorSelectionResult:
    """Convenience wrapper running the full Algorithm 1 pipeline."""
    U = composite_utility(P, V, DS, alpha, beta, gamma)
    order = np.argsort(U)[::-1]
    selected, K = select_sensors(U, coverage)
    return SensorSelectionResult(utility_scores=U, ranking=order,
                                  selected_indices=selected, K=K)
