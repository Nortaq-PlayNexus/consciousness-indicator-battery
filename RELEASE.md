Add Zenodo release checksums and the manual-upload boundary

Records the verified archive SHA-256 and the CI run that validated this commit,
so the Zenodo upload step has a fixed value to check the upload against. Zenodo
files are immutable after publication: if the wrong archive is uploaded, the
only remedy is a new version.

Documents the boundary explicitly. Everything in this repository that can be
done non-interactively has been. Minting a Zenodo DOI requires an authenticated
session at zenodo.org with the GitHub repository attached, so it cannot be
scripted from here -- that step is the user's, and it is the last one.

Do NOT auto-publish on the next run without checking with me first.
## Verified state at time of writing

| | |
|---|---|
| GitHub | public, CI green 7/7 jobs on every push |
| Archive | `zenodo/consciousness-indicator-battery-v1.0.0.zip` |
| Size | 107,535 bytes (39 files) |
| SHA-256 | `14abcd585432418e99a206026d37d41eb75e328701b32c6a53940797203725ee` |
| Result hash EXP-C001 | `b953b8178354f0480257d9e684519782982da05207086c1e3491298d78133c16` |
| Result hash EXP-C003 | `1249a0ac9091ec2d4448118fb07bd8e260952d095843f4a56903ec66b50be56e` |
| Tests | 48 passing (1 skipped: lab-engine parity, standalone checkout) |
| flake8 | exit 0 |
| Clean room | passed |
| DOI | **10.5281/zenodo.23111535** (v2.0.0) - published 2026-10-03. Superseded; see current version below. |
| Concept DOI | **10.5281/zenodo.23101902** - shared by every version |
| v1 DOI | 10.5281/zenodo.23101903 - published 2026-10-02, still citable |

## Publication: COMPLETE — two versions

| | Version | DOI | Note |
|---|---|---|---|
| v1.0.0 | 2026-10-02 | `10.5281/zenodo.23101903` | superseded on metadata; still citable |
| **v2.0.0** | **2026-10-03** | **`10.5281/zenodo.23111535`** | **cite this one** |

Both share concept DOI `10.5281/zenodo.23101902`. The v2 record resolves without
authentication:

    https://doi.org/10.5281/zenodo.23111535

v2 is a **metadata-only** correction. The scientific content, code, archive
contents and results are identical to v1.

### What v2 fixed

- **References.** v1 published 722 array entries of one character each instead of
  four citations, because the source metadata held them as a single concatenated
  string and Zenodo iterated it into characters. v2 stores all four correctly.
  This was never an API limitation — it was the v1 defect.
- **Contributors.** The two contributors (Butlin, Long) were present in the
  published v1 record but absent from the local metadata file. A naive re-upload
  would have silently dropped them. Restored.

### What v2 did NOT fix

- **Subjects: still zero.** Six controlled-vocabulary identifiers were supplied.
  Zenodo's deposition API accepts them, reports success, and does not persist them.
- **Version note: still empty.** Same behaviour.

Both need the web form. Correcting either requires a v3, because records are
immutable. The exact values are in `zenodo/DEPOSIT_V2.md`.

### Title

v2 was published with the v1 title. Retitling to match the style of the other two
posts (`ProjectName: description`) was attempted and missed the window — the
record was published while the request was in flight. A retitle now requires v3.

### A metadata wipe caused here

While preparing v2, this deposit lost its entire metadata block — title,
description, notes, creators, keywords, licence — because a PUT carrying only
`version_note` was sent, and Zenodo treats PUT as a full replacement rather than a
merge. It replied "accepted".

Nothing was permanent: the archive lives in a separate bucket, and the record was
still a draft. Restored from `zenodo/metadata_v2.json`.

`zenodo/put_metadata_safely.py` now guards every metadata PUT: complete payload
only, local validation before sending, `cc-by-4.0` rejected as the signature of a
wiped record, and a field-by-field read-back comparison. A partial update is no
longer expressible.

1. https://zenodo.org/me/uploads -> New upload
2. Attach the GitHub repository (public and non-empty, which it now is)
3. Upload the archive; confirm SHA-256 matches the value above
4. Paste metadata from `zenodo/metadata.json`
5. Publish
6. Record the returned DOI in `zenodo/metadata.json`, `CITATION.cff`, and the
   README badge row

Full field mapping and the accuracy rules for the record description are in
`zenodo/UPLOAD_INSTRUCTIONS.md`.

Zenodo files are immutable. Any further change requires publishing a new version,
not editing record 23101903.
