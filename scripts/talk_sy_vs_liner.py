import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 15})

sy_id = 39628085301085881
lin_id = 39627731247305171

zs = pd.read_csv('notes/targetid_redshift.csv')

def smooth(y, n=5):
    return np.convolve(y, np.ones(n) / n, mode='same')

fig, axes = plt.subplots(2, 2, figsize=(11, 6), sharex='col')

for row, (tid, label, color) in enumerate([(sy_id, 'SEYFERT', 'dimgray'),
                                           (lin_id, 'LINER', '#5B2C6F')]):
    spec = pd.read_csv(f'data/spectra/{tid}_desispec.csv')
    z = zs.loc[zs['TARGETID'] == tid].iloc[0, 1]
    wave = spec['Lambda'] / (1 + z)
    flux = smooth(spec['FLambda17'].values)
    for col, (lo, hi) in enumerate([(4830, 5060), (6250, 6620)]):
        sel = (wave > lo) & (wave < hi)
        axes[row, col].plot(wave[sel], flux[sel], 'k', lw=0.9)
        axes[row, col].set_yticks([])
    axes[row, 0].text(0.04, 0.82, label, transform=axes[row, 0].transAxes,
                      fontsize=18, color=color, weight='bold')

for col, marks in enumerate([{r'H$\beta$': 4861, '[OIII]': 5007},
                             {'[OI]': 6300, r'H$\alpha$': 6563}]):
    for row in [0, 1]:
        for name, lam in marks.items():
            axes[row, col].axvline(lam, color='gray', ls=':', lw=0.8)
        if row == 0:
            for name, lam in marks.items():
                axes[row, col].text(lam, axes[row, col].get_ylim()[1] * 0.97,
                                    name, ha='center', fontsize=14)

axes[1, 0].set_xlabel('rest wavelength (Angstrom)')
axes[1, 1].set_xlabel('rest wavelength (Angstrom)')
axes[0, 0].set_ylabel('brightness')
axes[1, 0].set_ylabel('brightness')
plt.tight_layout()
plt.savefig('plots/talk_sy_vs_liner.png', dpi=200)
print('saved plots/talk_sy_vs_liner.png')