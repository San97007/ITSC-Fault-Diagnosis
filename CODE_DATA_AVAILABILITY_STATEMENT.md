# Draft text for the manuscript

Replace the current "Data Availability" statement and add a new "Code
Availability" section with the text below. **Fill in the DOI placeholder
`10.5281/zenodo.XXXXXXX` after you publish the Zenodo record** — Zenodo
assigns the DOI automatically the first time you publish, and you can
optionally reserve it in advance (Zenodo shows a "Reserve DOI" button
before publishing, so you can paste it into the manuscript before
uploading the final version).

---

## Data Availability (replace existing section)

> The datasets generated and analyzed during the current study, including
> the transformer prototype parameters, finite-element mesh configuration,
> six-trial PSO inversion validation results, per-sensor domain-gap
> measurements, noise-robustness evaluation, and physical-virtual fusion
> comparison data, are available in the Zenodo repository,
> https://doi.org/10.5281/zenodo.XXXXXXX. Raw Hall-sensor data-acquisition
> exports underlying the summary tables are available from the
> corresponding author upon reasonable request.

*(Adjust the last sentence once raw DAQ files are added to the
repository — at that point they will also be "available in the Zenodo
repository" rather than "upon request.")*

## Code Availability (new section)

> The Python implementation of the composite utility-based sensor
> selection algorithm and the PSO-based ITSC fault inversion algorithm
> (including the exact hyperparameter configuration used in this study)
> is openly available in the Zenodo repository,
> https://doi.org/10.5281/zenodo.XXXXXXX, under the MIT license. A
> description of the COMSOL Multiphysics digital-twin finite-element
> model build (geometry, material model, mesh, and solver configuration)
> is provided in the same repository.

---

## Suggested placement

In the `wlscirep` (Scientific Reports) template used by this manuscript,
these appear as unnumbered sections near the end, alongside `Funding`,
`Author contributions`, and `Declarations`. Suggested order:

```latex
\section*{Data Availability}
... (text above) ...

\section*{Code Availability}
... (text above) ...

\section*{Funding}
...
```

## One-line addition to the main text (optional but recommended)

In Section "ITSC Diagnosis Based on Particle Swarm Optimization", after
the PSO parameter table, consider adding:

> A reference implementation of the sensor-selection and PSO inversion
> algorithms, together with the parameter configuration in
> Table~\ref{tab:pso}, is available at
> https://doi.org/10.5281/zenodo.XXXXXXX.

This pre-empts a repeat reviewer request by pointing to the code directly
at the point where the algorithm is described, rather than only in the
end-of-manuscript availability statements.
