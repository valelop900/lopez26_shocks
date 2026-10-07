import hashlib
import os
import zipfile

# Writes CHECKSUMS.txt, MANIFEST.txt and the release zip from one file list, so the three
# can never disagree about what is in the archive. Dotfiles are skipped, which is what
# keeps Finder's .DS_Store out. Runs from anywhere; paths are taken from this file.

desc = {
    'catalog_lopez_lacy_2026.csv': 'The release table. 77 rows keyed by TARGETID, 45 small then 32 large, 36 columns.',
    'columns.csv': 'Name, unit, dtype, description and source for every column of the release table.',
    'README.md': 'Description of the release, sample definitions, column notes, and how each number in the paper maps to the columns.',
    'LICENSE': 'Creative Commons Attribution 4.0 International, full legal text.',
    'CHECKSUMS.txt': 'SHA-256 of every file in this archive except itself and MANIFEST.txt.',
    'scripts/make_release_tables.py': 'Applies release rounding, adds the fitted line fluxes, and writes the release table.',
    'scripts/check_release.py': 'Recomputes every number quoted in the paper from the release table alone.',
    'scripts/jet_power.py': 'Jet power from the VLASS flux density following Willott et al. (1999). Writes the logQ table that plot_loi_vs_q.py reads.',
    'scripts/plot_bpt.py': 'The [OI] BPT diagram, single panel. Also writes the BPT classification table the other scripts read.',
    'scripts/paperstyle.py': 'Shared matplotlib settings and figure sizes used by the figure scripts.',
    'scripts/fig_bpt_2panel.py': 'fig_bpt_2panel.pdf, the BPT diagram and the SL histogram side by side.',
    'scripts/fig_w80_2panel.py': 'fig_w80_2panel.pdf, W80 by class and W80 against SL side by side.',
    'scripts/oiii_profiles.py': 'fig_oiii_profiles.pdf, [OIII] profiles of the broadest small sources with their fits. Needs the DESI spectra.',
    'scripts/fig_examples.py': 'fig_examples.pdf, one small and one large source with VLASS contours on Legacy Survey images. Fetches the cutouts online.',
    'scripts/plot_loi_vs_q.py': 'fig_loi_vs_q.pdf, [OI] luminosity against jet power.',
}

zenodo = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.join(zenodo, 'upload'))

files = []
skipped = []
for root, dirs, names in os.walk('.'):
    dirs[:] = sorted(d for d in dirs if not d.startswith('.'))
    for n in sorted(names):
        f = os.path.relpath(os.path.join(root, n), '.')
        if n.startswith('.'):
            skipped.append(f)
        else:
            files.append(f)
files.sort()

# the two generated files belong in the archive whether or not they exist yet
listed = [f for f in files if f not in ('CHECKSUMS.txt', 'MANIFEST.txt')]
files = sorted(listed + ['CHECKSUMS.txt', 'MANIFEST.txt'])

sha = {}
for f in listed:
    sha[f] = hashlib.sha256(open(f, 'rb').read()).hexdigest()

out = open('CHECKSUMS.txt', 'w')
for f in listed:
    out.write('%s  %s\n' % (sha[f], f))
out.close()

# CHECKSUMS.txt is hashed after it is written, so MANIFEST covers it; MANIFEST leaves out
# only itself, whose own hash would change as it is written.
sha['CHECKSUMS.txt'] = hashlib.sha256(open('CHECKSUMS.txt', 'rb').read()).hexdigest()

out = open('MANIFEST.txt', 'w')
out.write('MANIFEST for the Lopez & Lacy (2026) data release\n')
out.write('One block per file: size in bytes, SHA-256, and what it is.\n')
out.write('MANIFEST.txt is not listed here because its own hash would change as it is written.\n\n')
for f in files:
    if f == 'MANIFEST.txt':
        continue
    if f not in desc:
        raise SystemExit('no description for ' + f)
    out.write('%s\n  size    %d bytes\n  sha256  %s\n  %s\n\n'
              % (f, os.path.getsize(f), sha[f], desc[f]))
out.close()

z = zipfile.ZipFile(os.path.join(zenodo, 'lopez_lacy_2026_release_draft.zip'), 'w',
                    zipfile.ZIP_DEFLATED)
for f in files:
    z.write(f, f)
z.close()

print('archive files:', len(files))
print('CHECKSUMS.txt lists:', len(listed))
print('MANIFEST.txt lists:', len(files) - 1)
print('zip entries:', len(files))
print('dotfiles skipped:', skipped)
