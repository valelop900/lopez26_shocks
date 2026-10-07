import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import paperstyle

# makes fig_w80_2panel.pdf: W80 by sample and class, and W80 against the SL measure.
# reads the W80, classification and luminosity tables in notes/. run from the project root.

LARGE_COLOR = 'black'
SMALL_COLOR = '#5B2C6F'
LABELS = {'seyfert': 'Seyfert', 'liner': 'LINER'}
SAMPLE = {'large': 'large (>25 kpc)', 'small': 'small (10-15 kpc)'}
S = paperstyle.S2

w1 = pd.read_csv('notes/2026-07-13_resolution_w80.csv')
w2 = pd.read_csv('notes/2026-07-22_w80_new_large.csv')
w3 = pd.read_csv('notes/2026-07-31_w80_new_small24.csv')
w = pd.concat([w1, w2, w3], ignore_index=True)

bpt = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
size = pd.read_csv('notes/2026-07-28_luminosity_check.csv')[['TARGETID', 'Physical_Size', 'log_L_radio']]

m = w.merge(bpt, on='TARGETID', suffixes=('_w', ''))
m = m.merge(size, on='TARGETID')
m = m[m['log_L_radio'] > 24]
m = m[(m['sample'] == 'small') | (m['Physical_Size'] > 25)]
print('matched:', len(m), ' max small W80: %.1f' % m[m['sample'] == 'small']['w80'].max())

fig, (ax, ax2) = plt.subplots(1, 2, figsize=paperstyle.TWO_PANEL)

# ---- box plot ----
groups = [('small', 'seyfert'), ('small', 'liner'), ('large', 'seyfert')]
data, names, box_sample = [], [], []
for s, cl in groups:
    vals = m[(m['sample'] == s) & (m['bpt_class'] == cl)]['w80']
    data.append(vals)
    names.append('%s\n%s\n%s (n=%d)' % (SAMPLE[s].split(' (')[0], '(' + SAMPLE[s].split(' (')[1], LABELS[cl], len(vals)))
    box_sample.append(s)
bp = ax.boxplot(data, tick_labels=names, patch_artist=True, medianprops=dict(color='black'))
for patch, s in zip(bp['boxes'], box_sample):
    if s == 'large':
        patch.set_facecolor(LARGE_COLOR); patch.set_edgecolor(LARGE_COLOR); patch.set_alpha(0.85)
    else:
        patch.set_facecolor('white'); patch.set_edgecolor(SMALL_COLOR); patch.set_linewidth(1.0)
for flier, s in zip(bp['fliers'], box_sample):
    col = LARGE_COLOR if s == 'large' else SMALL_COLOR
    flier.set(markeredgecolor=col, markerfacecolor=col if s == 'large' else 'none', marker='o', markersize=5)
ax.set_ylabel(r'[O III] W80 (km s$^{-1}$)')
print('box: max small W80 plotted %.1f' % max(data[0].max(), data[1].max()))

# ---- W80 vs SL ----
m['bpt_dist'] = (m['log_oiii_hb'] - 1.18 * m['log_oi_ha'] - 1.30) / np.sqrt(1.18**2 + 1)
for s, cl, mk in [('large', 'seyfert', 'o'), ('large', 'liner', '*'),
                  ('small', 'seyfert', 'o'), ('small', 'liner', '*')]:
    sub = m[(m['sample'] == s) & (m['bpt_class'] == cl)]
    if s == 'large':
        ax2.scatter(sub['bpt_dist'], sub['w80'], marker=mk, color=LARGE_COLOR,
                    s=S[mk], label='%s %s' % (SAMPLE[s], LABELS[cl]))
    else:
        ax2.scatter(sub['bpt_dist'], sub['w80'], marker=mk, facecolors='none',
                    edgecolors=SMALL_COLOR, s=S[mk], linewidths=1.0, label='%s %s' % (SAMPLE[s], LABELS[cl]))
ax2.axvline(0, color='gray', ls=':')
ax2.set_xlabel('SL measure')
ax2.set_ylabel(r'[O III] W80 (km s$^{-1}$)')
ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=2)
print('scatter points:', sum(len(m[(m['sample'] == s) & (m['bpt_class'] == cl)]) for s in ['large', 'small'] for cl in ['seyfert', 'liner']), '(sf not plotted)',
      ' max small W80 plotted %.1f' % m[(m['sample'] == 'small') & (m['bpt_class'] != 'sf')]['w80'].max())

plt.tight_layout()
plt.savefig('plots/fig_w80_2panel.pdf')
plt.savefig('plots/fig_w80_2panel.png', dpi=paperstyle.PNG_DPI)
print('saved plots/fig_w80_2panel.pdf')
