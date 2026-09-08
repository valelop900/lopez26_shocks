import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('notes/2026-07-28_luminosity_check.csv')
cut = df[df['log_L_radio'] > 24]

lg = cut[cut['sample'] == 'large']['w80']
sm = cut[cut['sample'] == 'small']['w80']

bins = np.arange(150, 1900, 125)

plt.figure(figsize=(7, 5))
plt.hist(sm, bins=bins, weights=np.ones(len(sm))/len(sm), alpha=0.6,
         color='tab:blue', label='small (10-15 kpc), n=%d' % len(sm))
plt.hist(lg, bins=bins, weights=np.ones(len(lg))/len(lg), alpha=0.6,
         color='tab:orange', label='large (>20 kpc), n=%d' % len(lg))
plt.axvline(sm.median(), ls='--', color='tab:blue')
plt.axvline(lg.median(), ls='--', color='tab:orange')
plt.xlabel('W80 (km/s)')
plt.ylabel('fraction of sample')
plt.title('W80 after luminosity cut (normalised to fraction)')
plt.legend()
plt.tight_layout()
plt.savefig('plots/2026-07-31_w80_by_sample_cut_norm.png', dpi=150)
print('small median %.0f  large median %.0f' % (sm.median(), lg.median()))
