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
| Size | 108,683 bytes (39 files) |
| SHA-256 | `0ce7e12e2f619c6d067a98ea6fd1f83511eb4fb75d79106a7b921b0cd2fc4adc` |
| Result hash EXP-C001 | `b953b8178354f048�` |
| Result hash EXP-C003 | `1249a0ac9091ec2d�` |
| Tests | 48 passing (1 skipped: lab-engine parity, standalone checkout) |
| flake8 | exit 0 |
| Clean room | passed |
| DOI | **none yet** |

## Remaining manual step

1. https://zenodo.org/me/uploads -> New upload
2. Attach the GitHub repository (public and non-empty, which it now is)
3. Upload the archive; confirm SHA-256 matches the value above
4. Paste metadata from `zenodo/metadata.json`
5. Publish
6. Record the returned DOI in `zenodo/metadata.json`, `CITATION.cff`, and the
   README badge row

Full field mapping and the accuracy rules for the record description are in
`zenodo/UPLOAD_INSTRUCTIONS.md`.
