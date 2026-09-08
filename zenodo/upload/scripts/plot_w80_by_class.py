import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp, mannwhitneyu

LARGE_COLOR = 'black'
SMALL_COLOR = '#5B2C6F'

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
print('matched:', len(m))

groups = [('small', 'seyfert'), ('small', 'liner'), ('large', 'seyfert')]
labels = ['small Seyfert', 'small LINER', 'large Seyfert']
data, names, box_sample = [], [], []
for (s, cl), lab in zip(groups, labels):
    vals = m[(m['sample'] == s) & (m['bpt_class'] == cl)]['w80']
    data.append(vals)
    names.append('%s (n=%d)' % (lab, len(vals)))
    box_sample.append(s)
    print(lab, len(vals), 'median', round(vals.median(), 1))

print('KS small Sy vs large Sy p =', round(ks_2samp(data[0], data[2]).pvalue, 4))
print('KS small Sy vs small LINER p =', round(ks_2samp(data[0], data[1]).pvalue, 4))
print('MW small Sy vs large Sy p =', mannwhitneyu(data[0], data[2]).pvalue)

fig, ax = plt.subplots(figsize=(7, 5))
bp = ax.boxplot(data, tick_labels=names, patch_artist=True, medianprops=dict(color='black'))
for patch, s in zip(bp['boxes'], box_sample):
    if s == 'large':
        patch.set_facecolor(LARGE_COLOR); patch.set_edgecolor(LARGE_COLOR); patch.set_alpha(0.85)
    else:
        patch.set_facecolor('white'); patch.set_edgecolor(SMALL_COLOR); patch.set_linewidth(1.5)
for flier, s in zip(bp['fliers'], box_sample):
    col = LARGE_COLOR if s == 'large' else SMALL_COLOR
    flier.set(markeredgecolor=col, markerfacecolor=col if s == 'large' else 'none', marker='o')

ax.set_ylabel('W80 (km/s)')
plt.tight_layout()
plt.savefig('plots/2026-08-12_w80_by_class.png', dpi=150)
plt.savefig('plots/fig_w80_by_class.pdf')
print('saved')