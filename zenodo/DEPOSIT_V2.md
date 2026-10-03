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
| creators | 1 |
| **contributors** | **2** — Butlin, Patrick (Oxford) and Long, Robert (Eleos AI Research) |
| keywords | 17 |
| related_identifiers | 4 |
| communities | 1 — `philosophyofmind` |

The contributors were **absent from the local metadata file** and would have been
silently dropped by a naive re-upload. They are restored.

---

# THREE FIELDS TO ADD BY HAND — the API drops all three

Zenodo's deposition API has now silently discarded four different fields on this
account: `subjects`, `references`, `conceptrecid`, and `version_note`. Each was
accepted without error. None is echoed back on read.

Paste these in the web form.

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
successful. The four citations are recoverable and are correct in this version.

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

## 3. References

1. Butlin, P., Long, R., Elmoznino, E., Bengio, Y., et al. (2023). Consciousness
   in Artificial Intelligence: Insights from the Science of Consciousness.
   arXiv:2308.08708.
2. Butlin, P., Long, R., Bayne, T., Bengio, Y., et al. (2026). Identifying
   indicators of consciousness in AI systems. Trends in Cognitive Sciences,
   30(6), 488-501. https://doi.org/10.1016/j.tics.2025.10.011
3. Long, R., Sebo, J., Butlin, P., Plunkett, D., Campbell, R., Beasley, C., Saad,
   B., & Sims, T. (2026). Studying AI Welfare Empirically. NYU Center for Mind,
   Ethics, and Policy & Eleos AI Research.
   https://nonhumanminds.org/studying-ai-welfare-empirically
4. Gurnee, B., Sofroniew, N., Lindsey, J., et al. (2026). Verbalizable
   Representations Form a Global Workspace in Language Models. Transformer
   Circuits. https://transformer-circuits.pub/2026/workspace

---

## After publishing

Copy the **new version** DOI and record it *alongside* v1, not replacing it:

- `zenodo/metadata_v2.json` → `doi`
- `CITATION.cff` → note both DOIs
- `RELEASE.md` → record the correction

All further changes are new versions. Nothing is ever edited in place.
