# Evidence for strong shocks in the ISM of small radio sources — data release

## Authors

- Valeria Lopez — National Radio Astronomy Observatory, 520 Edgemont Road, Charlottesville, VA 22903, USA — ORCID: 0009-0009-0998-5049
- Mark Lacy — National Radio Astronomy Observatory, 520 Edgemont Road, Charlottesville, VA 22903, USA — ORCID: 0000-0002-3032-1783

Author names, affiliations and ORCIDs above are taken from the submitted manuscript so that
the deposit matches the paper. Both authors contributed equally.

Acknowledged: Kristina Nyland, Pallavi Patil. VL thanks the NRAO student program for support.

Contact: valelop800@gmail.com, mlacy@nrao.edu

## Paper

"Evidence for strong shocks in the ISM of small radio sources", Lopez & Lacy, to be submitted to
*The Astrophysical Journal Letters* (ApJL).

Paper DOI: TODO (add after acceptance)

## Description

This release contains the measurement tables behind the paper. We compare two samples of
radio-loud AGN drawn from a cross-match of the VLA Sky Survey (VLASS) with DESI DR1
spectroscopy over 0.15 < z < 0.5. One sample has jets that are still confined within the
host galaxy, the other has jets that have escaped it. For every source we give the radio
properties (flux density, angular and linear size, spectral index, 3 GHz luminosity), the
DESI emission line fluxes used in the analysis, the [OIII] 5007 W80 line width measured from
a two-Gaussian fit, and the BPT classification with its distance from the Seyfert/LINER
dividing line. The confined sources show broader [OIII] lines, sit further toward the shock
side of the BPT diagram, and have higher Balmer decrements, which we interpret as evidence
for shocks driven into the interstellar medium by jets that have not yet broken out.

## Sample definitions

Both samples are cut to 0.15 < z < 0.5, to log10(L_3GHz / W Hz^-1) > 24, and to a [OI] 6300
detection at better than 5 sigma so that every source can be placed on the [OI] BPT diagram.

- **Small (confined)**: projected linear size 10-15 kpc, jets confined within the host. n = 47.
- **Large (escaped)**: projected linear size > 25 kpc, jets escaped the host. n = 30.

The two samples are disjoint; no TARGETID appears in both.

Distances use a flat cosmology with H0 = 70 km s^-1 Mpc^-1, Omega_M = 0.3, Omega_Lambda = 0.7.

## Files

| File | Description |
|---|---|
| `catalog_lopez_lacy_2026.csv` | The release table. 77 rows keyed by `TARGETID`, 47 small then 30 large, with the `sample` column telling them apart. |
| `columns.csv` | Column name, unit, dtype, description and source for the catalog table. |
| `README.md` | This file. |
| `LICENSE` | Creative Commons Attribution 4.0 International. |
| `MANIFEST.txt` | Size, SHA-256 and a one-line description of every file. |
| `CHECKSUMS.txt` | SHA-256 of every file except itself and `MANIFEST.txt`. Verify with `shasum -a 256 -c CHECKSUMS.txt`. |
| `scripts/make_catalog_files.py` | Builds the catalog tables from the source cross-match and the fit outputs. |
| `scripts/make_release_tables.py` | Applies release rounding and writes the tables in this archive. |
| `scripts/check_release.py` | Recomputes every number quoted in the paper from the tables in this archive. |
| `scripts/jet_power.py` | Jet power from the VLASS flux density, following Willott et al. (1999). Writes the `logQ` table that `plot_loi_vs_q.py` reads. |
| `scripts/plot_bpt_lumcut_POSTEDIT_ML.py` | Paper Figure 1: [OI] BPT diagram with the SL measure. |
| `scripts/plot_w80_by_class.py` | Paper Figure 2: W80 by BPT class. |
| `scripts/bpt_distance.py` | Paper Figure 3: SL measure distributions. |
| `scripts/plot_loi_vs_q.py` | Paper Figure 4: [OI] luminosity vs jet power. |
| `scripts/plot_w80_vs_bptdist_paper.py` | Paper Figure 5: W80 vs SL measure. |
| `scripts/plot_balmer_decrement.py` | Balmer decrement figure, not in the paper. |
| `scripts/plot_oiii_nev.py` | [OIII]/Hb vs [NeV]/Hb figure, not in the paper. |
| `scripts/plot_oiii_oii.py` | [OIII] vs [OII] figure, not in the paper. |
| `scripts/plot_w80_nev_small.py` | W80 vs [NeV] figure for the small sample, not in the paper. |

The figure scripts are provided as they were run and read from the original working
directory layout (`data/`, `notes/`, `plots/`). They are included to document exactly how
each figure was made, not as a turnkey pipeline. `check_release.py` is the script to run
against this archive; it reads only the catalog table shipped here.

