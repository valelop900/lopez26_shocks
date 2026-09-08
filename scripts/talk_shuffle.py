import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 18})
rng = np.random.default_rng(42)

w1 = pd.read_csv('notes/2026-07-13_resolution_w80.csv')
w2 = pd.read_csv('notes/2026-07-22_w80_new_large.csv')
w3 = pd.read_csv('notes/2026-07-31_w80_new_small24.csv')
w = pd.concat([w1, w2, w3], ignore_index=True)

bpt = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
size = pd.read_csv('notes/2026-07-28_luminosity_check.csv')[['TARGETID', 'Physical_Size', 'log_L_radio']]

m = w.merge(bpt[['TARGETID', 'bpt_class', 'sample']], on='TARGETID', suffixes=('_w', ''))
m = m.merge(size, on='TARGETID')
m = m[m['log_L_radio'] > 24]
m = m[(m['sample'] == 'small') | (m['Physical_Size'] > 25)]

sy = m[m['bpt_class'] == 'seyfert']
small_sy = sy[sy['sample'] == 'small']['w80'].values
large_sy = sy[sy['sample'] == 'large']['w80'].values

obs = np.median(small_sy) - np.median(large_sy)
print('observed median difference:', round(obs))

both = np.concatenate([small_sy, large_sy])
n_small = len(small_sy)

diffs = []
for i in range(10000):
    rng.shuffle(both)
    diffs.append(np.median(both[:n_small]) - np.median(both[n_small:]))
diffs = np.array(diffs)

print('shuffle p:', (np.abs(diffs) >= abs(obs)).mean())

xlim = (min(diffs.min(), obs) - 40, max(diffs.max(), obs) + 40)

def base():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    ax.hist(diffs, bins=60, color='dimgray', alpha=0.8)
    ax.text(0, ax.get_ylim()[1] * 0.6, '10,000 shuffles:\nwhat luck alone produces',
            ha='center', color='dimgray', fontsize=18)
    ax.set_xlabel('confined minus escaped, median W80 (km/s)')
    ax.set_yticks([])
    ax.set_xlim(xlim)
    return fig, ax

fig, ax = base()
plt.tight_layout()
plt.savefig('plots/talk_shuffle_1.png', dpi=200)
plt.close()

fig, ax = base()
ax.axvline(obs, color='#5B2C6F', lw=3)
ax.annotate('the real data', xy=(obs, ax.get_ylim()[1] * 0.15),
            xytext=(obs - 60, ax.get_ylim()[1] * 0.45),
            ha='right', color='#5B2C6F', fontsize=20,
            arrowprops=dict(arrowstyle='->', color='#5B2C6F', lw=2))
plt.tight_layout()
plt.savefig('plots/talk_shuffle_2.png', dpi=200)
print('saved talk_shuffle_1.png and talk_shuffle_2.png')