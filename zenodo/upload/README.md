# Data for: Evidence for strong shocks in the ISM of small radio sources

Data release for Lopez and Lacy (2026), "Evidence for strong shocks in the ISM of small radio sources",
accepted for publication in The Astrophysical Journal Letters.

## What the data are

One table of 77 radio-loud AGN at 0.15 < z < 0.5. We matched the VLA Sky Survey (VLASS) to
DESI Data Release 1 spectra and kept sources with [O I] 6300 detected above 5 sigma and a
rest-frame 3 GHz luminosity above 10^24 W/Hz. The small sample (44 sources) has radio sizes of
10 to 15 kpc, jets still inside the host. The large sample (33 sources) has sizes above 25 kpc,
jets that have broken out.

Each row gives the VLASS radio properties, the DESI DR1 `agngal` line fluxes and inverse
variances, our Gaussian line fits for H-beta, [O III] 5007, H-alpha, [N II] 6584 and [O I] 6300,
the two BPT ratios, the [O III] W80 width corrected for instrumental resolution, the BPT class
and the SL measure (distance from the Seyfert/LINER line). We key the rows by DESI `TARGETID`.
The `sample` column says `small` or `large`.

For three sources (TARGETIDs 39628383604179664, 39627709696969353 and 39627808774818067)
we remeasured `LAS` and `Physical_Size` from the VLASS image, since the catalog component is
one part of a larger source.

`Common name`, `Host galaxy image`, `Merger_flg` and `Host galaxy image source` come from
looking at the host images by eye. `make_release_tables.py` does not regenerate them, it
rebuilds the other 36 columns.

## Files

| file | what it is |
|---|---|
| `catalog_lopez_lacy_2026.csv` | the table, 77 rows, 40 columns |
| `columns.csv` | one row per column: name, unit, dtype, description, source |
| `scripts/` | the scripts that build the table and make the figures |
| `CHECKSUMS.txt`, `MANIFEST.txt` | SHA-256 of every file, and one line on each |
| `LICENSE` | CC BY 4.0 |

## Columns

Units are in the second column. Line fluxes are in 1e-17 erg/s/cm2 and their inverse variances
in 1e34 cm4 s2/erg2, the DESI convention. Coordinates are given to 1e-6 deg, redshifts to 1e-5,
radio flux densities to 1e-3 mJy, and line fluxes and inverse variances to 5 significant figures.
A blank cell in an inverse variance column means no measurement. The `fit_` columns are our own
measurements and the upper-case `_FLUX` columns are DESI's. The two sets are different measurements.

