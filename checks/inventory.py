import glob
import os

print('================ PYTHON FILES ================')
for f in sorted(glob.glob('*.py')):
    size = os.path.getsize(f)
    with open(f) as fh:
        lines = fh.readlines()
    # grab reads, writes, and savefig lines so we can see what each script touches
    inputs = [l.strip() for l in lines if 'read_csv' in l or 'open(' in l]
    outputs = [l.strip() for l in lines if 'to_csv' in l or 'savefig' in l]
    print(f, '|', len(lines), 'lines |', size, 'bytes')
    for l in inputs[:4]:
        print('   IN :', l[:100])
    for l in outputs[:4]:
        print('   OUT:', l[:100])
    print()

print('================ OTHER FILES IN PROJECT ROOT ================')
for f in sorted(os.listdir('.')):
    if not f.endswith('.py') and os.path.isfile(f):
        print(f, os.path.getsize(f), 'bytes')

print()
print('================ NOTES ================')
for f in sorted(os.listdir('notes')):
    print('notes/' + f)

print()
print('================ PLOTS ================')
for f in sorted(os.listdir('plots')):
    print('plots/' + f)

print()
print('================ DATA ================')
for f in sorted(os.listdir('data')):
    print('data/' + f)
