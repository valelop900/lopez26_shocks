import numpy as np
import pandas as pd

targets = [39633413145101909, 39628159028563219]

def flux(amp, sig, lam0):
    return amp * sig * lam0

oiii = pd.concat([pd.read_csv('notes/2026-07-08_oiii_fits.csv'),
                  pd.read_csv('notes/2026-07-22_oiii_fits_new_large.csv'),
                  pd.read_csv('notes/2026-07-31_oiii_fits_new_small24.csv')], ignore_index=True)
oi = pd.concat([pd.read_csv('notes/2026-07-09_oi_fits.csv'),
                pd.read_csv('notes/2026-07-22_oi_fits_new_large.csv'),
                pd.read_csv('notes/2026-07-31_oi_fits_new_small24.csv')], ignore_index=True)
hb = pd.concat([pd.read_csv('notes/2026-07-15_hbeta_fits.csv'),
                pd.read_csv('notes/2026-07-22_hbeta_fits_new_large.csv'),
                pd.read_csv('notes/2026-07-31_hbeta_fits_new_small24.csv')], ignore_index=True)
ha = pd.concat([pd.read_csv('notes/2026-07-16_halpha_fits.csv'),
                pd.read_csv('notes/2026-07-22_halpha_fits_new_large.csv'),
                pd.read_csv('notes/2026-07-31_halpha_fits_new_small24.csv')], ignore_index=True)

w1 = pd.read_csv('notes/2026-07-13_resolution_w80.csv')
w2 = pd.read_csv('notes/2026-07-22_w80_new_large.csv')
w3 = pd.read_csv('notes/2026-07-31_w80_new_small24.csv')

bpt = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
lum = pd.read_csv('notes/2026-07-28_luminosity_check.csv')

for t in targets:
    print('=' * 60)
    print('TARGETID', t)

    for name, wf in [('w80 2026-07-13', w1), ('w80 2026-07-22 large', w2), ('w80 2026-07-31 small24', w3)]:
        hit = wf[wf['TARGETID'] == t]
        if len(hit):
            print('  in %s: w80 = %.0f km/s' % (name, hit['w80'].iloc[0]))

    for name, tab, cols in [
        ('oiii', oiii, ('oiii_narrow_amp', 'oiii_narrow_sigma_kms', 'oiii_broad_amp', 'oiii_broad_sigma_kms', 5006.8)),
        ('oi', oi, ('oi_narrow_amp', 'oi_narrow_sigma_kms', 'oi_broad_amp', 'oi_broad_sigma_kms', 6300.3)),
        ('hb', hb, ('hb_narrow_amp', 'hb_narrow_sigma_kms', 'hb_broad_amp', 'hb_broad_sigma_kms', 4861.3)),
        ('ha', ha, ('ha_narrow_amp', 'ha_narrow_sigma_kms', 'ha_broad_amp', 'ha_broad_sigma_kms', 6562.8))]:
        hit = tab[tab['TARGETID'] == t]
        if len(hit) == 0:
            print('  %s fits: NOT PRESENT in any fits file' % name)
        else:
            r = hit.iloc[0]
            f = flux(r[cols[0]], r[cols[1]], cols[4]) + flux(r[cols[2]], r[cols[3]], cols[4])
            print('  %s fits: present, total flux (amp*sig*lam0 convention) = %.3g %s'
                  % (name, f, '(POSITIVE)' if f > 0 else '<-- NOT positive, fails BPT cut'))

    hit = lum[lum['TARGETID'] == t]
    if len(hit):
        r = hit.iloc[0]
        print('  luminosity file: sample=%s size=%.1f kpc logL=%.2f  (logL>24 cut: %s)'
              % (r.get('sample', '?'), r['Physical_Size'], r['log_L_radio'],
                 'PASS' if r['log_L_radio'] > 24 else 'FAIL'))
    else:
        print('  luminosity file: NOT PRESENT')

    hit = bpt[bpt['TARGETID'] == t]
    if len(hit):
        r = hit.iloc[0]
        print('  bpt_class_lumcut_v2: present, sample=%s class=%s' % (r['sample'], r['bpt_class']))
    else:
        print('  bpt_class_lumcut_v2: NOT PRESENT  <-- excluded from classified sample')
