# lopez26_shocks

Code for Lopez & Lacy 2026, "Evidence for strong shocks in the ISM of small radio sources",
submitted to ApJL.

Two samples of radio-loud AGN at 0.15 < z < 0.5, from a cross-match of VLASS with DESI DR1:
47 sources 10-15 kpc across, whose jets are still inside the host galaxy, and 30 sources
larger than 25 kpc, whose jets have broken out. We compare them in [OIII] W80, position on
the [OI]/Ha versus [OIII]/Hb diagram, and [NeV] 3426 detection rate. The small sources have
broader lines, sit closer to the LINER region and mostly lack [NeV], which points to
jet-driven shocks powering much of their line emission rather than AGN photoionization.

Last Updated: 2026-09-08

Data: the catalog is on Zenodo, DOI TBD. The DESI spectra and VLASS catalogs come from the
public archives, not from here.

Figures:

- Fig 1, [OI] BPT diagram: `scripts/plot_bpt_lumcut_POSTEDIT_ML.py`
- Fig 2, W80 by BPT class: `scripts/plot_w80_by_class.py`
- Fig 3, SL measure distributions: `checks/bpt_distance.py`
- Fig 4, [OI] luminosity vs jet power: `scripts/plot_loi_vs_q.py`
- Fig 5, W80 vs SL measure: `scripts/plot_w80_vs_bptdist_paper.py`

Scripts read from `data/` and `notes/` and write to `plots/`. Run them from the project root.

## To do

- Adding the Zenodo DOI here and in the paper once the draft record is created and the DOI
  reserved.
- Adding the arXiv link once we post.
- Filling in `related_identifiers` in `zenodo/metadata.json`, currently `TODO-PAPER-DOI`,
  after ApJL accepts.
- Deciding what stays in the repo before it goes public: the four raw cross-match CSVs in
  `data/`, the QC and talk material in `plots/`, and `scripts/old/`.
- Pinning the environment. There is no `environment.yml` yet.