The last four scripts produced exploratory figures that did not make it into the paper. They
are shipped as a record of the analysis.

## What is not included

The DESI DR1 spectra themselves are not redistributed here. They are public and should be
obtained from the DESI Data Release 1 archive or through the NOIRLab SPARCL service
(https://astrosparcl.datalab.noirlab.edu/). The `TARGETID` column in the tables is the key
to retrieve them. VLASS images and the VLASS component catalog are likewise not
redistributed; see the VLASS reference below.

WISE magnitudes (W1-W4) and the [OII] 3726/3729 fluxes are deliberately left out. They were
not used in the paper, and anyone who wants them can pull them from the DESI DR1 `agngal`
value-added catalog by `TARGETID` at the URL given under Citations below.

## Column descriptions

See `columns.csv` for the machine-readable version. Notes worth repeating:

- Emission line fluxes and inverse variances come from the DESI DR1 `agngal` value-added
  catalog (Juneau et al., in preparation), matched to the VLASS positions with a 1.5 arcsec
  radius. The units are those of the FastSpecFit data model, which the VAC follows:
  `LINENAME_FLUX` is the Gaussian-integrated emission-line flux in 1e-17 erg / (cm2 s), and
  `LINENAME_FLUX_IVAR` is its inverse variance in 1e+34 cm4 s2 / erg2. See the FASTSPEC
  table (HDU03) of the FastSpecFit documentation,
  https://fastspecfit.readthedocs.io/en/3.4.3/fastspec.html.
- `HALPHA_BROAD_FLUX` is exactly 0.0 where no broad component was fitted. The matching
  `_IVAR` cell is blank in those rows. The same applies to `NEV_3426_FLUX`. Blank inverse
  variance therefore always means "line not fitted", never "measured but unknown error".
- A blank inverse variance cell means the line was not measured. It appears as `IVAR = 0` in
  the source `agngal` catalog, which is the DESI convention for no constraint; it is written
  blank here rather than 0 so that it cannot be mistaken for a measured value with infinite
  variance. Blank is preserved rather than filled.
- `Alpha` is blank for two sources in the large sample. Where a spectral index is needed for
  those two (K-correction and jet power), alpha = -0.7 is assumed, and `log_L_radio` in this
  table already has that assumption applied.
- `sample` is `"small"` or `"large"` and is what separates the two samples within the single
  table. Filtering on it reproduces the 47 and 30 row counts.
- **There are two sets of line fluxes here and they are not interchangeable.**
  - The `fit_` columns are the paper's own pyspeckit Gaussian fits, described in Section 2.2
    of the paper. **Figures 1, 3, 4 (y-axis) and 5, and the `bpt_class`, `sl_distance`,
    `log_oi_ha` and `log_oiii_hb` columns, all come from these.** They are narrow + broad
    sums; the very broad (BLR) component of H-alpha and H-beta is excluded, and [NII] 6584
    has its kinematics tied to H-alpha with the doublet ratio fixed at 1/3.
  - The columns without a prefix (`OI_6300_FLUX`, `HALPHA_FLUX`, `OIII_5007_FLUX`,
    `HBETA_FLUX`, `NEV_3426_FLUX`, `HALPHA_BROAD_FLUX`) are the DESI DR1 `agngal` reference
    values. **The [NeV] detection fractions and the Balmer decrement in the paper use
    these.**
  The two disagree: recomputing log([OI]/Ha) and log([OIII]/Hb) from the `agngal` columns
  differs from the fitted values by 0.14 and 0.18 dex in the median and by up to 1.0 and
  1.2 dex. Use the `fit_` columns for anything to do with the BPT diagram or the SL measure,
  and the `agngal` columns for [NeV] and the Balmer decrement, and the tables will reproduce
  the paper.

Values are rounded for release: RA and DEC to 6 decimals, Z to 5, `Physical_Size` to 2,
`log_L_radio` to 3, `w80` to 1, `sl_distance` to 4. All other columns are unrounded. No
measured value was altered beyond this rounding.

## How the numbers in the paper map to the columns

Running `python scripts/check_release.py` from the archive root reproduces all of the
following from the catalog table alone.

| Paper quantity | How to get it from the tables |
|---|---|
| Sample sizes: 47 small, 30 large | Row counts. |
| BPT class counts: 30/14/3 small, 26/4/0 large | Value counts of `bpt_class`, Seyfert / LINER / star forming. |
| W80 medians, Seyferts only: 688 km/s small, 513 km/s large | Median of `w80` where `bpt_class == "seyfert"`. |
| W80 KS p = 0.0065, Mann-Whitney p = 0.0026 | Two-sample tests on the same two `w80` sets. |
| W80 within the small sample: 688 Seyfert, 548 LINER, KS p = 0.42 | Median of `w80` split on `bpt_class` inside the small sample. |
| BPT Seyfert/LINER distance medians: 0.19 small, 0.38 large | Median of `sl_distance`. |
| SL Mann-Whitney p = 0.029, Anderson-Darling p = 0.026, KS p = 0.12 | Three two-sample tests on the same two `sl_distance` sets. |
| [NeV] detection at 3 sigma: 30% small, 60% large | `NEV_3426_FLUX * sqrt(NEV_3426_FLUX_IVAR) > 3` and `NEV_3426_FLUX > 0`, as a fraction of the sample. |
| [NeV] detection at 5 sigma: 21% small, 57% large | Same with a threshold of 5. |
| [NeV] at 3 sigma over a matched redshift range: 35% small, 60% large, 20 objects each | Same 3 sigma rule restricted to `0.30 < Z < 0.45`. |
| Balmer decrement medians: 4.00 small, 3.56 large | Median of `HALPHA_FLUX / HBETA_FLUX` where both are > 0. |
| Balmer Mann-Whitney p = 0.023 | Test on those two ratio sets. |
| [NeV] at 3 sigma in the low dust subset: 33% small, 84% large | Same 3 sigma rule restricted to `HALPHA_FLUX / HBETA_FLUX < 4`. |
| Balmer split by [NeV], large sample: 4.16 non-detections vs 3.25 detections, Mann-Whitney p = 0.01; small sample p = 0.26 | Median decrement of the 3 sigma non-detections against the detections, within each sample. |
| Type-1 counts: 14/47 small, 17/30 large | Count of `HALPHA_BROAD_FLUX > 0`. |
| Jet power medians: log Q = 35.11 small, 35.76 large (paper: 35.1 and 35.8) | Recomputed from `Flux`, `D_L`, `Z` and `Alpha` using Willott et al. (1999) with f = 1. `Alpha` K-corrects the 3 GHz luminosity; the 3 GHz to 151 MHz conversion uses a flat alpha = -0.7. `log_L_radio` reproduces from `Flux`, `D_L`, `Z` and `Alpha` to 0.000 dex. |

Jet power is not stored as a column; it is derived. If a `log_Q` column would be preferable,
it can be added.

Which paper figures these tables regenerate:

| Figure | Reproducible from this archive? |
|---|---|
| Fig 1, [OI] BPT diagram | Yes, from `log_oi_ha` and `log_oiii_hb`, or by recomputing them from the `fit_` fluxes. Both axes span exactly the plotted range, and reapplying the Kewley et al. (2006) boundaries returns `bpt_class` for all 77 sources. |
| Fig 2, W80 by class | Yes, from `w80` and `bpt_class`. Medians, quartiles, whiskers and outliers all match. |
| Fig 3, SL measure histogram | Yes, from `sl_distance`. |
| Fig 4, [OI] luminosity vs jet power | Yes. x from `Flux`, `D_L`, `Z`, `Alpha`; y from `fit_OI_6300_FLUX` and `D_L`. Both axes span exactly the plotted range. |
| Fig 5, W80 vs SL measure | Yes, from `w80` and `sl_distance`. |

`sl_distance` recomputes from `log_oi_ha` and `log_oiii_hb` to within 5e-5, which is the
rounding on those two columns.

## Software versions

Measurements and checks were made with:

- Python 3.11.15
- numpy 1.26.4
- scipy 1.17.1
- pandas 2.1.4
- astropy 7.2.2
- pyspeckit 1.0.4.dev
- matplotlib 3.11.0

TOPCAT (Taylor 2005) was used for the catalog cross-matching, as stated in the paper.

## Citations

Please cite the paper above. In addition:

- **DESI DR1**: DESI Collaboration, Abdul Karim, M., Adame, A. G., et al. 2026, AJ, 171, 285.
  doi:10.3847/1538-3881/ae4c43
- **VLASS survey**: Lacy, M., Baum, S. A., Chandler, C. J., et al. 2020, PASP, 132, 035001.
  doi:10.1088/1538-3873/ab63eb
- **VLASS Single Epoch Continuum catalogs** (the `Name`, `Flux`, `E_Flux`, `LAS`, `Alpha`
  columns; 20260601 versions, Epochs 2.1 and 3.2): Kimball, A., et al. 2026,
  arXiv:2606.27414. This is the reference to use for these columns (M. Lacy, 2026-09-04).
  The DRAGN Hunter association method is Gordon, Y. A., Rudnick, L., Andernach, H., et al.
  2023, ApJS, 267, 37. doi:10.3847/1538-4365/acda30
- **DESI DR1 `agngal` value-added catalog** (the emission line columns): Juneau, S., et al.,
  in preparation. https://data.desi.lbl.gov/public/dr1/vac/dr1/agngal/v1.0/
- **Jet power**: Willott, C. J., Rawlings, S., Blundell, K. M., & Lacy, M. 1999, MNRAS, 309,
  1017. doi:10.1046/j.1365-8711.1999.02907.x
- **BPT diagram**: Baldwin, J. A., Phillips, M. M., & Terlevich, R. 1981, PASP, 93, 5;
  Veilleux, S. & Osterbrock, D. E. 1987, ApJS, 63, 295; Allen, M. G., Groves, B. A.,
  Dopita, M. A., Sutherland, R. S., & Kewley, L. J. 2008, ApJS, 178, 20.
  doi:10.1086/589652
- **Shock models**: Allen et al. (2008), the MAPPINGS III library of fast radiative shock
  models. The paper cites it both alongside the BPT references above and separately for the
  shock grid itself: for the shock velocities needed to produce [NeV], for LINER-like
  ratios arising from shock heating and post-shock photoionization, and for the predicted
  distance from the Seyfert-LINER divide that the SL measure is compared against.
- **Classification / host galaxies**: Kewley, L. J., Groves, B., Kauffmann, G., & Heckman, T.
  2006, MNRAS, 372, 961; Heckman, T. M. & Best, P. N. 2014, ARA&A, 52, 589.

Software used for the measurements in these tables:

- **pyspeckit**: Ginsburg, A., Mirocha, J., Sokolov, V., Sipocz, B., et al. 2022, AJ, 163, 291.
- **numpy**: Harris, C. R., Millman, K. J., van der Walt, S. J., et al. 2020, Nature, 585, 357.
- **scipy**: Virtanen, P., Gommers, R., Oliphant, T. E., et al. 2020, Nature Methods, 17, 261.
- **astropy**: Astropy Collaboration, Price-Whelan, A. M., Lim, P. L., et al. 2022, ApJ, 935, 167.
- **matplotlib**: Hunter, J. D. 2007, CSE, 9, 90.
- **TOPCAT**: Taylor, M. B. 2005, ASPC, 347, 29.

All of these are taken from the submitted manuscript, which cites the same sources for the
same columns.

## Still to do before publishing

1. **Paper DOI.** `related_identifiers` in `metadata.json` is still `TODO-PAPER-DOI`. It is
   filled in once ApJL accepts the paper. The Zenodo DOI is reserved at draft stage and can
   go into the manuscript before then.

## Decisions settled

- **License: CC BY 4.0.** Confirmed by Mark Lacy, 2026-09-04.
- **Jet power spectral index: flat alpha = -0.7.** Confirmed by Mark Lacy, 2026-09-04. The
  medians are log Q = 35.1 for the small sample and 35.8 for the large sample, and the
  Conclusions no longer claim the two samples have nearly identical median jet powers.
  `jet_power.py` and `plot_loi_vs_q.py` both use alpha = -0.7 for the 3 GHz to 151 MHz
  conversion, as stated in the paper: `jet_power.py` computes it and `plot_loi_vs_q.py`
  reads the table it writes, so the two cannot drift apart.
- **Fitted line fluxes are shipped.** The five `fit_` columns and `log_oi_ha` /
  `log_oiii_hb` are now always written, so every figure in the paper regenerates from these
  tables.
- **VLASS attribution: Kimball et al. (2026).** Confirmed by Mark Lacy, 2026-09-04.
- **`agngal` flux unit: 1e-17 erg / (cm2 s), inverse variance 1e+34 cm4 s2 / erg2.** This
  is the FastSpecFit data model, FASTSPEC table (HDU03),
  https://fastspecfit.readthedocs.io/en/3.4.3/fastspec.html. It agrees with what Mark Lacy
  reasoned on 2026-09-04 from the DESI spectral units, so it is now documented rather than
  inferred.

Settled with Mark Lacy on 2026-09-08:

- **One file, not two.** The release is a single `catalog_lopez_lacy_2026.csv` of 77 rows
  keyed by `TARGETID`, with `sample` separating small from large.
- **Blank, not 0, for inverse variance** where there is no measurement. See the column notes
  above.
- **WISE magnitudes and [OII] fluxes stay out.** They were not used in the paper and are
  available from the `agngal` VAC by `TARGETID`.
- **Valeria Lopez makes the deposit**, with Mark Lacy as second creator. Both are listed in
  `metadata.json` with their ORCIDs and the NRAO affiliation, in the name form used on the
  submitted manuscript.
