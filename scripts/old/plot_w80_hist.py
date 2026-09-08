import pandas as pd
import matplotlib.pyplot as plt

m = pd.read_csv('notes/2026-07-13_resolution_w80.csv')
lg = m[m['sample'] == 'large']['w80']
sm = m[m['sample'] == 'small']['w80']

plt.figure(figsize=(8, 5))
bins = range(0, 2200, 150)
plt.hist(sm, bins=bins, alpha=0.6, label='small (10-15 kpc), n=%d' % len(sm))
plt.hist(lg, bins=bins, alpha=0.6, label='large (>20 kpc), n=%d' % len(lg))
plt.axvline(sm.median(), color='C0', ls='--')
plt.axvline(lg.median(), color='C1', ls='--')
plt.xlabel('W80 (km/s)')
plt.ylabel('number of objects')
plt.legend()
plt.tight_layout()
plt.savefig('plots/w80_by_sample.png', dpi=150)
print('saved plots/w80_by_sample.png')