import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

LARGE_COLOR = 'black'
SMALL_COLOR = '#5B2C6F'
MARKERS = {'seyfert': ('o', 45), 'liner': ('*', 110), 'sf': ('^', 55)}

b = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
lum = pd.read_csv('notes/2026-07-28_luminosity_check.csv')[['TARGETID', 'Physical_Size', 'log_L_radio']]
df = b.merge(lum, on='TARGETID')

# lum cut plus new size cut, large now means > 25 kpc
df = df[df['log_L_radio'] > 24]
df = df[(df['sample'] == 'small') | (df['Physical_Size'] > 25)]

print(df.groupby('sample')['bpt_class'].value_counts())

x = np.linspace(-2.5, -0.6, 200)
sf = 0.73 / (x + 0.59) + 1.33
x2 = np.linspace(-1.12, 0.5, 200)
sy = 1.18 * x2 + 1.30

plt.figure(figsize=(8, 6))
plt.plot(x[x < -0.65], sf[x < -0.65], 'k-')
plt.plot(x2, sy, 'k--')

for s in ['large', 'small']:
    for cl in ['seyfert', 'liner', 'sf']:
        sub = df[(df['sample'] == s) & (df['bpt_class'] == cl)]
        if not len(sub):
            continue
        mk, ms = MARKERS[cl]
        if s == 'large':
            plt.scatter(sub['log_oi_ha'], sub['log_oiii_hb'], marker=mk, s=ms,
                        facecolors=LARGE_COLOR, edgecolors=LARGE_COLOR,
                        label='large %s (n=%d)' % (cl, len(sub)))
        else:
            plt.scatter(sub['log_oi_ha'], sub['log_oiii_hb'], marker=mk, s=ms,
                        facecolors='none', edgecolors=SMALL_COLOR, linewidths=1.3,
                        label='small %s (n=%d)' % (cl, len(sub)))

plt.xlabel('log [OI]6300 / Ha')
plt.ylabel('log [OIII]5007 / Hb')
plt.xlim(-2.5, 0.5)
plt.ylim(-1.5, 2.2)
plt.text(-2.3, 1.6, 'Seyfert')
plt.text(-2.3, -0.8, 'star forming')
plt.text(-0.4, 0.0, 'LINER')
plt.legend(fontsize=8, loc='lower left')
plt.tight_layout()
plt.savefig('plots/fig_bpt.pdf')
plt.savefig('plots/2026-08-12_bpt_25kpc.png', dpi=150)
print('saved plots/2026-08-12_bpt_25kpc.png')