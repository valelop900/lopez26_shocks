import pandas as pd

large = "/Users/valeria/Desktop/nrao_project/notes/2026-07-07_cutout_QC_large_final.txt"
small = "/Users/valeria/Desktop/nrao_project/notes/2026-07-07_cutout_QC_small.txt"

good_ids = []

for path in [large, small]:
    for line in open(path):
        fields = [x.strip() for x in line.split("|")]
        if len(fields) != 6:
            continue
        verdict = fields[4]
        targetid = fields[3]
        if verdict == "good":
            good_ids.append(targetid)

print("good objects:", len(good_ids))

out = "/Users/valeria/Desktop/nrao_project/notes/2026-07-07_good_targetids.txt"
f = open(out, "w")
for t in good_ids:
    f.write(t + "\n")
f.close()

print("saved to", out)