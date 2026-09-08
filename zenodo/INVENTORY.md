# Project inventory for the Zenodo release

Generated 2026-09-04. Sizes as reported by `ls -l`.

Category key:

- **(a) release data** — goes into `zenodo/upload/`
- **(b) analysis script** — produced release data or a paper figure
- **(c) intermediate / scratch** — kept for provenance, not released
- **(d) raw input, do not redistribute** — DESI / VLASS data obtained elsewhere

---

## data/

| File | Size | Cat | Description |
|---|---|---|---|
| `catalog_small.csv` | 18 KB | a | Release table, small (confined) sample, 47 rows, 29 columns. Output of `make_catalog_files.py`. |
| `catalog_large.csv` | 11 KB | a | Release table, large (escaped) sample, 30 rows, 29 columns. Output of `make_catalog_files.py`. |
| `OI_sample_small.csv` | 86 KB | d | Original VLASS x DESI cross-match from Mark, small sample, 67 rows, 140 columns. Uses `TARGETID` / `Physical_Size`. |
| `OI_sample_large.csv` | 39 KB | d | Same for the large sample. |
| `VLASS3_2_OI_small.csv` | 54 KB | d | Later VLASS 3.2 cross-match, small, 44 rows. Uses `TARGETID_1` / `Physical_size` (known name mismatch). |
| `VLASS3_2_OI_large.csv` | 36 KB | d | Same for the large sample. |
| `VLASS3_2_OI_small_Q.csv` | 56 KB | c | Above plus `logL3` and `logQ` columns, written by `jet_power.py`. Pre-luminosity-cut. |
| `VLASS3_2_OI_large_Q.csv` | 37 KB | c | Same for the large sample. Source of the `log_L_radio` patch for the two NaN-Alpha sources. |
| `small_new_cut24.csv` | 30 KB | c | Small sample after the log L > 24 cut. Scratch. |
| `small_new_cut27.csv` | 34 KB | c | Small sample after an alternative log L > 27 cut. Scratch, not used in the paper. |
| `QC_new_large.csv` | 2.9 KB | c | Quality-control table for the newly added large sources. |
| `get_desi_spec.ipynb` | 129 KB | c | Notebook used to pull DESI spectra via SPARCL. Duplicate of the copy in `scripts/`. |
| `spectra/` | 130 files, 35 MB | d | Per-object DESI DR1 spectra extracted to CSV. **Not redistributed** — get from DESI DR1 / SPARCL by `TARGETID`. |
| `vlass_cutouts_small/` | 49 files, 23 MB | d | VLASS image cutouts. **Not redistributed** — VLASS images are public. |

## notes/

