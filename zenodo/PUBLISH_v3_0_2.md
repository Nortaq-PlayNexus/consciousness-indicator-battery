# Publish v3.0.2 — **PUBLISHED 2026-10-05**

> **This file is a historical record, not a to-do list.**
>
> v3.0.2 was published on **2026-10-05** as **`10.5281/zenodo.23150723`**,
> 109,791 B, `md5:cf7b2953325002e2c1ad913dea8e59fa`, state `done`. It is the
> version to cite. Verified by API read-back on 2026-10-08.
>
> The "Draft. Not published. No DOI minted." line this file used to open with was
> true on 2026-10-04 and is no longer true. `zenodo/DEPOSIT_STATUS.md` still
> describes v3.0.1 as the pending publication; it too is stale.
>
> The one open item that survives: **subjects are 0 on every published version**,
> because Zenodo's API accepts the field, reports success, and stores nothing.
> That is defect D2 in the laboratory's `PUBLICATION_VERIFICATION.md`.

**Original instructions, preserved:**

```
https://zenodo.org/deposit/23150723
```

Concept `23101902` — the same concept as every prior version, so
`10.5281/zenodo.23101902` resolves to v3.0.2.

---

## Why this version exists

v3.0.1 (`10.5281/zenodo.23137224`) is published and cannot be edited or deleted —
Zenodo records are immutable once published. Its **description claims the archive
rebuilds byte-for-byte, and that is false of the archive it shipped.** A reader
would trust a claim the artefact does not bear.

A new version is the only correction route. That is what this is.

| version | archive | rebuilds? | subjects | issue |
|---|---|---|---|---|
| 3.0.0 | 115,050 B | no | 0 | CRLF working copy; platform-dependent manifest generator |
| 3.0.1 | 116,848 B | no | 0 | deposit contained a session doc quoting its own digest |
| **3.0.2** | **109,791 B** | **yes** | **paste below** | — |

**No code, result, or claim differs across the three.** They differ only in what
is inside the deposit and whether it can be regenerated.

---

## Verified before staging

| check | result |
|---|---|
| state | `unsubmitted` |
| concept | `23101902` — correct, no fork |
| version | `3.0.2` |
| archive | `consciousness-indicator-battery-v3.0.2.zip` |
| size | 109,791 B — matches local |
| checksum | `cf7b2953325002e2c1ad913dea8e59fa` — matches local |
| description | identical as rendered (11,735 / 11,735) |
| build reproducibility | two builds, identical digest |
| CRLF in archive | 0 of 41 entries |
| build gates | 4 / 4 pass |
| source | commit `fdb9d3c`, clean working tree |

---

## Do these two things BEFORE publishing

Both fields are **discarded by Zenodo's API on both endpoints** — verified against
`PUT /api/deposit/depositions/<id>` and `PUT /api/records/<id>/draft`. Web form
only. **Once you publish, it is permanent — v3.0.0, v3.0.1 and all twelve
laboratory records are proof.**

### 1. Subjects — all six

| id | title |
|---|---|
| `mesh:D003243` | Consciousness |
| `euroscivoc:297` | Artificial intelligence |
| `mesh:D009488` | Neurosciences |
| `euroscivoc:307` | Software |
| `euroscivoc:609` | Philosophy |
| `mesh:D015203` | Reproducibility of Results |

### 2. Version note

> v3.0.2 - ships the archive that rebuilds byte-for-byte from the repository (109,791 B, md5:cf7b2953..., commit fdb9d3c, two builds identical). v3.0.1 did not, because the deposit contained a session document quoting its own digest; v3.0.0 did not, because of CRLF line endings and a platform-dependent manifest generator. No code, result or claim changed in any version. v3.0.0 and v3.0.1 remain citable.

**Then publish.** Not the other way round.

---

## After publishing — verify, do not assume

```
python zenodo/check_description.py <new_id> zenodo/description_v3_0_2.md
```

Expect `IDENTICAL as rendered`. Then confirm `subjects` has 6 entries:

```
https://zenodo.org/api/records/<new_id>
```

Every prior version of this record has zero subjects, and Zenodo reported success
each time.

Then record the DOI in `zenodo/DEPOSIT_STATUS.md`, `CITATION.cff` and the README
badge, and check whether the record is **search-indexed** — v3.0.0 and v3.0.1 both
return zero hits on Zenodo DOI and title search.

---

## Reproducing v3.0.2

```
git clone https://github.com/Nortaq-PlayNexus/consciousness-indicator-battery
cd consciousness-indicator-battery
git checkout fdb9d3c
BATTERY_VERSION=3.0.2 python zenodo/build_zenodo_package.py
```

Expected: **109,791 bytes**, `md5:cf7b2953325002e2c1ad913dea8e59fa`.

Note the digest differs from the v3.0.1 build of the same size: `manifest.json`
records the version, so a different version is a different archive by design.

---

## What was fixed, and what caused each

1. **CRLF.** `.gitattributes` normalises to LF, but v3.0.0 was built from a
   working copy predating that file.
2. **Platform-dependent manifest.** `manifest.json` was written with
   `write_text()` and no `newline=`, so Windows produced CRLF and Linux LF from
   identical source — two different archives from a tool whose purpose is
   identical-input-identical-output.
3. **Self-referential deposit.** `HANDOFF.md` was inside the archive and quoted
   the archive's digest, and is rewritten every session, so the archive could
   never match its repository. Now excluded, along with `PUBLISH_CHECKLIST.md`
   and `RELEASE.md`.

Each has a gate that was tested by making it fail first: the CRLF gate blocked a
build with exit 1; the version guard aborted on a fake base version; the digest
check caught a copied-from-v3.0.1 value that was wrong for v3.0.2.