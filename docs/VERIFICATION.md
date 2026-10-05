# Verification record

Date: 2026-10-05. **PASS for data-only reproduction. Private review candidate.**

## Tests performed

- Linux/Python 3.11.7 with the locked dependencies: complete generation and
  all nine regression tests passed.
- A second independent Linux desktop, Python 3.12.3: downloaded the ZIP
  through a private loopback-only SSH connection, verified its checksum,
  extracted into a fresh directory and ran `bash reproduce.sh` with an empty
  HOME and cleared environment. Dependencies were freshly installed. The
  original numerical project, private solver and credentials were not transferred.
- All nine tests, `pip check`, and `--verify-only` passed on that clean copy.
- All **49 generated figure, coordinate and table files** were byte-identical
  between the tested Python 3.11.7 and Python 3.12.3 runs.
- All 27 input/reference manifest entries passed their SHA-256 checks.
- All 282 displayed cells across eight tables match the manuscript fixture,
  including the two documented presentation records, endpoint daggers,
  upper-bound marker and unavailable high-mass entry.
- All 174 comparisons of ported display-processing arrays with the archived
  plotting routines were identical. This checks the port, not a new solver.
- All eleven generated PDFs were rendered and visually inspected. The eight
  LaTeX row files compiled together successfully using standard AMS symbols.
- A final check of the original canonical freeze again matched 255/255
  entries. No original scientific file or manuscript was modified.

## Tested execution content

Execution-content SHA-256:
`cb83b30b8ed82f30f96b5c98ae6f8851c9d027a587926ac006e4d5560db9f10a`.

This hashes the sorted relative-file SHA-256 map for code, inputs, references,
tests, workflow, installer, Makefile and dependency lock. README,
citation/rights metadata and documentation are excluded from this aggregate,
so this completed verification record can be appended without changing the
tested executable/data content. The final ZIP checksum is supplied separately.

Cross-machine byte identity is for the generated outputs under the pinned
environments. It is not a claim of byte-identical rendering to the original
paper images; minor font/layout differences are documented in provenance.

## Scope and privacy

The allowlisted candidate was checked for excluded identifiers, private paths,
credential patterns and solver imports. Text, filenames, PNG metadata and HDF5
string attributes were inspected; no such material was found. The numerical
inputs total 813,337 bytes before ZIP compression. The independent desktop
test occupied approximately 417 MB including its environment and cache,
within the declared 1-GB working budget. No cluster jobs or solver runs occurred.

This is saved-data reproduction, not independent recalculation of the EOS,
TOV solutions or QNM spectrum. Solver source, private correspondence,
administrative proofs and research notes remain excluded. No public upload
or additional reuse license is authorized by this verification record.
