# Zenodo DOI registration and upload

## STATUS: DONE. These instructions are historical.

**This deposit was published.** Cite:

| | |
|---|---|
| **v2.0.0 — cite this** | `10.5281/zenodo.23111535` |
| v1.0.0, still citable | `10.5281/zenodo.23101903` |
| Concept DOI, shared by both | `10.5281/zenodo.23101902` |

Everything below is the procedure that was followed, kept because the ordering
matters if a **new version** is ever needed. Zenodo records are immutable, so none
of it can be repeated against a published record.

**Set every field before publishing.** v2 was published before its subjects and
version note were entered, because those two fields are silently discarded by the
deposition API and must be typed in the web form. That mistake costs a v3 to
correct. See `HANDOFF.md` in the repository root.

---

## Original procedure (historical)

Sequence required before a DOI can be minted:

1. Push the GitHub repository (`git push -u origin main` in the repo root).
2. Create the Zenodo record and attach the GitHub repository.
3. Upload the package, review, publish.
4. Zenodo assigns the DOI.
5. Record the DOI in `zenodo/metadata.json`, `CITATION.cff`, and the README badge row.

## Prerequisite

The GitHub repository must be **public and non-empty** before the Zenodo–GitHub
integration will link it. As of writing the repository
`https://github.com/Nortaq-PlayNexus/consciousness-indicator-battery`
exists and is **empty** — the name is reserved but nothing is pushed.

```powershell
# from the repository root
git push -u origin main
```

Verify before uploading:

```powershell
gh repo view Nortaq-PlayNexus/consciousness-indicator-battery --json isEmpty
```

Must report `isEmpty: false`.

## Steps

### 1. Reserve the DOI (optional but recommended)

On the new-upload page, click **Reserve DOI** first. This gives the concept DOI
before any file is attached, which is useful if the metadata needs to be cited
while the package is still being checked.

### 2. Upload the archive

```
zenodo/consciousness-indicator-battery-v1.0.0.zip
```

Regenerate if stale:

```powershell
python zenodo/build_zenodo_package.py
```

It stages the tree, writes `manifest.json` with a SHA-256 per file, builds the
zip, then **extracts the archive and re-runs the full verification against the
extraction** — because Zenodo files are immutable once published.

### 3. Metadata

Paste from `zenodo/metadata.json`. Field mapping:

| Zenodo field | Value |
|---|---|
| Upload type | Software |
| Title | A calibrated indicator battery for AI consciousness, and what survives perturbing it |
| Subtitle | (see metadata.json) |
| Version | 1.0.0 |
| Publication date | 2026-10-02 |
| Access right | Open |
| License | MIT License |
| Creator | ScientificDiscoveryLab contributors |
| Keywords | 17 terms, see metadata.json |
| Related identifier | https://github.com/Nortaq-PlayNexus/consciousness-indicator-battery (isSupplementTo, repository) |

### 4. Verify before publishing

Zenodo files are **immutable after publication**. Metadata stays editable; files
do not. So verify the archive contents now:

```powershell
# build_zenodo_package.py already does this; re-run it if anything changed
python zenodo/build_zenodo_package.py
```

Expected: `ARCHIVE VERIFIED`, 38 tests pass, both result hashes VALID.

Manually, if you want to inspect before publishing:

```powershell
Expand-Archive zenodo/consciousness-indicator-battery-v1.0.0.zip -DestinationPath verify\ -Force
cd verify\consciousness-indicator-battery
pip install -r requirements.txt
pytest -q
python verify_clean_room.py
```

### 5. Record the DOI

```powershell
# after publishing, fill in the returned DOI
(Get-Content zenodo\metadata.json -Raw) -replace '"doi": ""', '"doi": "10.5281/zenodo.23111535"' | Set-Content zenodo\metadata.json
```

Then update `CITATION.cff` and the README badge row.

**Step 5 is the one that cannot be retried.** Everything above is repeatable
against a draft. This step is only possible because publication was the *last*
action — and it still was not enough, because two fields (`subjects`,
`version_note`) can only be set through the web form at all, and were missed.
Fold them into step 2 of the next version.

## Accuracy requirements for the record description

These are accurate and should be stated:

- No AI system was scored.
- No claim is made about AI consciousness.
- The calibration is circular and unresolved.
- Ranking is robust under perturbation; absolute probabilities are not.

These are **not** accurate and must not appear:

- The project determined whether AI is conscious.
- The project proved AI is not conscious.
- A reliable measure of AI consciousness now exists.
- The instrument is validated.

The original authors' own caveat applies and is quoted in the metadata:
satisfying all fourteen indicators **would still not mean** a system is
definitely conscious.

## License note

MIT covers the code and documentation in this deposit. The upstream indicator
paper is CC BY-NC-SA 4.0 and is cited, not reproduced. If any upstream text were
added, the combined work would fall under the more restrictive upstream terms —
so no upstream text is included beyond attributed quotation for identification.