| column | unit | description |
|---|---|---|
| `TARGETID` |  | DESI unique target identifier |
| `sample` |  | Sample flag: "small" (10-15 kpc, 44 rows) or "large" (>25 kpc, 33 rows). Filter on this to separate the two samples |
| `Name` |  | VLASS radio component name |
| `RA` | deg | Right ascension (J2000) of the radio source |
| `DEC` | deg | Declination (J2000) of the radio source |
| `Z` |  | DESI spectroscopic redshift |
| `Flux` | mJy | VLASS 3 GHz total flux density |
| `E_Flux` | mJy | Uncertainty on Flux |
| `LAS` | arcsec | Largest angular size of the radio source; for 39628383604179664, 39627709696969353, 39627808774818067 remeasured from the VLASS image because the catalog component is one part of a larger source |
| `Physical_Size` | kpc | Projected linear size from LAS and redshift; for 39628383604179664, 39627709696969353, 39627808774818067 from the remeasured LAS |
| `Alpha` |  | Catalog radio spectral index (S ~ nu^alpha), used to K-correct the 3 GHz luminosity. NOT used in the paper's jet power estimate, which converts 3 GHz to 151 MHz with a flat alpha = -0.7. Blank for 2 large sources; -0.7 assumed for those |
| `E_Alpha` |  | Uncertainty on Alpha |
| `D_L` | Mpc | Luminosity distance |
| `log_L_radio` | log10(W/Hz) | log10 rest-frame 3 GHz radio luminosity, K-corrected as (1+z)^(-1-alpha) |
| `w80` | km/s | [OIII] 5007 W80 line width, two-Gaussian pyspeckit fit, instrumental resolution removed |
| `bpt_class` |  | BPT classification from the [OI]/Ha diagram: seyfert, liner, or sf |
| `sl_distance` | dex | Perpendicular distance from the Seyfert/LINER line y = 1.18x + 1.30 in the [OI] BPT plane; positive = Seyfert side |
| `NEV_3426_FLUX` | 1e-17 erg/s/cm2 | [NeV] 3426 emission line flux |
| `NEV_3426_FLUX_IVAR` | 1e34 cm4 s2/erg2 | Inverse variance of NEV_3426_FLUX. Blank where flux is 0.0 (line not fitted) |
| `OI_6300_FLUX` | 1e-17 erg/s/cm2 | [OI] 6300 emission line flux |
| `OI_6300_FLUX_IVAR` | 1e34 cm4 s2/erg2 | Inverse variance of OI_6300_FLUX |
| `OIII_5007_FLUX` | 1e-17 erg/s/cm2 | [OIII] 5007 emission line flux |
| `OIII_5007_FLUX_IVAR` | 1e34 cm4 s2/erg2 | Inverse variance of OIII_5007_FLUX |
| `HALPHA_FLUX` | 1e-17 erg/s/cm2 | Narrow H-alpha emission line flux |
| `HALPHA_FLUX_IVAR` | 1e34 cm4 s2/erg2 | Inverse variance of HALPHA_FLUX |
| `HBETA_FLUX` | 1e-17 erg/s/cm2 | Narrow H-beta emission line flux |
| `HBETA_FLUX_IVAR` | 1e34 cm4 s2/erg2 | Inverse variance of HBETA_FLUX |
| `HALPHA_BROAD_FLUX` | 1e-17 erg/s/cm2 | Broad H-alpha emission line flux. 0.0 where no broad component was fitted; nonzero identifies Type-1 AGN |
| `HALPHA_BROAD_FLUX_IVAR` | 1e34 cm4 s2/erg2 | Inverse variance of HALPHA_BROAD_FLUX. Blank where flux is 0.0 |
| `fit_HB_FLUX` | 1e-17 erg/s/cm2 | Fitted H-beta 4861 flux, narrow + broad components. The very broad (BLR) component is excluded |
| `fit_OIII_5007_FLUX` | 1e-17 erg/s/cm2 | Fitted [OIII] 5007 flux, narrow + broad components |
| `fit_HA_FLUX` | 1e-17 erg/s/cm2 | Fitted H-alpha 6563 flux, narrow + broad components. The very broad (BLR) component is excluded |
| `fit_NII_6584_FLUX` | 1e-17 erg/s/cm2 | Fitted [NII] 6584 flux, narrow + broad components. Kinematics tied to H-alpha, doublet ratio fixed at 1/3 |
| `fit_OI_6300_FLUX` | 1e-17 erg/s/cm2 | Fitted [OI] 6300 flux, narrow + broad components. This is the flux behind the y-axis of paper Figure 4 |
| `log_oi_ha` | dex | log10(fit_OI_6300_FLUX / fit_HA_FLUX). x-axis of paper Figure 1 |
| `log_oiii_hb` | dex | log10(fit_OIII_5007_FLUX / fit_HB_FLUX). y-axis of paper Figure 1 |
| `Common name` |  | Common catalog name of the radio source where one exists, else blank |
| `Host galaxy image` |  | Host morphology from the optical image: E, S, interacting, merger, BCG, or blank if unclear |
| `Merger_flg` |  | 1 if the host shows signs of interaction or merging in the optical image, else 0 |
| `Host galaxy image source` |  | Image used for the host classification: LDR10 (Legacy Surveys DR10) or EUCLID |

We do not include the DESI spectra or the VLASS images. They are public: get DESI DR1 from the
DESI archive or NOIRLab SPARCL by `TARGETID`, and VLASS from the NRAO archive or the CADC
cutout service.

## Running the scripts

We used Python 3.11.15 with numpy 1.26.4, pandas 2.1.4, scipy 1.17.1, matplotlib 3.11.0,
astropy 7.2.2, pyspeckit 1.0.4 and requests 2.34.2.

