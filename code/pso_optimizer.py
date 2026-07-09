"""
pso_optimizer.py
-----------------
Particle Swarm Optimization (PSO) engine implementing the exact parameter
configuration reported in Table "Complete PSO Parameter Configuration for
ITSC Fault Inversion" of the manuscript:

    Population size N          : 50 particles
    Inertia weight w           : 0.9 -> 0.4 (linear decay)
    Acceleration coefficients  : c1 = c2 = 2.0
    Random variables r1, r2    : Uniform(0, 1)
    Maximum iterations T_max   : 200
    Convergence criterion      : |F(t) - F(t-20)| / F(t) < 1e-6
    Velocity clamping V_max    : 0.2 * (range per dimension)
    Independent restarts N_r   : 10
    Final solution selection   : min F_t across all N_r runs
    Search bounds z_h          : [0, 200] mm
    Search bounds M            : [100, 1000] mT

This module is deliberately generic (it optimizes an arbitrary 2D fitness
function subject to box constraints) so it can be reused for other
inversion problems beyond the dipole model in dipole_model.py.
"""

from dataclasses import dataclass, field
from typing import Callable, Tuple
import numpy as np


@dataclass
class PSOConfig:
    n_particles: int = 50
    w_start: float = 0.9
    w_end: float = 0.4
    c1: float = 2.0
    c2: float = 2.0
    max_iter: int = 200
    conv_window: int = 20
    conv_tol: float = 1e-6
    v_max_fraction: float = 0.2
    n_restarts: int = 10
    bounds: Tuple[Tuple[float, float], Tuple[float, float]] = ((0.0, 200.0), (100.0, 1000.0))
    seed: int = None


@dataclass
class PSOResult:
    best_position: np.ndarray
    best_fitness: float
    fitness_history: np.ndarray          # best-so-far fitness at each iteration
    all_restart_bests: np.ndarray = field(default_factory=lambda: np.array([]))
    all_restart_positions: np.ndarray = field(default_factory=lambda: np.array([]))


def _clip_to_bounds(x: np.ndarray, bounds) -> np.ndarray:
    lower = np.array([b[0] for b in bounds])
    upper = np.array([b[1] for b in bounds])
    return np.clip(x, lower, upper)


def _single_run(fitness_fn: Callable[[np.ndarray], float], cfg: PSOConfig,
                 rng: np.random.Generator) -> Tuple[np.ndarray, float, np.ndarray]:
    """One independent PSO run. Returns (best_position, best_fitness, history)."""
    dim = len(cfg.bounds)
    lower = np.array([b[0] for b in cfg.bounds])
    upper = np.array([b[1] for b in cfg.bounds])
    v_max = cfg.v_max_fraction * (upper - lower)

    # Initialize swarm uniformly within bounds.
    positions = rng.uniform(lower, upper, size=(cfg.n_particles, dim))
    velocities = rng.uniform(-v_max, v_max, size=(cfg.n_particles, dim))

    fitness = np.array([fitness_fn(p) for p in positions])
    personal_best_pos = positions.copy()
    personal_best_fit = fitness.copy()

    g_idx = int(np.argmin(personal_best_fit))
    global_best_pos = personal_best_pos[g_idx].copy()
    global_best_fit = personal_best_fit[g_idx]

    history = np.zeros(cfg.max_iter)

    for t in range(cfg.max_iter):
        w = cfg.w_start - (cfg.w_start - cfg.w_end) * (t / max(cfg.max_iter - 1, 1))

        r1 = rng.uniform(0.0, 1.0, size=(cfg.n_particles, dim))
        r2 = rng.uniform(0.0, 1.0, size=(cfg.n_particles, dim))

        velocities = (w * velocities
                      + cfg.c1 * r1 * (personal_best_pos - positions)
                      + cfg.c2 * r2 * (global_best_pos - positions))
        velocities = np.clip(velocities, -v_max, v_max)

        positions = positions + velocities
        positions = _clip_to_bounds(positions, cfg.bounds)

        fitness = np.array([fitness_fn(p) for p in positions])

        improved = fitness < personal_best_fit
        personal_best_pos[improved] = positions[improved]
        personal_best_fit[improved] = fitness[improved]

        g_idx = int(np.argmin(personal_best_fit))
        if personal_best_fit[g_idx] < global_best_fit:
            global_best_fit = personal_best_fit[g_idx]
            global_best_pos = personal_best_pos[g_idx].copy()

        history[t] = global_best_fit

        # Convergence check per manuscript criterion.
        if t >= cfg.conv_window:
            prev = history[t - cfg.conv_window]
            if prev > 0 and abs(history[t] - prev) / history[t] < cfg.conv_tol:
                history = history[: t + 1]
                break

    return global_best_pos, global_best_fit, history


def optimize(fitness_fn: Callable[[np.ndarray], float],
             cfg: PSOConfig = None) -> PSOResult:
    """
    Run PSO with N_r independent restarts (per manuscript methodology) and
    return the best result across all restarts.
    """
    cfg = cfg or PSOConfig()
    rng = np.random.default_rng(cfg.seed)

    restart_bests = []
    restart_positions = []
    best_history = None
    best_fit_overall = np.inf
    best_pos_overall = None

    for r in range(cfg.n_restarts):
        pos, fit, hist = _single_run(fitness_fn, cfg, rng)
        restart_bests.append(fit)
        restart_positions.append(pos)
        if fit < best_fit_overall:
            best_fit_overall = fit
            best_pos_overall = pos
            best_history = hist

    return PSOResult(
        best_position=best_pos_overall,
        best_fitness=best_fit_overall,
        fitness_history=best_history,
        all_restart_bests=np.array(restart_bests),
        all_restart_positions=np.array(restart_positions),
    )
