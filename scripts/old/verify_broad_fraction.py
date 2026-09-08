import pandas as pd

fits = pd.read_csv("notes/2026-07-08_oiii_fits.csv")
large = pd.read_csv("data/OI_sample_large.csv")
small = pd.read_csv("data/OI_sample_small.csv")

large_ids = set(large["TARGETID"])
small_ids = set(small["TARGETID"])

# check every fitted object belongs to exactly one sample
in_l = fits["TARGETID"].isin(large_ids)
in_s = fits["TARGETID"].isin(small_ids)
print("total fitted:", len(fits))
print("matched to large:", in_l.sum())
print("matched to small:", in_s.sum())
print("in both:", (in_l & in_s).sum())
print("in neither:", (~in_l & ~in_s).sum())

# check how the counts change with the no-broad cutoff
for cut in [0.5, 1.0, 2.0]:
    nb = fits["oiii_broad_amp"] < cut
    l = (nb & in_l).sum()
    s = (nb & in_s).sum()
    print("cutoff", cut, ": large", l, "of", in_l.sum(), ", small", s, "of", in_s.sum())