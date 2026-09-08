import pandas as pd
from scipy.stats import ks_2samp

w = pd.read_csv("notes/2026-07-13_resolution_w80.csv")
b = pd.read_csv("notes/2026-07-16_bpt_class.csv")

m = w.merge(b[["TARGETID", "bpt_class"]], on="TARGETID")
print("objects with both W80 and BPT class:", len(m))
print()
print("median W80 by sample and class:")
print(m.groupby(["bpt_class", "sample"])["w80"].agg(["size", "median"]).round(1))
print()

# small vs large among seyferts only
sy = m[m["bpt_class"] == "seyfert"]
a = sy[sy["sample"] == "large"]["w80"]
s = sy[sy["sample"] == "small"]["w80"]
if len(a) > 3 and len(s) > 3:
    print("seyferts only: large", len(a), "median", round(a.median(), 1),
          "| small", len(s), "median", round(s.median(), 1))
    print("KS p =", round(ks_2samp(a, s).pvalue, 4))
print()

# seyfert vs liner within the small sample
sm = m[m["sample"] == "small"]
sy2 = sm[sm["bpt_class"] == "seyfert"]["w80"]
li2 = sm[sm["bpt_class"] == "liner"]["w80"]
if len(li2) > 3:
    print("small sample, seyfert vs liner:")
    print("seyfert", len(sy2), "median", round(sy2.median(), 1),
          "| liner", len(li2), "median", round(li2.median(), 1))
    print("KS p =", round(ks_2samp(sy2, li2).pvalue, 4))