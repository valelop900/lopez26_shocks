# lopez26_shocks

Code for Lopez and Lacy 2026, "Evidence for strong shocks in the ISM of small radio sources",
submitted to ApJL. We take two samples of radio-loud AGN at 0.15 < z < 0.5 from VLASS matched to
DESI DR1. 44 sources are 10 to 15 kpc across and 33 are larger than 25 kpc. The small ones have
broader [OIII], sit closer to the LINER side of the [OI] BPT diagram and mostly lack [NeV].

The data release lives in `zenodo/upload/`. This gives every number in the paper from the
released table:

    python zenodo/upload/scripts/check_release.py

The figure scripts live in `zenodo/upload/scripts/` and run from the project root. The figures
are in `figures/` and the line fit tables the scripts read are in `notes/`. We do not include the
raw VLASS and DESI tables, the DESI spectra or the VLASS cutouts, they are public. So
`oiii_profiles.py` (needs the spectra) and `fig_examples.py` (fetches cutouts online) do not run
from the release alone.

The code is MIT (`LICENSE`). The data in `zenodo/upload/` are CC BY 4.0, same as the Zenodo record.

We will add the Zenodo DOI and the arXiv link when we have them.
