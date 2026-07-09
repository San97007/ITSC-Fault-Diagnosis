"""
dipole_model.py
----------------
Analytical forward model for the axial leakage-flux-density produced by an
inter-turn short-circuit (ITSC) fault, modeled as a magnetic dipole located
at axial position z_h with equivalent moment M.

This implements Eq. (dipole) of the manuscript:

    B_i^model(z_h, M) = (mu0 / (4*pi)) * M *
                         (2*(z_i - z_h)^2 - r0^2) /
                         ((z_i - z_h)^2 + r0^2)^(5/2)

Notes on units
--------------
In the manuscript, M is reported directly in the same units as the measured
flux density (mT), rather than as an SI dipole moment (A*m^2). This is a
phenomenological / calibrated forward model used purely as a fast surrogate
for the coupled electromagnetic-circuit finite-element (DT) simulation, so
that the PSO inversion (Section "ITSC Diagnosis Based on Particle Swarm
Optimization") can evaluate the fitness function in real time.

To keep the model self-consistent and dimensionally transparent, we expose
an explicit calibration constant `C` (units: mT * mm^3) instead of silently
mixing SI and mm/mT units:

    B_i^model(z_h, M) = C * M *
                         (2*(z_i - z_h)^2 - r0^2) /
                         ((z_i - z_h)^2 + r0^2)^(5/2)

`C` plays the role of mu0/(4*pi) in the manuscript's formula, but expressed
in the mixed (mm, mT) unit system actually used for the reported values. It
should be calibrated once against the authors' original DT (COMSOL) or
experimental data and then held fixed for all inversions.

Default calibration (principled placeholder)
---------------------------------------------
In the manuscript, M is reported directly in mT (e.g. Table 1: M_obs in
the range ~470-590 mT) rather than as an SI dipole moment, so the natural
reading is that M represents approximately the peak fault-induced flux
density *at the sensor closest to the fault* (dz = z_i - z_h -> 0). Setting

    C = r0^3

makes this exact: at dz = 0, the geometric factor reduces to -1/r0^3, so
B_model(z_h, M) = C * M * (-1/r0^3) = -M at the nearest sensor. This gives
a dimensionally clean, data-independent default. **If the authors' original
COMSOL/experimental calibration differs, replace `DEFAULT_CALIBRATION_CONSTANT`
accordingly before final deposit** -- see `calibrate_constant()` below for a
least-squares alternative if a reference (z_h, M, sensor readings) triple is
available.
"""

import numpy as np

# Radial distance from the winding axis to the sensor array midplane (mm),
# as specified in the manuscript.
DEFAULT_R0_MM = 7.5

# Principled default: C = r0^3, so that M is (approximately) the peak
# flux density in mT at the sensor nearest the fault. See module docstring.
DEFAULT_CALIBRATION_CONSTANT = DEFAULT_R0_MM ** 3


def sensor_positions_mm(n_sensors: int = 12, winding_height_mm: float = 200.0,
                         spacing_mm: float = 16.7) -> np.ndarray:
    """
    Return the axial positions (mm) of the 12 S49E Hall sensors, uniformly
    spaced at 16.7 mm and centered on the winding height, as described in
    the Experimental Platform section of the manuscript.
    """
    offset = (winding_height_mm - (n_sensors - 1) * spacing_mm) / 2.0
    return offset + np.arange(n_sensors) * spacing_mm


def dipole_field(z_h: float, M: float, z_sensors: np.ndarray,
                  r0: float = DEFAULT_R0_MM,
                  C: float = DEFAULT_CALIBRATION_CONSTANT) -> np.ndarray:
    """
    Predicted axial leakage flux density (mT) at each sensor position, per
    Eq. (dipole) of the manuscript.

    Parameters
    ----------
    z_h : float
        Fault axial location (mm), search bound [0, 200].
    M : float
        Equivalent fault dipole moment / severity parameter (mT-scale),
        search bound [100, 1000].
    z_sensors : np.ndarray
        Axial positions (mm) of the active sensors.
    r0 : float
        Radial distance from winding axis to sensor array (mm).
    C : float
        Calibration constant playing the role of mu0/(4*pi) (see module
        docstring).

    Returns
    -------
    np.ndarray
        Modeled flux density (mT) at each sensor position.
    """
    dz = z_sensors - z_h
    numerator = 2.0 * dz ** 2 - r0 ** 2
    denominator = (dz ** 2 + r0 ** 2) ** 2.5
    return C * M * numerator / denominator


def calibrate_constant(z_h_ref: float, M_ref: float, z_sensors_ref: np.ndarray,
                        B_measured_ref: np.ndarray, r0: float = DEFAULT_R0_MM) -> float:
    """
    Optional least-squares calibration of C against a single reference
    fault case with known (z_h, M) and measured sensor readings, e.g. the
    experimentally validated case in Table 3 (z = 130 mm, M = 564.7 mT)
    combined with the per-sensor readings in
    data/table_persensor_domaingap.csv. Use this instead of the default
    C = r0^3 if the authors want the forward model calibrated directly
    against their own measurements.
    """
    dz = z_sensors_ref - z_h_ref
    numerator = 2.0 * dz ** 2 - r0 ** 2
    denominator = (dz ** 2 + r0 ** 2) ** 2.5
    basis = M_ref * numerator / denominator
    # Least-squares solve for scalar C: minimize ||C * basis - B_measured_ref||^2
    C = float(np.dot(basis, B_measured_ref) / np.dot(basis, basis))
    return C