| File | Size | Cat | Description |
|---|---|---|---|
| `2026-07-28_luminosity_check.csv` | 21 KB | c | **Master analysis file.** Carries the luminosity cut and the patched `log_L_radio` for the two large sources with NaN `Alpha`. Every released TARGETID appears here (verified). |
| `2026-07-31_bpt_class_lumcut_v2.csv` | 5.5 KB | c | Final BPT classes and line ratios after the luminosity cut. Direct input to the release tables. |
| `2026-07-13_resolution_w80.csv` | 20 KB | c | W80 measurements, original sample, instrumental resolution removed. |
| `2026-07-22_w80_new_large.csv` | 8.1 KB | c | W80 for the sources added to the large sample. |
| `2026-07-31_w80_new_small24.csv` | 6.4 KB | c | W80 for the sources added to the small sample. These three concatenate into the released `w80` column. |
| `2026-07-08_oiii_fits.csv` | 11 KB | c | [OIII] two-Gaussian fit parameters, original run. |
| `2026-07-22_oiii_fits_new_large.csv` | 4.5 KB | c | [OIII] fits, new large sources. |
| `2026-07-31_oiii_fits_new_small24.csv` | 3.5 KB | c | [OIII] fits, new small sources. |
| `2026-07-09_oi_fits.csv` | 11 KB | c | [OI] 6300 fits, original run. |
| `2026-07-22_oi_fits_new_large.csv` | 4.4 KB | c | [OI] fits, new large sources. |
| `2026-07-31_oi_fits_new_small24.csv` | 3.5 KB | c | [OI] fits, new small sources. |
| `2026-07-16_halpha_fits.csv` | 19 KB | c | H-alpha fits, original run. |
| `2026-07-22_halpha_fits_new_large.csv` | 7.5 KB | c | H-alpha fits, new large sources. |
| `2026-07-31_halpha_fits_new_small24.csv` | 6.3 KB | c | H-alpha fits, new small sources. |
| `2026-07-15_hbeta_fits.csv` | 14 KB | c | H-beta fits, original run. |
| `2026-07-22_hbeta_fits_new_large.csv` | 5.6 KB | c | H-beta fits, new large sources. |
| `2026-07-31_hbeta_fits_new_small24.csv` | 4.4 KB | c | H-beta fits, new small sources. |
| `2026-07-16_bpt_class.csv` | 4.3 KB | c | First BPT classification, superseded. |
| `2026-07-22_bpt_class_expanded.csv` | 6.1 KB | c | BPT classes after the large sample was expanded, superseded. |
| `2026-07-29_bpt_class_lumcut.csv` | 4.6 KB | c | BPT classes after the luminosity cut, v1, superseded by `_v2`. |
| `2026-07-13_fwhm_avg.csv` | 4.5 KB | c | Averaged instrumental FWHM per object, v1. |
| `2026-07-31_fwhm_avg_v2.csv` | 12 KB | c | Averaged instrumental FWHM, v2. Used for the resolution correction on W80. |
| `2026-07-31_luminosity_small_new.csv` | 5.3 KB | c | Radio luminosities for the newly added small sources. |
| `targetid_redshift.csv` | 5.6 KB | c | TARGETID to redshift lookup. |
| `2026-07-31_targetid_redshift_new24.csv` | 898 B | c | Same for the new small sources. |
| `2026-07-07_good_targetids.txt` | 1.4 KB | c | TARGETIDs passing the first cutout QC pass. |
| `2026-07-22_new_large_targetids.txt` | 540 B | c | TARGETIDs added to the large sample. |
| `2026-07-31_new_small24_targetids.txt` | 432 B | c | TARGETIDs added to the small sample. |
| `2026-07-07_cutout_QC_small.txt` | 9.2 KB | c | Per-source VLASS cutout QC notes, small sample. |
| `2026-07-07_cutout_QC_large_final.txt` | 4.6 KB | c | Same, large sample. |
| `2026-07-13_QC_recheck_small.txt` | 1.2 KB | c | Second QC pass on the small sample. |
| `2026-07-22_QC_new_large.txt` | 2.5 KB | c | QC on the newly added large sources. |
| `2026-07-31_vlass_qc_small_verdicts.txt` | 2.9 KB | c | Final keep/drop verdicts on small-sample cutouts. |
| `2026-07-13_STAGE_RESULTS_oiii.txt` | 3.2 KB | c | Staged [OIII] fitting results log. |
| `2026-07-13_final_oiii_census.txt` | 1.3 KB | c | Count of successful [OIII] fits. |
| `2026-07-13_oiii_doublet_census.txt` | 1.1 KB | c | Count of resolved [OIII] doublets. |
| `2026-07-13_fit_handcheck.txt` | 1.1 KB | c | Notes from hand-checking individual fits. |
| `2026-07-09_broad_fraction.txt` | 1.4 KB | c | Early broad-line fraction estimate. |
| `2026-08-05_mark_handwritten_notes.txt` | 406 B | c | **Mark's notes, 2026-08-05.** Jet power run results, the log L > 24 cut reminder, and a reminder to verify the Willott 1999 normalization. No Zenodo instructions. |

**No `2026-09-04_mark_zenodo_notes.txt` exists**, and no file anywhere in `notes/` mentions
Zenodo, a data release, or licensing. The four open questions are therefore still open.

## scripts/

