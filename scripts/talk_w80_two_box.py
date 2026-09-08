import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 18})

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

small_sy = m[(m['sample'] == 'small') & (m['bpt_class'] == 'seyfert')]['w80']
large_sy = m[(m['sample'] == 'large') & (m['bpt_class'] == 'seyfert')]['w80']
print('confined n =', len(small_sy), 'median', round(small_sy.median()))
print('escaped n =', len(large_sy), 'median', round(large_sy.median()))

fig, ax = plt.subplots(figsize=(8, 5.5))
bp = ax.boxplot([small_sy, large_sy],
                tick_labels=['confined\n(n=%d)' % len(small_sy), 'escaped\n(n=%d)' % len(large_sy)],
                widths=0.5, patch_artist=True, medianprops=dict(color='black'))
bp['boxes'][0].set_facecolor('plum')
bp['boxes'][1].set_facecolor('dimgray')
for flier in bp['fliers']:
    flier.set(marker='o', markeredgecolor='black', markerfacecolor='none')
ax.set_ylabel('gas speed, W80 (km/s)')
plt.tight_layout()
plt.savefig('plots/talk_w80_two_box.png', dpi=200)
print('saved plots/talk_w80_two_box.png')