# Zenodo status — consciousness-indicator-battery

**Single source of truth. Everything below is current as of 2026-10-04.**

## Published

| Version | DOI | Published | Note |
|---|---|---|---|
| v1.0.0 | `10.5281/zenodo.23101903` | 2026-10-02 | superseded on metadata; **still citable** |
| **v2.0.0** | **`10.5281/zenodo.23111535`** | 2026-10-03 | **cite this** |

**Concept DOI `10.5281/zenodo.23101902`** — shared by every version.

### What v1 got wrong

- **references**: published as **722 array entries of one character each**,
  because the source metadata held the citations as a single concatenated string
  and Zenodo iterated it into characters. Valid JSON, so nothing warned.
- **subjects**: **zero**. Free-text strings were supplied; Zenodo requires
  controlled-vocabulary identifiers and discards free text.

v2 fixed the references. **Subjects are still zero** — that is why v3 exists.

---

## Draft, ready to publish

| | |
|---|---|
| Draft | **`23122664`** |
| Edit | **https://zenodo.org/deposit/23122664** |
| Concept DOI | `23101902` — **verified linked** |
| Version | 3.0.0 |
| Files | 1 |
| Archive | `consciousness-indicator-battery-v3.0.0.zip`, 115,050 bytes |
| SHA-256 | `6199c42cf9c44609bafdbec09df0a0c73e46fb899ccbe5c306f21d31c5c54c5f` |
| MD5 as uploaded | `371e3447554ac602794b10517c0750b6` |

### What v3 changes

**Metadata only.** No code, no results, no scientific content — identical to v1
and v2.

1. **Retitled** to the house style used by the other two repositories:

   > Consciousness Indicator Battery: calibrated indicators for AI consciousness,
   > and what survives perturbing them

   v2 kept v1's title because the retitle was attempted while the record was being
   published, and the PUT returned 404. A published record is immutable, so this
   is the first version where the change is possible.

2. **Six subjects** added — the field v2 still lacked.
3. **Version note** drafted, explaining what v1 got wrong and why v3 exists.

### Verified on read-back

| field | status |
|---|---|
| title | ok |
| version | ok |
| license | ok |
| description | ok |
| notes | ok |
| creators | 1/1 |
| contributors | **2/2** |
| keywords | 17/17 |
| references | 4/4 |
| related_identifiers | 4/4 |
| communities | 1/1 |

The two contributors — Butlin, Patrick (Oxford) and Long, Robert (Eleos AI
Research) — were present in the published v1 record but **absent from the local
metadata file**. A naive re-upload would have silently dropped them.

### Three steps, then publish

1. **Subjects** — the deposition API discards this field. Paste by hand:

   | id | title |
   |---|---|
   | `mesh:D003243` | Consciousness |
   | `euroscivoc:297` | Artificial intelligence |
   | `mesh:D009488` | Neurosciences |
   | `euroscivoc:307` | Software |
   | `euroscivoc:609` | Philosophy |
   | `mesh:D015203` | Reproducibility of Results |

2. **Version note** — from `metadata_v2.json`, field `version_note`.

3. **Publish.**

### After publishing

Record the new DOI in four places: `metadata_v2.json`, `CITATION.cff`, the README
badge, `RELEASE.md`. Note **both** version DOIs in `CITATION.cff` — v3 to cite,
v1 superseded but still valid.

Any further change must be a **new version**, never an edit.

---

## Dead draft — leave alone

| | |
|---|---|
| Draft | `23110728` |
| Title | `[UNUSABLE DRAFT] battery v2 attempt - concept linkage failed, do not publish` |
| Why | Created through the **legacy** deposit endpoint, whose `conceptrecid` is accepted and then ignored. It belongs to concept `23110727`, not `23101902`. |
| Files | none |

No files, wrong concept, and its notes field explains itself. **Never delete a
deposit** — the maintainer decides that. Leave it or remove it yourself.

---

## Toolbox

| Script | Purpose |
|---|---|
| `new_version.py` | create and populate a version via `POST /api/records/<id>/versions`, verifying concept linkage **before** uploading |
| `put_metadata_safely.py` | update draft metadata; refuses partial PUTs |
| `build_zenodo_package.py` | byte-reproducible archive; `BATTERY_VERSION` env var sets the filename |
| `upload_v2.py`, `upload_to_zenodo.py` | legacy creation paths; superseded by `new_version.py` |

See `HANDOFF.md` at the repository root for the API traps and standing instructions.

---

## Note on this working copy

Up to 2026-10-04 this repository lived at
`C:\Users\natha\AppData\Local\Temp\opencode\cib-clean`. **That directory was
cleared and the working copy lost.** It was recovered by cloning from GitHub,
which is why no committed work was lost — but the three Zenodo drafts were never
at risk, because those live on Zenodo's servers, not here.

The repository now lives at:

```
C:\Users\natha\AI_RESEARCH\consciousness-indicator-battery
```

Do not put a working copy under `%TEMP%`.
---

## Published � verified 2026-10-04

| version | DOI | concept | archive |
|---|---|---|---|
| v1.0.0 | `10.5281/zenodo.23101903` | `10.5281/zenodo.23101902` | superseded on metadata |
| v2.0.0 | `10.5281/zenodo.23111535` | `10.5281/zenodo.23101902` | 109,495 B |
| v3.0.0 | `10.5281/zenodo.23122664` | `10.5281/zenodo.23101902` | 115,050 B |

All three resolve through `doi.org`. Cite the concept DOI
`10.5281/zenodo.23101902` to cover all versions.

## DEFECT: v3.0.0 is not byte-reproducible from this repository

Found during post-publication verification on 2026-10-04.

| | bytes | md5 |
|---|---|---|
| published `23122664` | 115,050 | `371e3447554ac602794b10517c0750b6` |
| rebuilt from HEAD | 116,863 | `00d84b0dbaa604f13f2cf105096bb85d` |

`battery.py` content is byte-identical between the two � zero differing lines. The
difference is line endings: the published archive carries 858 CRLF pairs where
this repository has none.

**Cause.** The v3 archive was built from the working copy at
`%TEMP%\opencode\cib-clean`, which was lost when Windows cleared the temp
directory. This repository is the re-clone, and it carries `.gitattributes` with
`* text=auto eol=lf`; the lost copy predates that file. `core.autocrlf` is `true`
on this machine, which produced the CRLF working tree the archive was built from.

**This is not corruption.** All 41 SHA-256 digests in the published
`manifest.json` verify against the files beside them, so a reader who downloads
the archive can confirm it is intact. What fails is narrower: a reader who clones
this repository and rebuilds gets different bytes than the archive contains.

**Remedy.** Publish v3.0.1 built from the current tree, so repository and artifact
agree. No code differs, so nothing else needs to change.

## Known gaps on all published versions

- **Zero subjects.** Zenodo's API accepts the field, reports success and stores
  nothing � verified against both `/api/deposit/depositions` and
  `/api/records/<id>/draft`. Published records are immutable, so this cannot be
  corrected in place. Intended values are in `zenodo/metadata_v2.json` and
  `PUBLISH_CHECKLIST.md`.
- **Not search-indexed.** Both this project's records are `resource_type:
  software` and return zero hits on Zenodo DOI and title search, while the
  `dataset` records from the same period are indexed. Live and citable; only
  discoverability is affected. Worth re-checking on v3.0.1.
