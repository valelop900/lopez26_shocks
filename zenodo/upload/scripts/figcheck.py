import numpy as np
import matplotlib.transforms as mtrans

# legend and label placement that is checked against the plotted data.
# overlaps(ax, bbox) counts scatter points, line vertices (segments sampled), and patches
# (histogram bars, boxes) that fall inside a display-space bbox, with a 4 pt margin for the
# marker size. anything outside the axis limits is clipped and does not count.
# place_legend tries the four corners, then below the axes. place_text tries the candidate
# positions given, in order.

MARGIN_PT = 4

def _bbox_px(ax, artist):
    fig = ax.figure
    fig.canvas.draw()
    bb = artist.get_window_extent(fig.canvas.get_renderer())
    m = MARGIN_PT * fig.dpi / 72
    return mtrans.Bbox([[bb.x0 - m, bb.y0 - m], [bb.x1 + m, bb.y1 + m]])

def _inside(ax, xy):
    x0, x1 = sorted(ax.get_xlim()); y0, y1 = sorted(ax.get_ylim())
    return (xy[:, 0] >= x0) & (xy[:, 0] <= x1) & (xy[:, 1] >= y0) & (xy[:, 1] <= y1)

def overlaps(ax, bb, skip=()):
    n = 0
    tr = ax.transData
    for c in ax.collections:
        off = np.asarray(c.get_offsets())
        off = off[_inside(ax, off)] if len(off) else off
        if len(off):
            p = tr.transform(off)
            n += int(np.sum((p[:, 0] >= bb.x0) & (p[:, 0] <= bb.x1) & (p[:, 1] >= bb.y0) & (p[:, 1] <= bb.y1)))
    for l in ax.lines:
        xy = np.asarray(l.get_xydata())
        if len(xy) < 2 or not l.get_visible():
            continue
        if len(xy) < 50:
            xy = np.vstack([np.column_stack([np.linspace(a[0], b[0], 50), np.linspace(a[1], b[1], 50)])
                            for a, b in zip(xy[:-1], xy[1:])])
        xy = xy[_inside(ax, xy)]
        p = tr.transform(xy)
        n += int(np.sum((p[:, 0] >= bb.x0) & (p[:, 0] <= bb.x1) & (p[:, 1] >= bb.y0) & (p[:, 1] <= bb.y1)))
    for pa in ax.patches:
        if pa in skip:
            continue
        pb = pa.get_window_extent(ax.figure.canvas.get_renderer())
        if pb.width == 0 or pb.height == 0:
            continue
        if pb.overlaps(bb):
            n += 1
    return n

def place_legend(ax, name, **kw):
    kw.setdefault('markerscale', 1)
    for loc in ['upper right', 'upper left', 'lower left', 'lower right']:
        leg = ax.legend(loc=loc, **kw)
        n = overlaps(ax, _bbox_px(ax, leg))
        if n == 0:
            print('%s: legend %s, overlap %d' % (name, loc, n))
            return leg
    # one column under a single-column figure, two under a double
    ncol = 2 if ax.figure.get_figwidth() > 5 else 1
    leg = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=ncol, **kw)
    bb = _bbox_px(ax, leg)
    n = overlaps(ax, bb)
    print('%s: legend below axes, overlap %d' % (name, n))
    return leg

def place_text(ax, name, label, candidates, **kw):
    for x, y in candidates:
        t = ax.text(x, y, label, **kw)
        n = overlaps(ax, _bbox_px(ax, t))
        if n == 0:
            print('%s: "%s" at (%.2f, %.2f), overlap %d' % (name, label, x, y, n))
            return t
        t.remove()
    t = ax.text(*candidates[-1], label, **kw)
    print('%s: "%s" at (%.2f, %.2f), overlap %d  NO CLEAR SPOT' % (name, label, candidates[-1][0], candidates[-1][1], overlaps(ax, _bbox_px(ax, t))))
    return t