This gives every number in the paper from the table alone:

    python scripts/check_release.py

The figure scripts need the line fit tables in `notes/` and the two `data/catalog_*.csv`
files. Those live in the code repository (github.com/valelop900/lopez26_shocks), not here.
Run them from the root of that repository:

    python scripts/fig_bpt_2panel.py       # BPT diagram and SL histogram
    python scripts/fig_w80_2panel.py       # W80 by class, W80 vs SL
    python scripts/plot_loi_vs_q.py        # [O I] luminosity vs jet power
    python scripts/oiii_profiles.py        # [O III] profiles, needs data/spectra/
    python scripts/fig_examples.py         # radio contours on optical images, fetches cutouts online

| script | what it makes |
|---|---|
| `check_release.py` | every number in the paper, from the table |
| `fig_bpt_2panel.py` | BPT diagram and SL histogram |
| `fig_w80_2panel.py` | W80 by class, W80 vs SL |
| `plot_loi_vs_q.py` | [O I] luminosity vs jet power |
| `oiii_profiles.py` | [O III] profiles of the broadest small sources, needs the DESI spectra |
| `fig_examples.py` | one small and one large source with VLASS contours, fetches cutouts online |
| `plot_bpt.py` | the BPT classification table the figure scripts read |
| `jet_power.py` | the jet power table `plot_loi_vs_q.py` reads |
| `make_release_tables.py` | builds `catalog_lopez_lacy_2026.csv` |
| `paperstyle.py` | matplotlib settings and figure sizes, the figure scripts import it |

## Data sources

- VLASS Single Epoch Continuum catalogs (Epochs 2.1 and 3.2, 20260601 versions), for `Name`,
  `Flux`, `E_Flux`, `LAS`, `Alpha`: Kimball, A., et al. 2026, arXiv:2606.27414. Survey design:
  Lacy, M., Baum, S. A., Chandler, C. J., et al. 2020, PASP, 132, 035001,
  doi:10.1088/1538-3873/ab63eb. Component association: Gordon, Y. A., Rudnick, L.,
  Andernach, H., et al. 2023, ApJS, 267, 37, doi:10.3847/1538-4365/acda30.
- DESI Data Release 1: DESI Collaboration, Abdul Karim, M., Adame, A. G., et al. 2026, AJ,
  171, 285, doi:10.3847/1538-3881/ae4c43. The line columns come from the DR1 `agngal`
  value-added catalog, Juneau, S., et al., in preparation.
- Legacy Surveys DR9 images, for the optical panels of `fig_examples.pdf`: Dey, A.,
  Schlegel, D. J., Lang, D., et al. 2019, AJ, 157, 168, doi:10.3847/1538-3881/ab089d.
- Jet power: Willott, C. J., Rawlings, S., Blundell, K. M., and Lacy, M. 1999, MNRAS, 309,
  1017, doi:10.1046/j.1365-8711.1999.02907.x. BPT boundaries: Kewley, L. J., Groves, B.,
  Kauffmann, G., and Heckman, T. 2006, MNRAS, 372, 961. Shock models: Allen, M. G., Groves,
  B. A., Dopita, M. A., Sutherland, R. S., and Kewley, L. J. 2008, ApJS, 178, 20,
  doi:10.1086/589652.
- Software: pyspeckit (Ginsburg, A., et al. 2022, AJ, 163, 291), numpy (Harris, C. R., et al.
  2020, Nature, 585, 357), scipy (Virtanen, P., et al. 2020, Nature Methods, 17, 261), astropy
  (Astropy Collaboration 2013, A&A, 558, A33, 2018, AJ, 156, 123, and 2022, ApJ, 935, 167),
  matplotlib (Hunter, J. D. 2007, CSE, 9, 90).

## License

The data are CC BY 4.0 (`LICENSE`). The scripts are MIT, as in the code repository.

## How to cite

Lopez, V. and Lacy, M. 2026, "Evidence for strong shocks in the ISM of small radio sources",
ApJL, in press. Please also cite this dataset by its Zenodo DOI, 10.5281/zenodo.23326653.