| File | Size | Cat | Description |
|---|---|---|---|
| `make_catalog_files.py` | 2.1 KB | b | **Builds the release tables.** Merges the four source cross-matches with W80, BPT and luminosity, computes `sl_distance`, writes `data/catalog_{small,large}.csv`. |
| `jet_power.py` | 810 B | b | Radio luminosity and Willott et al. (1999) jet power, K-corrected. Writes the `_Q` files. |
| `plot_bpt_lumcut_POSTEDIT_ML.py` | 5.5 KB | b | Produces `plots/fig_bpt.pdf`. Latest of the BPT-figure variants. |
| `plot_balmer_decrement.py` | 2.5 KB | b | Produces `plots/fig_balmer.pdf` and the Balmer medians and MW p-value. |
| `plot_w80_by_class.py` | 2.2 KB | b | Produces `plots/fig_w80_by_class.pdf` and the W80 medians, KS and MW p-values. |
| `plot_w80_vs_bptdist_paper.py` | 2.2 KB | b | Produces `plots/fig_w80_bptdist.pdf`. |
| `plot_loi_vs_q.py` | 2.7 KB | b | Produces `plots/fig_loi_vs_q.pdf`. |
| `plot_oiii_nev.py` | 2.5 KB | b | Produces `plots/fig_oiii_nev.pdf` and the [NeV] detection counts. |
| `plot_oiii_oii.py` | 2.4 KB | b | Produces `plots/fig_oiii_oii.pdf`. |
| `plot_w80_nev_small.py` | 2.8 KB | b | Produces `plots/fig_w80_nev_small.pdf`. |
| `type1_counts.py` | 1.0 KB | b | Type-1 counts from nonzero `HALPHA_BROAD_FLUX`. |
| `fit_oiii_all.py`, `fit_oiii_new_large.py`, `fit_oiii_new_small24.py` | ~2.7 KB each | b | pyspeckit two-Gaussian [OIII] fits for the three batches. |
| `fit_oi_all.py`, `fit_oi_new_large.py`, `fit_oi_new_small24.py` | ~2.1 KB each | b | [OI] 6300 fits. |
| `fit_halpha_all.py`, `fit_halpha_new_large.py`, `fit_halpha_new_small24.py` | ~4.1 KB each | b | H-alpha fits including the broad component. |
| `fit_hbeta_all.py`, `fit_hbeta_new_large.py`, `fit_hbeta_new_small24.py` | ~2.6 KB each | b | H-beta fits. |
| `w80_new_large.py`, `w80_new_small24.py` | ~2.0 KB each | b | W80 from the [OIII] fits, resolution removed. |
| `fwhm_avg.py`, `fwhm_avg_v2.py` | ~1.3 KB each | b | Instrumental FWHM averaging for the resolution correction. |
| `lum_new_small.py` | 612 B | b | Radio luminosities for the new small sources. |
| `plot_bpt_lumcut.py`, `plot_bpt_lumcut_v2.py`, `plot_bpt_lumcut_POSTEDIT.py` | 3.9-4.9 KB | c | Earlier BPT figure variants. `_v2` and `_POSTEDIT` are byte-identical. |
| `plot_bpt.py`, `plot_bpt_25kpc.py`, `plot_bpt_expanded.py` | 1.9-3.2 KB | c | Older BPT figures, superseded. |
| `plot_loi_vs_q_variants.py` | 2.6 KB | c | Exploratory jet-power panel variants. |
| `plot_w80_cut_norm.py`, `plot_w80_hist_expanded.py`, `w80_by_nev.py`, `w80_vs_bptdist.py`, `width_by_class_expanded.py` | 0.8-2.3 KB | c | Exploratory W80 plots and statistics. |
| `get_desi_spec.ipynb` | 129 KB | c | SPARCL spectrum download notebook. |
| `get_new_spectra.py`, `ids_for_sparcl.py`, `get_good_targetids.py`, `get_large_coords.py` | 0.1-1.0 KB | c | Helpers for pulling spectra and target lists. |
| `add_new_redshifts.py`, `make_redshift_table.py`, `make_new_targetid_list.py`, `make_qc_file.py`, `make_cut_small.py`, `match_old_new.py`, `check_new_large.py`, `check_sample_coverage.py`, `check_targetid_overlap.py`, `screen_hbeta.py` | 0.2-1.0 KB | c | Small bookkeeping and consistency scripts. |
| `talk_*.py` (17 files) | 0.3-3.7 KB | c | Figures for a talk, not for the paper. |
| `anim_energize.py` | 3.0 KB | c | Animated GIF for the talk. |
| `old/` | 22 files, 88 KB | c | Superseded scripts from earlier iterations. |

## checks/

Everything in `checks/` is category **(c)** except where noted. 41 scripts, 0.1-7.2 KB each.

| File | Cat | Description |
|---|---|---|
| `bpt_distance.py` | b | Produces `plots/fig_bpt_distance.pdf` (mtime matches the current PDF). Also prints the SL-distance medians and p-values. |
| `bpt_distance_paper.py` | c | Near-identical earlier variant, writes a differently-named PNG. |
| `patch_lum_check.py` | c | **Rewrote the master file in place**, filling `log_L_radio` from `logL3` for the two NaN-Alpha sources. |
| `fix_two_missing.py` | c | Diagnostic for those same two sources. |
| `audit.py`, `audit_q.py`, `audit_stage1.py`, `audit_stage2.py` | c | Sample and jet-power audits. |
| `lum_check.py`, `lum_matched.py`, `lumcut_borderline.py`, `plot_lum_hist.py` | c | Luminosity cut checks and the cut histogram. |
| `w80_after_cut.py`, `w80_merge_check.py`, `w80_missing.py`, `mw_and_outliers.py`, `ad_test.py`, `tail_fraction.py` | c | W80 statistics checks. |
| `oi_flux_compare.py`, `oi_flux_coverage.py`, `check_total_flux.py` | c | [OI] flux sanity checks. |
| `render_vlass_cutouts.py`, `render_vlass_v2.py`, `render_vlass_v3.py`, `find_missing_cutouts.py`, `snr_at_center.py` | c | VLASS cutout rendering and QC. |
| `check_columns.py`, `check_new_small_columns.py`, `check_new_small_overlap.py`, `check_new_small_positions.py`, `check_new_small_sizes.py`, `inventory.py`, `compare_large_sets.py`, `removed_objects.py`, `find_sf_small.py`, `cut_large.py`, `cut_large2.py`, `cut_old_small.py` | c | Column, overlap and cut consistency checks. |
| `dig_39633413145101909.py`, `trace_extreme_objects.py` | c | Single-object deep dives. |

