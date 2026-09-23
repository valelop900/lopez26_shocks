import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.patches as mpatches
import paperstyle

# left panel is plot_bpt_lumcut_POSTEDIT_ML.py, right panel is checks/bpt_distance.py,
# plotting code copied in. both read the classification table the left script wrote.

LARGE_COLOR = 'black'
SMALL_COLOR = '#5B2C6F'

b = pd.read_csv('notes/2026-07-31_bpt_class_lumcut_v2.csv')
lum = pd.read_csv('notes/2026-07-28_luminosity_check.csv').drop_duplicates('TARGETID')[['TARGETID', 'Physical_Size', 'log_L_radio']]
df = b.merge(lum, on='TARGETID')
df = df[df['log_L_radio'] > 24]
df = df[(df['sample'] == 'small') | (df['Physical_Size'] > 25)]
print('objects:', len(df))

xv = df['log_oi_ha'].values
yv = df['log_oiii_hb'].values
samp = df['sample'].values
cls = df['bpt_class'].values

def kewley(x):
    return 0.73 / (x + 0.59) + 1.33
def syliner(x):
    return 1.18 * x + 1.30

fig, (ax, ax2) = plt.subplots(1, 2, figsize=paperstyle.TWO_PANEL)

# ---- BPT ----
ax.set_xlim(-2.5, 0.7)
ax.set_ylim(-1.2, 2.0)
styles = {
    ('large', 'seyfert'): ('large (>25 kpc) Seyfert', dict(marker='o', facecolors='black', edgecolors='black')),
    ('large', 'liner'):   ('large (>25 kpc) LINER', dict(marker='*', facecolors='black', edgecolors='black', s=140)),
    ('small', 'seyfert'): ('small (10-15 kpc) Seyfert', dict(marker='o', facecolors='none', edgecolors='#5B2C6F')),
    ('small', 'liner'):   ('small (10-15 kpc) LINER', dict(marker='*', facecolors='none', edgecolors='#5B2C6F', s=140)),
}
for (s_name, c_name), (lab, st) in styles.items():
    sel = (samp == s_name) & (cls == c_name)
    ax.scatter(xv[sel], yv[sel], label=lab, **st)
sf_sel = (samp == 'small') & (cls == 'sf')
if sf_sel.any():
    ax.scatter(xv[sf_sel], yv[sf_sel], marker='^', facecolors='none', edgecolors='#5B2C6F', label='small (10-15 kpc) SF')

xk = np.linspace(-2.5, -0.63, 100)
ax.plot(xk, kewley(xk), 'k-', lw=1)
xs = np.linspace(-1.12, 0.4, 50)
ax.plot(xs, syliner(xs), 'k--', lw=1)

xt = 0.2
yt = syliner(xt)
xh = -0.15
m2 = -1/1.18
c2 = yt - xt*m2
yh = m2*xh + c2
arrow = mpatches.FancyArrowPatch((xt, yt), (xh, yh), mutation_scale=20, color='r')
ax.add_patch(arrow)
ax.annotate('SL', xy=(xh, yh), xytext=(8, -2), textcoords='offset points', color='tab:red', fontweight='bold',
            path_effects=[pe.withStroke(linewidth=3, foreground='white')])
ax.text(0.25, 1.8, 'Seyfert')
ax.text(-0.5, 0.0, 'LINER')
ax.text(-2.2, -0.3, 'star forming')
ax.set_xlabel(r'log [O I] 6300 / H$\alpha$')
ax.set_ylabel(r'log [O III] 5007 / H$\beta$')
ax.legend(loc='lower right', fontsize=7, handletextpad=0.3, borderpad=0.4, labelspacing=0.3)

# ---- SL histogram ----
d = (df['log_oiii_hb'] - 1.18*df['log_oi_ha'] - 1.30) * np.cos(np.arctan(1.18))
lg = d[df['sample'] == 'large']
sm = d[df['sample'] == 'small']
print('histogram: large %d  small %d' % (len(lg), len(sm)))
bins = np.arange(-1.0, 1.4, 0.15)
ax2.hist(lg, bins=bins, weights=np.ones(len(lg))/len(lg), histtype='stepfilled',
         facecolor='0.8', edgecolor=LARGE_COLOR, linewidth=1.3, label='large (>25 kpc), n=%d' % len(lg))
ax2.hist(sm, bins=bins, weights=np.ones(len(sm))/len(sm), histtype='stepfilled',
         facecolor='none', edgecolor=SMALL_COLOR, hatch='\\\\\\\\', linewidth=1.3, label='small (10-15 kpc), n=%d' % len(sm))
ax2.axvline(0, color='k', ls='--')
ax2.set_xlabel('SL measure')
ax2.set_ylabel('fraction of sample')
ax2.legend()

plt.tight_layout()
plt.savefig('plots/fig_bpt_2panel.pdf')
plt.savefig('plots/fig_bpt_2panel.png', dpi=150)
print('saved plots/fig_bpt_2panel.pdf')
