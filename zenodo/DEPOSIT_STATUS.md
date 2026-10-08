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

## Published — verified by API read-back 2026-10-08

Corrected 2026-10-08. This table previously stopped at v3.0.0 and
described the next version as pending. Both were true on 2026-10-04.
The live API shows three further versions published since.

| version | DOI | concept | archive | state |
|---|---|---|---|---|
| v1.0.0 | `10.5281/zenodo.23101903` | `10.5281/zenodo.23101902` | superseded on metadata | `done` |
| v2.0.0 | `10.5281/zenodo.23111535` | `10.5281/zenodo.23101902` | 109,495 B | `done` |
| v3.0.0 | `10.5281/zenodo.23122664` | `10.5281/zenodo.23101902` | 115,050 B | `done` |
| v3.0.1 | `10.5281/zenodo.23137224` | `10.5281/zenodo.23101902` | 116,848 B | `done` — **superseded, do not cite** |
| **v3.0.2** | **`10.5281/zenodo.23150723`** | `10.5281/zenodo.23101902` | 109,791 B | `done` — **cite this one** |

All five resolve through `doi.org`. Cite the concept DOI
`10.5281/zenodo.23101902` to cover all versions, or v3.0.2 directly.

### Why v3.0.1 must not be cited

v3.0.1's description claims its archive rebuilds byte-for-byte from the
repository. That is false of the archive it shipped: the draft was built
from a tree with an uncommitted edit to `HANDOFF.md`, which was excluded
from the final archive. A published record is immutable, so the only
correction route was a new version, which is what v3.0.2 is. See
`HANDOFF.md` section 0.

## DEFECT: v3.0.0 is not byte-reproducible from this repository

Found during post-publication verification on 2026-10-04.

| | bytes | md5 |
|---|---|---|
| published `23122664` | 115,050 | `371e3447554ac602794b10517c0750b6` |
| rebuilt from HEAD | 116,863 | `00d84b0dbaa604f13f2cf105096bb85d` |

`battery.py` content is byte-identical between the two — zero differing lines. The
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

**Remedy (done).** v3.0.2 is published and its archive does rebuild
byte-for-byte from the current tree. No code, result, or claim differs across
v3.0.0, v3.0.1 and v3.0.2.

## Drafts awaiting publication — reviewed 2026-10-08

Three drafts are staged and **unpublished**. Nothing below has a DOI yet, so all
of it is still correctable.

| draft | project | version | concept | archive |
|---|---|---|---|---|
| `23229093` | ScientificDiscoveryLab | 2.0.1 | `23109116` (v2.0.0 = `23122787`) | `ScientificDiscoveryLab-v2.0.1.zip`, 6,785,251 B |
| `23229094` | Consciousness Indicator Battery | 3.0.3 | `23101902` (v3.0.2 = `23150723`) | `consciousness-indicator-battery-v3.0.3.zip`, 110,029 B |
| `23229095` | Phantom Vision Lab | 2.0.1 | `23112115` (v2.0.0 = `23123095`) | `phantom-vision-lab-v2.0.1.zip`, 99,211 B |

Edit URLs are `https://zenodo.org/deposit/<id>`.

### v3.0.3 was not publishable as staged

It has been corrected. What was wrong:

1. **The archive did not rebuild from the repository.** `CITATION.cff` and
   `README.md` were inside the deposit as modified working-tree files, and
   `tests/test_citation.py` was inside it while untracked. Both point at the same
   defect as v3.0.1 — the archive is staged by walking the working tree, so
   uncommitted work silently becomes part of a permanently frozen deposit.
2. **The description was byte-identical to v3.0.2's.** It never mentioned 3.0.3,
   had no section saying what changed, and its reproduction steps still
   instructed `BATTERY_VERSION=3.0.1` and `3.0.2`.
3. **The notes** ended by describing 2.0.0. **`publication_date`** was
   2026-10-03. **`description_source`** pointed at `description.md`, which does
   not exist. The `related_identifiers` note named a commit that is not an
   ancestor. **`version_note_requested`** was headed "v3.0.2", copied verbatim.

Rebuilt at commit `b47987e`: **110,029 B**, `md5:33a4e5a7940881fa6eac4588d00a9e49`,
`sha256:d8aa4f3d2bb92b51644bb7e423fada5be0bd6820b09e965bcaded23e09cab657`.
Verified byte-for-byte from a fresh `git clone`, identical across repeated builds,
all four build gates passing.

The root cause is now gated: `preflight_clean_tree()` in
`build_zenodo_package.py` fails the build and names every file that would change
the archive without being committed. `tests/` is excluded from the deposit, so
the untracked network-calling guard can no longer ship by accident.

### Before publishing any of the three

**Nothing is left to do by hand.** Subjects are set on all three drafts and
verified: 6 on `23229094`, 5 on `23229093`, 5 on `23229095`, each with `term`,
`identifier` and `scheme` present.

This corrects a conclusion this repository carried for three versions, recorded
in `DRAFT_23122664.md`, `DEPOSIT_STATUS.md` and `PUBLISH_v3_0_2.md`: that Zenodo's
API discards `subjects` and the field must be typed into the web form. **It does
not.** The field was never broken, the payload shape was wrong. See
`zenodo/set_subjects.py` for the measurements and the shape that works.

The trap worth remembering: `[{"scheme": "mesh", "id": "D003243"}]` returns 200,
raises the count, and **drops the identifier**, leaving subjects that name a
scheme and nothing else. Checking `len(subjects)` alone would have passed that
straight through to a permanent record.

### Other open items, not fixed

- `23229095` has no Zenodo community (`communities: null`) and no references.
  Neither is required; no community slug was guessed, because an invalid one
  fails the PUT all-or-nothing and would discard the rest of the metadata.
- The v2.0.1 archives for ScientificDiscoveryLab and Phantom Vision Lab are not
  present locally, so their uploads were verified by Zenodo's own reported size
  and checksum only, not against a local build.

---

## Known gaps on all published versions

- **Zero subjects — on every version published before 3.0.3.** This file
  previously explained it as an API limitation, "verified against both
  `/api/deposit/depositions` and `/api/records/<id>/draft`". That verification was
  sound and the conclusion was still wrong: both endpoints store subjects
  correctly when given `term` + `identifier` + `scheme`. The probes used
  `{"id": ...}`, which stores nothing. Published records remain immutable, so
  these versions still cannot be corrected in place — that part is unchanged —
  but it now takes one scripted new version each, not a manual form entry.
  Intended values are in `zenodo/metadata_v2.json`; the tool is
  `zenodo/set_subjects.py`. v3.0.3 is the first version of this record to carry
  subjects.
- **Not search-indexed.** Both this project's records are `resource_type:
  software` and return zero hits on Zenodo DOI and title search, while the
  `dataset` records from the same period are indexed. Live and citable; only
  discoverability is affected. Re-checked on v3.0.2 and unchanged.
