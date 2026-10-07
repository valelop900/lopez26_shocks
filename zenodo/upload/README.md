# Data for: Evidence for strong shocks in the ISM of small radio sources

Lopez, V. and Lacy, M., 2026, ApJL. DOI to be added on publication.

## What the data are

One table of 77 radio-loud AGN at 0.15 < z < 0.5, drawn from a cross-match of the VLA Sky Survey
(VLASS) with DESI Data Release 1 spectroscopy, with [O I] 6300 detected above 5 sigma and a
rest-frame 3 GHz luminosity above 10^24 W/Hz. The small sample (45 sources) has projected radio
sizes of 10-15 kpc, jets still inside the host galaxy. The large sample (32 sources) has sizes
above 25 kpc, jets that have broken out. For each source the table gives the VLASS radio
properties, the DESI DR1 `agngal` emission-line fluxes and inverse variances, Gaussian line
fits for H-beta, [O III] 5007, H-alpha, [N II] 6584 and [O I] 6300, the two BPT line ratios,
the [O III] W80 line width corrected for instrumental resolution, the BPT class, and the SL
measure (perpendicular distance from the Seyfert/LINER line). Rows are keyed by DESI `TARGETID`;
the `sample` column is `small` or `large`.
For two sources (TARGETIDs 39627808774818067 and 39627709696969353) `LAS` and `Physical_Size` give
the 5 sigma extent of the radio emission in the VLASS image rather than the catalog LAS, because the
catalog component is one part of a larger source.

## Files

| file | what it is |
|---|---|
| `catalog_lopez_lacy_2026.csv` | the table, 77 rows, 36 columns |
| `columns.csv` | one row per column: name, unit, source, description |
| `scripts/` | the scripts that build the table and make the figures |
| `CHECKSUMS.txt`, `MANIFEST.txt` | SHA-256 of every file, and a one-line description of each |
| `LICENSE` | CC BY 4.0 |

Blank cells in an inverse-variance column mean no measurement. `columns.csv` says which line
fluxes come from DESI and which from the fits here; the two sets are not interchangeable.

The DESI spectra and VLASS images are not included. They are public: DESI DR1 via the DESI
data archive or NOIRLab SPARCL by `TARGETID`, VLASS via the NRAO archive or the CADC cutout
service.

## Reproducing the numbers and figures

Python 3.11.15 with numpy 1.26.4, pandas 2.1.4, scipy 1.17.1, matplotlib 3.11.0,
astropy 7.2.2, pyspeckit 1.0.4, requests 2.34.2.

Every statistic quoted in the paper, from the table alone:

    python scripts/check_release.py

The figure scripts need the line-fit tables in `notes/` and the two `data/catalog_*.csv`
files, which ship with the code repository (github.com/valelop900/lopez26_shocks) rather than
here. From the root of that repository:

    python scripts/fig_bpt_2panel.py       # BPT diagram and SL histogram
    python scripts/fig_w80_2panel.py       # W80 by class and W80 against SL
    python scripts/plot_loi_vs_q.py        # [O I] luminosity against jet power
    python scripts/oiii_profiles.py        # [O III] profiles; also needs data/spectra/
    python scripts/fig_examples.py         # radio contours on optical images; fetches cutouts online

What each script does:

| script | what it makes |
|---|---|
| `check_release.py` | every statistic in the paper, from the table alone |
| `fig_bpt_2panel.py` | the BPT diagram and the SL histogram |
| `fig_w80_2panel.py` | W80 by class, and W80 against the SL measure |
| `plot_loi_vs_q.py` | [O I] luminosity against jet power |
| `oiii_profiles.py` | [O III] profiles of the broadest small sources; needs the DESI spectra |
| `fig_examples.py` | one small and one large source with VLASS contours; fetches cutouts online |
| `plot_bpt.py` | the BPT classification table the figure scripts read |
| `jet_power.py` | the jet-power table `plot_loi_vs_q.py` reads |
| `make_release_tables.py` | builds `catalog_lopez_lacy_2026.csv` |
| `paperstyle.py` | matplotlib settings and figure sizes, imported by the figure scripts |

## Data sources

- VLASS Single Epoch Continuum catalogs (Epochs 2.1 and 3.2, 20260601 versions), for `Name`,
  `Flux`, `E_Flux`, `LAS`, `Alpha`: Kimball, A., et al. 2026, arXiv:2606.27414. Survey design:
  Lacy, M., Baum, S. A., Chandler, C. J., et al. 2020, PASP, 132, 035001,
  doi:10.1088/1538-3873/ab63eb. Component association: Gordon, Y. A., Rudnick, L.,
  Andernach, H., et al. 2023, ApJS, 267, 37, doi:10.3847/1538-4365/acda30.
- DESI Data Release 1: DESI Collaboration, Abdul Karim, M., Adame, A. G., et al. 2026, AJ,
  171, 285, doi:10.3847/1538-3881/ae4c43. Emission-line columns from the DR1 `agngal`
  value-added catalog, Juneau, S., et al., in preparation.
- Legacy Surveys DR9 images, used for the optical panels of `fig_examples.pdf`: Dey, A.,
  Schlegel, D. J., Lang, D., et al. 2019, AJ, 157, 168, doi:10.3847/1538-3881/ab089d.
- WISE, used in the paper for the 12 micron luminosities (not in this table): Wright, E. L.,
  Eisenhardt, P. R. M., Mainzer, A. K., et al. 2010, AJ, 140, 1868,
  doi:10.1088/0004-6256/140/6/1868.
- Jet power: Willott, C. J., Rawlings, S., Blundell, K. M., & Lacy, M. 1999, MNRAS, 309,
  1017, doi:10.1046/j.1365-8711.1999.02907.x. BPT boundaries: Kewley, L. J., Groves, B.,
  Kauffmann, G., & Heckman, T. 2006, MNRAS, 372, 961. Shock models: Allen, M. G., Groves,
  B. A., Dopita, M. A., Sutherland, R. S., & Kewley, L. J. 2008, ApJS, 178, 20,
  doi:10.1086/589652.
- Software: pyspeckit (Ginsburg, A., et al. 2022, AJ, 163, 291), numpy (Harris, C. R., et al.
  2020, Nature, 585, 357), scipy (Virtanen, P., et al. 2020, Nature Methods, 17, 261), astropy
  (Astropy Collaboration 2013, A&A, 558, A33; 2018, AJ, 156, 123; 2022, ApJ, 935, 167),
  matplotlib (Hunter, J. D. 2007, CSE, 9, 90).

## License

The data are CC BY 4.0 (`LICENSE`). The code in `scripts/` is MIT, as in the code repository.

## How to cite

Lopez, V. and Lacy, M. 2026, "Evidence for strong shocks in the ISM of small radio sources",
ApJL. DOI to be added on publication. Cite this dataset by its Zenodo DOI as well.
