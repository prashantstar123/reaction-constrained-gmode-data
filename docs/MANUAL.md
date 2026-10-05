# Reproduction manual

## Requirements and installation

Use Linux with Python 3.11 or 3.12 and its `venv` support. Leave 1 GB free
for dependencies, caches and generated figures. Numerical inputs themselves
are below 1 MB, excluding the reference images. The package requires NumPy,
SciPy, h5py and Matplotlib; all direct and plotting dependencies are pinned
in `requirements.lock`. No compiler or stellar code is needed.

Extract the ZIP into a new folder, rather than overlaying another project.
From the extracted directory run:

```bash
bash reproduce.sh
```

To choose a particular Python executable:

```bash
PYTHON=python3.12 bash reproduce.sh
```

The first run downloads dependencies. Subsequent offline runs can use
`.venv/bin/python -m reproduction`. A complete run creates an output-hash
record. `.venv/bin/python -m reproduction --verify-only` checks the inputs,
table values and existing output hashes without regenerating the figures.

Use a separate output directory to preserve an earlier result:

```bash
.venv/bin/python -m reproduction --output output_comparison
```

Inputs are opened read-only. Only the chosen output folder, environment and
plotting cache are written. A failed check produces a nonzero exit status;
partial files from a failed run are not a verified result.

## Figure map

| Paper figure | Output stem(s) |
| --- | --- |
| 1 | `FIG1_kaon_buoyancy_fractions` |
| 2 | `FIG2_kaon_MR` |
| 3 | `FIG3a_kaon_freq`, `FIG3b_kaon_damping` |
| 4 | `FIG4_hypdelta_buoyancy_fractions` |
| 5 | `FIG5_hypdelta_MR` |
| 6 | `g1_paperstyle_can`, `tau_paperstyle_can` |
| 7 | `FIG7_strongD` |
| 8 | `FIG8_tidal_dphi` |
| 9 | `ddme2_appendix_robustness` |

Each stem produces a PNG, PDF and `.curves.json` coordinate record. Coordinate
records contain the actual plotted line arrays and panel indices; `null`
marks a break. Filled observational regions are provided separately in HDF5.
PDFs are vector graphics; PNGs use the archived figure dimensions and DPI.
Rendering-library differences can alter pixels/fonts without changing data.

## Table map

| Proof-corrected number | Output suffix | Content |
| --- | --- | --- |
| I | `model_parameters` | Adopted BigApple parameters and saturation targets |
| II | `exotic_couplings` | Adopted antikaon, hyperon and Delta prescriptions |
| III | `kaon_summary` | Structure, frequencies and damping for the kaon family |
| IV | `kaon_channels` | Species-resolved kaon sensitivities |
| V | `baryonic_summary` | Nucleonic, hyperon and Delta structural/mode summary |
| VI | `baryonic_channels` | Hyperon/Delta sensitivities |
| VII | `tidal_response` | Reported resonance frequencies and phase estimates |
| VIII | `eos_comparison` | BigApple versus DD-ME2 reaction-limit comparison |

Files are named `table<number>_<suffix>.json` and `.tex`. JSON gives semantic
labels, column names/units and displayed cell strings. Underlying unrounded
values are in the input JSON/HDF5 files. LaTeX files contain rows to insert
into an appropriate `tabular` or `longtable`; they do not reproduce journal
pagination. No TeX installation is needed unless you choose to compile them.
When compiling, load `amsmath` and `amssymb` for the mathematical symbols,
including the upper-bound marker in Table VII.

Retain the following qualifications when reusing a table:

- A dagger marks an EOS-validity endpoint, not a physical maximum mass.
- Frozen and reaction-limit frequencies use paired backgrounds.
- The nucleonic 2.0-solar-mass tidal entry is an upper-bound-style estimate;
  its less-than-or-approximately-equal symbol is retained.
- There is no 2.0-solar-mass NYDelta tidal entry: the sequence terminates earlier.
- Channel masses are the stored sample masses, not relabelled nearest integers.

## Direct data access

```python
import h5py
with h5py.File("data/bigapple.h5", "r") as f:
    modes = f["g1/ka_UK120"][:]
    mass = modes[:, 1]
    full_gr_frequency_hz = modes[:, 4]
```

Dataset attributes give column names and source hashes. See the data
dictionary before using raw damping rows or tidal records. Display curves
are not replacements for exact-star numerical tables or convergence records.

## Troubleshooting

- Missing `venv`/`ensurepip`: install the matching Python venv support using
  your operating system's package manager.
- Download failure: check internet access/package-index availability. No
  repository credentials are required to install dependencies.
- Input mismatch: re-extract the verified archive; do not edit a manifest to
  conceal a changed data file.
- Missing output: run the full command; `--verify-only` does not create figures.
- Different visual encoding: numerical/table checks must still pass. Consult
  `verification.json` for Python and package versions.

For an issue report, provide the command, Python version and error message.
Do not share private source directories, credentials, or administrative records.
