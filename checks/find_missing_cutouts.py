import glob, os, re
import pandas as pd

df = pd.read_csv("data/VLASS3_2_OI_small.csv")
# the 'Name' column holds VLASS3.2SE Jxxxxxx names
csv_names = set()
for n in df["Name"].astype(str):
    m = re.search(r"(J\d{6}\.\d{2}[+-]\d{6}\.\d)", n)
    if m: csv_names.add(m.group(1))

files = glob.glob("data/vlass_cutouts_small/*.fits")
cut_names = set()
for f in files:
    m = re.search(r"(J\d{6}\.\d{2}[+-]\d{6}\.\d)", os.path.basename(f))
    if m: cut_names.add(m.group(1))

print("objects in CSV:", len(csv_names))
print("objects with cutouts:", len(cut_names))
print("\nin CSV but NO cutout:")
for n in sorted(csv_names - cut_names):
    print("  ", n)
