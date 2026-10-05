# Data dictionary

HDF5 arrays are float64, stored with lossless gzip compression and shuffle.
They are copied from saved reduced numerical records, not regenerated
simulations. Dataset attributes specify columns and original source hashes.
No precision truncation was applied.

## Model tags

`npemu` denotes nucleonic matter with electrons and muons; `ny`, `ndelta`,
and `nydelta` include hyperons, Delta baryons, and both, respectively.
`ka_UK100`, `ka_UK120`, `ka_UK140`, and `ka_UK160` denote the antikaon
potential depths -100, -120, -140 and -160 MeV. `ka_UK0` is the no-condensate
reference. Suffix `_Keq` denotes the fast-kaon limit; `_strongD` denotes
the strong-Delta equilibrium limit. These are the paper's reaction limits,
not different newly computed equilibrium sequences.

## `bigapple.h5`

- `eos/<tag>`: baryon density in fm^-3, energy density and pressure in
  MeV fm^-3, frozen sound speed squared, equilibrium sound speed squared.
  Sound speeds are in units of c^2.
- `reaction/<tag>`: the corresponding reaction-constrained sound-speed
  table, with the same background density/energy/pressure columns.
- `mr/<tag>`: mass in solar masses, radius in km, central energy density
  in MeV fm^-3, central baryon density in fm^-3. Physical-maximum sequences
  include the turnover; plotting selects the rising branch.
- `g1/<tag>`: central energy density, mass, radius, Cowling frequency in Hz,
  full-GR frequency in Hz. `cowling_same_record` records which archived
  source supplies the illustrative Cowling comparison.
- `cowling/<tag>`: separately saved mass/frequency comparison arrays.
- `tau/<tag>`: mass, radiative amplitude-damping time in years,
  Im(omega)/Re(omega), finer-grid damping time in years, relative grid
  difference, central energy density, and real-frequency seed in Hz.
  These are pre-display-selection records; unresolved/small-width tips are
  retained in the data rather than silently erased.
- `composition/ka_UK120`: baryon density and the n, p, e, mu and K fractions.
- `composition/nydelta`: density and the species columns named in its attribute.
- `chi/<tag>`: stored sample mass, frequency, summed/reconstructed sensitivity,
  and the individual channels named in the dataset attribute.

## `ddme2.h5`

`eos/<tag>` and `g1/<tag>` use the same column/units conventions. Tags are
`npemu`, `kaon`, `kaon_fastK`, `ny`, `ndelta`, `ndelta_strongD`, `nydelta`
and `nydelta_strongD`. The appendix compares mechanisms across EOSs; this
file does not contain new DD-ME2 damping or tidal calculations.

## Small JSON numerical/definition records

- `parameters.json`: frozen couplings, masses and convention metadata.
- `adopted_parameters.json`: the article's adopted nucleon/kaon masses and
  quoted saturation targets. These are model inputs, not a rerun saturation test.
- `structure.json`: saved structural summary, onsets and terminal classifications.
- `exact_points.json`: full-precision exact-star mode records and target
  metadata. Frequencies are in Hz and damping times in years. Tables use
  the structural catalogue for radii, not a substitute radius from a mode record.
- `reaction_summary.json`: saved reaction-retention summaries and original
  numerical checks. Archived pass flags are not a new verification campaign.
- `ddme2_comparison.json`: only the DD-ME2 rows from the saved comparison;
  BigApple comparison values are taken from the canonical exact-star data.
- `tidal_resolved.json`: all 17 resolved phase/overlap records, with model,
  mass, dimensionless overlap, phase in radians, convergence and method flags.
- `published_tidal_points.json`: the 14 displayed/Table VII points from the
  frozen figure-validation record. Frequencies are recorded at 0.1-Hz
  resolution and are distinct from independent smooth-curve interpolation.
- `published_display.json`: two documented last-digit table-display records;
  their full-precision checkpoint values remain unchanged elsewhere.

## `observational_display.h5`

Five two-column mass-radius display contour arrays, with radius in km and
mass in solar masses. They are the polygons used by the archived plotting
recipe, not posterior samples or likelihood functions. Source attribution
is retained in the reference bibliography. Their inclusion does not grant
rights over the original observational products.

## Reference files

`reference/table_cells.json` is the independent manuscript comparison fixture;
table generators never read it as a source of numerical output values.
`reference/numerical_sources.json` records the source names/hashes for the
HDF5 arrays. `reference/input_manifest.json` protects the packaged inputs.
The original reference images are comparison-only and are not read by renderers.
