# Publish v3.0.1 — draft 23137224

**One record. One publish click. Nothing is lost if you do nothing.**

```
https://zenodo.org/deposit/23137224
```

**Draft. Not published. No DOI minted yet.**

---

## What this version is for

3.0.0 is not byte-reproducible from its own repository. A reader who cloned and
rebuilt got different bytes from the ones published. **3.0.1 rebuilds
byte-for-byte.** No code, result, or claim changed between them.

This version also exists because it is the first opportunity to publish with
subjects actually attached — see below.

---

## Verified before staging

| check | result |
|---|---|
| state | `unsubmitted` |
| concept | `23101902` — correct, no fork |
| version | `3.0.1` |
| archive | `consciousness-indicator-battery-v3.0.1.zip` |
| size | 116,848 B — matches local |
| checksum | `726b7584f439c46d7da0e89d4ebe03da` — matches local |
| description | identical as rendered |
| build reproducibility | two builds, identical digest |
| CRLF in archive | 0 of 43 entries |
| build gates | 4 / 4 pass |

---

## Before you publish: paste these two things

Both fields are **discarded by Zenodo's API on both endpoints** — verified against
`PUT /api/deposit/depositions/<id>` and `PUT /api/records/<id>/draft` on
2026-10-04. They can only be entered in the web form. **This is the last chance:
published records are immutable.**

### 1. Subjects — all six

| id | title |
|---|---|
| `mesh:D003243` | Consciousness |
| `euroscivoc:297` | Artificial intelligence |
| `mesh:D009488` | Neurosciences |
| `euroscivoc:307` | Software |
| `euroscivoc:609` | Philosophy |
| `mesh:D015203` | Reproducibility of Results |

Every published version of this record so far — v1.0.0, v2.0.0, v3.0.0 — has
**zero subjects**, permanently, for exactly this reason.

### 2. Version note

> v3.0.1 - rebuilds byte-for-byte from the repository; v3.0.0 does not, because it was built from a CRLF working copy and the manifest generator was platform-dependent. No code, result or claim changed. v3.0.0 remains citable and self-consistent.

---

## Then

1. **Publish.**
2. **Read it back** — `https://zenodo.org/api/records/<id>`:
   ```
   python zenodo/check_description.py <new_id> zenodo/description_v3_0_1.md
   python tools/verify_manifest.py          # if present
   ```
   Confirm `subjects` has 6 entries. Do not assume. Every v1 record published
   with zero subjects and nobody checked, because Zenodo reports success either way.
3. Record the DOI in `zenodo/DEPOSIT_STATUS.md`, `CITATION.cff`, README badge.
4. Check whether the record is **search-indexed** — both previous versions return
   zero hits on Zenodo DOI and title search. If v3.0.1 is indexed, the cause was
   transient. If not, it is the `software` resource type and worth raising with
   Zenodo support.

---

## Reproducing v3.0.1 yourself

```
git clone https://github.com/Nortaq-PlayNexus/consciousness-indicator-battery
cd consciousness-indicator-battery
BATTERY_VERSION=3.0.1 python zenodo/build_zenodo_package.py
```

Expected: **116,848 bytes**, `md5:726b7584f439c46d7da0e89d4ebe03da`.

If that command produces anything else, the repository and the published record
have diverged again — please report it rather than rebuilding around it.

---

## Tools

| script | purpose |
|---|---|
| `zenodo/make_v3_0_1.py` | derives v3.0.1 metadata from v3.0.0; aborts if any field would change |
| `zenodo/build_zenodo_package.py` | builds the archive; now fails on any CRLF |
| `zenodo/check_description.py` | compares stored vs local description as **rendered** text |
| `zenodo/new_version.py` | creates the version via `POST /api/records/<id>/versions` |

### Field-name trap

The two endpoints name file fields differently:

| | draft endpoint | published record |
|---|---|---|
| name | `filename` | `key` |
| size | `filesize` | `size` |
| checksum | `726b7584…` | `md5:726b7584…` |

Reading a draft with the record endpoint's field names returns empty strings
rather than an error, which looks like a missing file.

### Description comparison

Zenodo stores descriptions as HTML and decodes entities on save: a local `&gt;=`
comes back as `>=`. Comparing raw strings reports a difference no reader can see.
`check_description.py` compares **rendered** text — local 9157, remote 9157,
identical.