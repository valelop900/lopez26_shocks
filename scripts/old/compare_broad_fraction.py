import pandas as pd

fits = pd.read_csv("notes/2026-07-08_oiii_fits.csv")
large = pd.read_csv("data/OI_sample_large.csv")
small = pd.read_csv("data/OI_sample_small.csv")

# no broad component = broad amplitude near zero
fits["no_broad"] = fits["oiii_broad_amp"] < 1

large_ids = set(large["TARGETID"])
small_ids = set(small["TARGETID"])

in_large = fits[fits["TARGETID"].isin(large_ids)]
in_small = fits[fits["TARGETID"].isin(small_ids)]

print("large sample:", in_large["no_broad"].sum(), "of", len(in_large), "have no broad component")
print("small sample:", in_small["no_broad"].sum(), "of", len(in_small), "have no broad component")

# see which ones
print()
print("large, no broad:")
print(in_large[in_large["no_broad"]]["TARGETID"].to_string(index=False))
print("small, no broad:")
print(in_small[in_small["no_broad"]]["TARGETID"].to_string(index=False))