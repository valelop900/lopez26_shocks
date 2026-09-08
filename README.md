# Evidence for strong shocks in the ISM of small radio sources

Lopez & Lacy 2026, submitted to ApJL. arXiv: TBD.

Analysis code for a study of two samples of radio-loud AGN at 0.15 < z < 0.5, drawn from a
cross-match of the VLA Sky Survey with DESI DR1: 47 sources 10-15 kpc across, whose jets are
still inside the host galaxy, and 30 sources larger than 25 kpc, whose jets have broken out
of it. We compare the two in [OIII] W80, position on the [OI]/Ha versus [OIII]/Hb diagram,
and [NeV] 3426 detection rate. The small sources have broader lines, sit closer to the LINER
region and mostly lack [NeV], which points to jet-driven shocks powering much of their line
emission rather than photoionization by the AGN.

The catalog behind the paper is released separately on Zenodo, doi to be added. The DESI
spectra and the VLASS source catalogs are not in this repository; they come from the public
DESI DR1 and VLASS archives.

Figures:

| Figure | Script |
|---|---|
| 1, [OI] BPT diagram | `scripts/plot_bpt_lumcut_POSTEDIT_ML.py` |
| 2, W80 by BPT class | `scripts/plot_w80_by_class.py` |
| 3, SL measure distributions | `checks/bpt_distance.py` |
| 4, [OI] luminosity vs jet power | `scripts/plot_loi_vs_q.py` |
| 5, W80 vs SL measure | `scripts/plot_w80_vs_bptdist_paper.py` |

The scripts read from `data/` and `notes/` and write to `plots/`, and are meant to be run
from the project root.