## plots/

All of `plots/` is category **(c)** — figures are outputs, not release data. The paper
figures themselves are the `fig_*.pdf` files; the scripts that make them are released, the
PDFs are not (they belong to the paper, not the dataset).

| File | Size | Description |
|---|---|---|
| `fig_bpt.pdf` | 22 KB | [OI] BPT diagram. Paper figure. |
| `fig_balmer.pdf` | 16 KB | Balmer decrement distributions. Paper figure. |
| `fig_bpt_distance.pdf` | 16 KB | Distance from the Seyfert/LINER line. Paper figure. |
| `fig_w80_bptdist.pdf` | 19 KB | W80 vs BPT distance. Paper figure. |
| `fig_loi_vs_q.pdf` | 18 KB | [OI] luminosity vs jet power. Paper figure. |
| `fig_oiii_nev.pdf` | 18 KB | [OIII]/Hb vs [NeV]/Hb. Paper figure. |
| `fig_oiii_oii.pdf` | 18 KB | [OIII] vs [OII]. Paper figure. |
| `fig_w80_by_class.pdf` | 14 KB | W80 by BPT class. Paper figure. |
| `fig_w80_nev_small.pdf` | 15 KB | W80 vs [NeV], small sample. Paper figure. |
| `fig_loi_vs_q_panels.pdf`, `fig_loiii_vs_q_panels.pdf` | ~16 KB | Panel variants, likely superseded. |
| `2026-*.png` (~40 files) | 15-160 KB | Dated PNG versions of the above, one per iteration. |
| `oiii_double_*.png` (24), `halpha_triple_*.png` (23), `hbeta_triple_*.png` (24), `oi_double_*.png` (24) | 25-63 KB each | Per-object fit QC panels for the new small sources. |
| `talk_*.png/.gif` (17) | 20-346 KB | Talk figures. |
| `candidates_sheet.png`, `energize_gas.gif` | 220 KB, 823 KB | Talk material. |
| `fit_qc/` | 421 files, 18 MB | Per-object fit QC panels from the original fitting run. |
| `vlass_qc_small/`, `vlass_qc_v2/`, `vlass_qc_v3/` | 48-49 files each, 3-6 MB | VLASS cutout QC renders, three passes. |
| `bpt_oi.png`, `bpt_oi_expanded.png`, `bpt_oi_lumcut.png`, `w80_by_class.png`, `w80_by_sample.png`, `w80_by_sample_expanded.png` | 33-66 KB | Undated early figures. |

## Project root

| File | Size | Cat | Description |
|---|---|---|---|
| `plot_balmer_decrement.py` | 2.5 KB | c | Root-level copy, **differs** from `scripts/plot_balmer_decrement.py`. The `scripts/` one is the later version and is the one released. |
| `plot_bpt_distance.py` | 1.8 KB | c | Root-level copy, byte-identical to `checks/bpt_distance_paper.py`. |
| `bpt_distance.py` | 0 B | c | Empty file. |
| `papers/` | 3 PDFs, 5.7 MB | d | Reference papers (Heckman & Best 2014, Kewley 2006, Molyneux 2019). Third-party, not redistributable. |

---

## Summary

- **Released (a):** 19 files. The single catalog CSV, rounded, plus README, columns.csv,
  LICENSE, MANIFEST.txt, CHECKSUMS.txt and 13 scripts. See `zenodo/upload/`.
- **Not released, kept locally (c):** all `notes/` intermediates, all `checks/`, all `plots/`.
  These are the provenance chain and can be supplied on request.
- **Never redistribute (d):** `data/spectra/` (DESI DR1 — point to SPARCL),
  `data/vlass_cutouts_small/` (VLASS images), the four source cross-match CSVs (they
  contain the full DESI DR1 and VLASS column sets rather than our measurements), and
  `papers/`.
