import pandas as pd
import numpy as np

large = pd.read_csv("data/OI_sample_large.csv")
small = pd.read_csv("data/OI_sample_small.csv")
both = pd.concat([large, small])

good = [int(line.strip()) for line in open("notes/2026-07-07_good_targetids.txt")]
both = both[both["TARGETID"].isin(good)]

snr = both["OI_6300_FLUX"] * np.sqrt(both["OI_6300_FLUX_IVAR"])

print("objects:", len(both))
print("catalog OI snr > 5:", (snr > 5).sum())
print("catalog OI snr 3-5:", ((snr > 3) & (snr <= 5)).sum())
print("catalog OI snr < 3:", (snr <= 3).sum())
print()
print("lowest ten:")
out = both[["TARGETID"]].copy()
out["oi_snr"] = snr.values
print(out.sort_values("oi_snr").head(10).to_string(index=False))