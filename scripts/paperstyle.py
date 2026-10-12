# shared style for the paper figures
import matplotlib as mpl

mpl.rcParams['font.size'] = 9
mpl.rcParams['axes.labelsize'] = 9
mpl.rcParams['axes.titlesize'] = 9
mpl.rcParams['xtick.labelsize'] = 8
mpl.rcParams['ytick.labelsize'] = 8
mpl.rcParams['legend.fontsize'] = 8
mpl.rcParams['legend.markerscale'] = 1
mpl.rcParams['legend.handlelength'] = 1.5
mpl.rcParams['legend.handletextpad'] = 0.4
mpl.rcParams['legend.borderpad'] = 0.4
mpl.rcParams['legend.labelspacing'] = 0.3
mpl.rcParams['axes.linewidth'] = 0.8
mpl.rcParams['lines.linewidth'] = 1.0
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.major.size'] = 3
mpl.rcParams['ytick.major.size'] = 3
mpl.rcParams['xtick.major.width'] = 0.8
mpl.rcParams['ytick.major.width'] = 0.8
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['savefig.bbox'] = 'tight'

# inches. two-panel figures span both columns, one-panel fits one column
TWO_PANEL = (7.0, 3.5)
ONE_PANEL = (3.5, 3.2)

# marker areas (points^2). circles at markersize 5 / 4, stars twice that so they read the same
S2 = {'o': 25, '*': 50, '^': 25}
S1 = {'o': 16, '*': 32, '^': 16}
PNG_DPI = 300

# axis label and tick label sizes, two-panel figures and the single-column one
LABEL2, TICK2 = 14, 12
LABEL1, TICK1 = 11, 10
