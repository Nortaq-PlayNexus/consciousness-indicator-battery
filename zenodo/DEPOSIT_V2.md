# Battery v2 — READY TO PUBLISH

## Status

```
deposit        23111535
state          unsubmitted  (Publish button now enabled)
concept DOI    10.5281/zenodo.23101902   <- correctly linked to v1
version        2.0.0
files          1
editable at    https://zenodo.org/deposit/23111535
```

**v1 (`10.5281/zenodo.23101903`) stays published and citable. Nothing is
withdrawn or replaced.**

## Why it could not be published before

The draft had **zero files**, so Zenodo disabled the Publish button. It was
created in the web interface but never given an archive. The archive is uploaded
now and the md5 matches the local build exactly.

## This draft is the correct one

`23111535` was created through the **web interface**, which links the concept
correctly: `conceptrecid = 23101902`, which is v1's concept. Every new version
will share that concept DOI, so citations resolve to the newest version while
pointing at the same body of work.

**`23110728` must not be published.** It was my attempt through the API, and
`conceptrecid` is accepted and then silently ignored there — that draft belongs
to a different concept entirely. It is titled `[UNUSABLE DRAFT]`, has no files,
and its notes explain itself. Leave it or delete it; either is fine.

That API failure is why the web interface was necessary, not merely convenient.

## The uploaded archive

| | local | Zenodo | match |
|---|---|---|---|
| size | 109,495 | 109,495 | yes |
| md5 | `aa84712cd82510c774e463938060db66` | `aa84712cd82510c774e463938060db66` | yes |

SHA-256 `d93a6b830e4de4d7b1dbbd86eaf39b45b52c648a4ad47be9df063cdb90ce7498`

Rebuilt and re-verified **from the extracted archive**, not from the source tree,
since what is uploaded cannot be fixed afterwards.

The local `consciousness-indicator-battery-v1.0.0.zip` no longer matches the
published v1 — rebuilding it from a tree that has since gained
`tools/fix_battery_references.py` produces different bytes. Zenodo's v1 copy is
immutable and untouched: 107,535 bytes, md5 `085eb1e7…`.

## Already stored correctly

| Field | Value |
|---|---|
| title | A calibrated indicator battery for AI consciousness, and what survives perturbing it |
| version | 2.0.0 |
| upload_type | software |
| license | mit-license |
| access_right | open |
| language | eng |
| description | 6,943 chars (verbatim from published v1) |
| notes | 1,433 chars |
| creators | 1 |
| **contributors** | **2** — Butlin, Patrick (Oxford) and Long, Robert (Eleos AI Research) |
| keywords | 17 |
| **references** | **4** — see the correction below |
| related_identifiers | 4 |
| communities | 1 — `philosophyofmind` |
| files | 1 |

The contributors were **absent from the local metadata file** and would have been
silently dropped by a naive re-upload. They are restored.

---

# A metadata wipe caused here, and the guard against it

On 2026-10-02 this deposit's entire metadata block was destroyed. Title,
description, notes, creators, contributors, keywords, related identifiers, version
and licence all went to empty, and the licence silently reverted to Zenodo's
default `cc-by-4.0`.

**Cause: a partial PUT.** A request carrying only `version_note` was sent to work
around that field not persisting. Zenodo's deposit API treats PUT as a **full
replacement, not a merge**. The response was "accepted".

The archive survived, because files live in a separate bucket. Nothing had been
published, so nothing was permanent. But an empty title and the wrong licence are
one click from permanent.

A PUT that reports success while deleting everything else is the worst available
failure mode, because it looks like it worked.

**Guard:** `zenodo/put_metadata_safely.py`. Every metadata PUT must now

1. build the payload from the complete metadata file, never a fragment
2. validate locally that title, description, licence, creators and keywords are
   all present and non-empty before sending anything
3. reject `cc-by-4.0` explicitly, as the signature of an already-wiped record
4. read the record back and compare field by field
5. exit non-zero on any destructive change

```bash
python zenodo/put_metadata_safely.py 23111535 --dry-run   # validate only
python zenodo/put_metadata_safely.py 23111535             # send and verify
```

Current status of that check on this deposit:

```
~ subjects: sent but NOT stored -- known API behaviour, enter it in the web form
~ version_note: sent but NOT stored -- known API behaviour, enter it in the web form
OK: metadata stored intact
```

---

# TWO FIELDS TO ADD BY HAND

## References: already stored — do NOT re-add

**Correction.** An earlier version of this file said references also had to be
entered by hand. That was wrong.

The references field works correctly as long as it is sent as a **list of
strings**. v1 sent it as a *single concatenated string*, and Zenodo iterated that
string into 722 one-character entries. That was never an API limitation — it was
the original v1 defect.

Verified on this deposit:

```
references : 4 entries
first      : "Butlin, P., Long, R., Elmoznino, E., Bengio, Y., et al. (2023). Consci..."
```

So the 722-character corruption is fixed in v2 by construction, and the four
citations are stored as intended.

---

## The two fields that genuinely cannot be set through the API

`subjects` and `version_note` are accepted by Zenodo's deposition endpoint,
report success, and are not persisted. Verified on this deposit: both read back
as empty after a successful PUT.

That is three fields on this account that behave this way, after `conceptrecid`.
Paste these two in the web form.

## 1. Version note

```
Corrects two metadata defects in version 1.0.0 (DOI 10.5281/zenodo.23101903).
The scientific content, code, archive and results are unchanged; this is a
metadata-only correction.

1. REFERENCES. In 1.0.0 the references field was published as 722 array entries of
one character each, rather than the four intended citations. The source metadata
held the citations as a single concatenated string, and Zenodo iterated it into
characters. Nothing reported the error: a 722-element array of one-character
strings is valid JSON, so the upload and every later read both appeared
successful. The four citations are recoverable and are correct in this version,
where the field is sent as a list of strings.

2. SUBJECTS. In 1.0.0 the record carries zero subjects. Six free-text subject
strings were supplied, but Zenodo requires controlled-vocabulary identifiers and
silently discards free text.

Both defects were found by inspecting the published record rather than trusting
the upload. Version 1.0.0 remains published and is not withdrawn: it is the
citable record for the scientific content. Cite this version for the corrected
metadata.
```

## 2. Subjects

Free text is silently discarded. These ids were looked up in Zenodo's live
vocabulary, not guessed.

| id | title |
|---|---|
| `mesh:D003243` | Consciousness |
| `euroscivoc:297` | Artificial intelligence |
| `mesh:D009488` | Neurosciences |
| `euroscivoc:307` | Software |
| `euroscivoc:609` | Philosophy |
| `mesh:D015203` | Reproducibility of Results |

---

## After publishing

Copy the **new version** DOI and record it *alongside* v1, not replacing it:

- `zenodo/metadata_v2.json` → `doi`
- `CITATION.cff` → note both DOIs
- `RELEASE.md` → record the correction

All further changes are new versions. Nothing is ever edited in place.
