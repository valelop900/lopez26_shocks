# lopez26_shocks

Code for Lopez & Lacy 2026, "Evidence for strong shocks in the ISM of small radio sources",
submitted to ApJL. Two samples of radio-loud AGN at 0.15 < z < 0.5 from a cross-match of VLASS
with DESI DR1: 47 sources 10-15 kpc across and 30 larger than 25 kpc. The small ones have
broader [OIII], sit closer to the LINER region of the [OI] BPT diagram and mostly lack [NeV].

The data release is in `zenodo/upload/`. Run `zenodo/upload/scripts/check_release.py` to
reproduce every number quoted in the paper from the released catalog. The scripts that make the
five paper figures are in `zenodo/upload/scripts/` and run from the project root; the figures
themselves are in `figures/`. The line fits they read are in `notes/`. The raw VLASS x DESI
cross-match tables, the DESI spectra and the VLASS cutouts come from the public archives and are
not redistributed here, so the few scripts that read them will not run as shipped.

The code is MIT licensed (`LICENSE`). The data release in `zenodo/upload/` is CC BY 4.0, same as the Zenodo record.

Zenodo DOI and arXiv link to be added once the record and preprint are up.
