# Digital Twin Finite-Element Model: Build Description

This document describes how to reconstruct the COMSOL Multiphysics digital
twin model used in the manuscript, since the native `.mph` model file is
not included in this deposit (see note at the end).

## Software

- COMSOL Multiphysics, with the **AC/DC Module** (Magnetic Fields
  interface) and **Electrical Circuit** interface, coupled.

## Physics setup

1. **Magnetic Fields (mf) interface**: 3D, frequency-domain (or
   time-dependent, matching the experimental excitation), applied to the
   transformer core, HV winding, LV winding, inter-winding gap, and
   surrounding air domain.
2. **Electrical Circuit (cir) interface**: implements the local equivalent
   circuit of the winding under ITSC (primary winding resistance `R1`,
   load + secondary winding impedance `Z_L`, short-circuit turn resistance
   `R_d`), coupled to the Magnetic Fields interface through the source
   current density `J_s`.
3. **Coupling**: Kirchhoff's voltage law is applied simultaneously to the
   primary winding loop and the faulted secondary turns; `R_d` is the
   shared circuit parameter linking the field and circuit domains.

## Geometry (see `data/table2_transformer_parameters.csv`)

- Single-phase shell/core-type transformer, HV winding turns = 122, LV
  winding turns = 20.
- HV winding outer/inner diameter: 170 mm / 150 mm; height 200 mm.
- LV winding outer/inner diameter: 145 mm / 125 mm; height 200 mm.
- Inter-winding gap: 5 mm (houses the 12-sensor Hall array).
- Insulation layer thickness: 3 mm.
- Core cross-section: 45 x 80 mm^2; core window height 220 mm; core limb
  length 340 mm; stacking factor 0.96.
- ITSC faults introduced at various axial locations within the pie-type
  LV winding.

## Material model

- Core: grade 50W470 silicon steel, nonlinear B-H curve implemented via
  piecewise cubic spline interpolation over the 9-point dataset in
  `data/table_bh_curve_50W470.csv` (derived from IEC 60404-2). Healthy
  operating point: peak flux ~1.42 T, mu_r ~ 800. Under ITSC, adjacent
  core region saturates above 1.7 T, mu_r drops below 300.
- Windings: copper, standard electrical conductivity; explicit
  turn-by-turn or homogenized (multi-turn coil) modeling as appropriate
  for the mesh density used.

## Mesh (see `data/table_mesh_parameters.csv`)

- Inter-winding gap (sensor region): 0.5-2 mm elements (finest, since this
  is the primary input region for the PSO inversion).
- Winding conductors: 1-3 mm elements.
- Iron core: 2-8 mm elements.
- Surrounding air: 5-20 mm elements.
- Total: ~420,000 degrees of freedom.

## Solver

- Stationary (or time-dependent, if replicating transient fault onset)
  solver with the default COMSOL MUMPS or PARDISO direct solver;
  nonlinear material (B-H curve) requires the default Newton iteration
  with automatic damping.

## Digital twin update / calibration loop

- Fidelity metric: cosine similarity `E(P,V)` between simulated and
  measured current-magnetic-field response vectors (Eq. in
  "Virtual-Real Dynamic Update of the Digital Twin" section).
- Update cadence and triggers: see `data/table_dt_update_cycle.csv`.
  Operating conditions and fidelity are checked every 100 ms; the
  effective core permeability `mu_eff` is re-calibrated on demand whenever
  `E(P,V) < 0.85`; fault state `(z_h, M)` is updated every 5 s following
  each PSO inversion.

## Note on the native model file

The native `.mph` COMSOL model file was not included in this initial
Zenodo deposit (COMSOL model files can be large and require a licensed
COMSOL installation to open/verify). Authors are encouraged to add the
`.mph` file (and/or an exported COMSOL Application or Java/MATLAB
LiveLink build script) to a `comsol/` subdirectory in a future version of
this deposit to maximize reproducibility, since the build description
above -- while complete with respect to reported parameters -- cannot
substitute for the exact solver settings, boundary conditions, and named
selections encoded in the original model tree.
