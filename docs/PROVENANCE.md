# Provenance and presentation conventions

The reference is the accepted DV13734 scientific content and the subsequent
proof-numbering request. The supplied manuscript source has SHA-256
`33bcc86ef6462f86bfe128e5ce9ed618fa4a111c572940ced25aa67d64e18e05`.
All eleven image assets and all eight table bodies match the final APS
submission package. The supplied source removes revision colours and uses
a renamed bibliography file; those changes do not alter scientific values.

The canonical numerical freeze was checked independently at packaging time:
all 255 manifest entries matched. The DD-ME2 appendix and observational
display inputs have separate recorded hashes. That preservation check must
not be described as rerunning or independently revalidating the physics.

## Figures

The release adapts data-only parts of the archived plotting recipes.
EOS construction, TOV integration, perturbation/eigenfunction integration,
QNM searches and arbitrary-precision backends are not included or called.

The frequency display sorts by central energy density, truncates at the
sequence's mass maximum and removes near-duplicate masses at the original
1e-4-solar-mass tolerance. Below the archived divergence/onset criterion,
the exotic family is plotted on its corresponding nucleonic reference.
The original threshold is 12 Hz above a mass of 1 solar mass, with the
subsequent-points condition retained. The Cowling comparison is selected
using the archived 0.72-1.03 frequency-ratio interval; it is an approximation
comparison, not a full-GR data column.

The published damping curves apply, in order, the archived duplicate-mass
selection, the 1e-16 relative imaginary-frequency display floor, onset
splicing, a 1.3-times-baseline onset display cap, upward-spike removal in
log10(tau), and a seven-point/order-two Savitzky-Golay log-display smoothing
where enough points exist. Those operations are **presentation rules**,
not new convergence tests or changes to the stored raw records. All saved
pre-display arrays are retained. Exact-star tables do not use those smoothed
display curves.

The ported processing was compared with the archived routines on the same
saved files: 174 array comparisons were identical. This checks the storage
conversion and processing port; it is not an independent stellar solver.

Figure 8 uses the archived published-point record, including its 0.1-Hz
frequency precision, and the unchanged resolved phase values. These points
must not be replaced by the earlier unreconciled tidal file or by frequencies
interpolated independently from another grid. The full smooth mode sequences
are retained separately for the other figures.

## Tables

Tables I and II state adopted model inputs and targets. Tables III and V
combine the saved structural summary with exact-star mode records. The
terminal classification is retained: an EOS-validity endpoint is not
silently renamed a maximum mass. Frozen and fast-kaon entries use the same
saved background. Tables IV and VI use the exact stored channel sample
rows; Table VII uses the published tidal point record and retains its
upper-bound marker and missing high-mass NYDelta entry. Table VIII combines
canonical BigApple exact-star values with the DD-ME2 comparison records.

Two archived table cells differ in their final displayed hundredth of a hertz
from formatting the saved full-precision checkpoint directly:

| Table/quantity | Checkpoint (Hz) | Archived display (Hz) |
| --- | --- | --- |
| III, U_K=-120 fast-kaon terminal frequency | 433.74476384856223 | 433.75 |
| V, NYDelta terminal frequency | 751.5545669768339 | 751.56 |

The release preserves both: full-precision values are unchanged in
`exact_points.json`, and `published_display.json` explicitly records the
table presentation. These are not concealed numerical replacements or new
calculated roots. All 282 displayed table cells are compared against the
independently extracted manuscript fixture.

The proof correction swaps the former Tables V and VI. The release uses
the requested corrected numbers while keeping semantic labels and values.
No manuscript or publisher proof is modified by this package.

## Scope and limits

The figures' numerical content and display selections are reproduced from
saved data. Fonts, pixel encoding or small layout details can differ from
the original article images across rendering-library versions. Reference
images are included for comparison, never copied as generated results.

Damping times are isolated-star radiative quantities. The tidal phase values
use the paper's leading-order hybrid orbital reduction with full-GR mode
inputs; they are not a binary-spacetime simulation or a detector forecast.
The observational overlays are display contours, not statistical posterior
releases. No additional scientific or priority claim is made by this package.
