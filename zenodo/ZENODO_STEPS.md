# Making the draft deposit

Valeria owns the deposit, Mark is the second creator. Everything below is done in a browser
on zenodo.org. Nothing here has been done yet: no account, no token, no upload.

Do not press Publish. The record stays a draft until Mark signs off.

1. Sign in at https://zenodo.org. Use the ORCID login for 0009-0009-0998-5049 so the account
   is tied to the right ORCID from the start. Whoever logs in owns the record, and ownership
   cannot be transferred later without asking Zenodo support.

2. Click New upload. This creates a draft. Drafts are private, are not indexed, and can be
   edited or deleted freely.

3. Upload `zenodo/lopez_lacy_2026_release_draft.zip`. Wait for the transfer to finish before
   editing any fields. The zip is used because the web uploader does not preserve folder
   structure, and the README refers to the scripts as `scripts/...`.

4. Click Reserve DOI, in the Basic information section. Zenodo hands back a real DOI
   (`10.5281/zenodo.XXXXXXX`) immediately, while the record is still an unpublished draft.
   Copy it. It replaces "doi to be added after review" in the manuscript. Do not wait for
   acceptance to do this.

5. Resource type: Dataset. Access: Open.

6. Title:
   Measurement tables for "Evidence for strong shocks in the ISM of small radio sources"

7. Creators, in this order, entered as `Family name, Given name`:
   - Lopez, Valeria — ORCID 0009-0009-0998-5049 — National Radio Astronomy Observatory,
     520 Edgemont Road, Charlottesville, VA 22903, USA
   - Lacy, Mark — ORCID 0000-0002-3032-1783 — same affiliation

   Paste the bare ORCID, not the full URL. Drag the rows so the order matches the paper.

8. Description: paste the text of `zenodo/description_for_zenodo.txt`.

9. License: Creative Commons Attribution 4.0 International (CC BY 4.0).

10. Keywords, one per line:
    Active galactic nuclei (16)
    Radio jets (1347)
    AGN host galaxies (2017)
    shocks
    interstellar medium
    emission line galaxies
    VLASS
    DESI
    spectroscopy
    BPT diagram

11. Related works: the paper goes here as "is supplement to", identifier type DOI. The ApJL
    DOI does not exist yet, so leave this entry out for now.

12. Language: English. Version: 1.0.0.

13. Click Save. Do not click Publish.

14. Verify the upload: download the zip back from the draft and run `shasum -a 256 -c
    CHECKSUMS.txt` inside it. Zenodo shows an MD5 per file, not SHA-256, so checking by eye
    on the web page is not enough.

15. Send Mark the reserved DOI and the draft link.

`zenodo/metadata.json` holds the same fields in the format Zenodo's REST API expects, if the
deposit is ever made from a script instead of the web form.

# After the paper is accepted

1. Add the ApJL DOI as the Related works entry from step 11, and put it in the
   `related_identifiers` block of `zenodo/metadata.json`.
2. Confirm the reserved DOI printed in the manuscript matches the one on the record.
3. Get Mark's go-ahead, then Publish.

Publishing is irreversible. The record becomes public permanently, the DOI is minted for
good, and files can no longer be changed. The only way to alter files afterwards is New
version, which mints a new version DOI and leaves the old one live. Zenodo also keeps a
concept DOI that always resolves to the newest version; cite that one in the paper if
revisions are likely.
