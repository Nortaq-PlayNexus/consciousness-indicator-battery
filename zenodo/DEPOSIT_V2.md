# Battery v2 — prepared, blocked on the Zenodo web interface

## Status: v2 is fully prepared but CANNOT be published via the API

Everything for v2 exists and is verified. The one thing that cannot be done from
here is creating a *new version* of an already-published record — Zenodo's legacy
deposit API silently ignores the field that expresses it.

## The blocker, exactly

To make v2 a version of v1 (same concept DOI `10.5281/zenodo.23101902`), the
deposition must carry `conceptrecid = 23101902`. Both ways of sending it were
**accepted without error and then ignored**:

| Attempt | Result |
|---|---|
| `POST /deposit/depositions` with `metadata.conceptrecid = 23101902` | draft created, `conceptrecid = 23110727` — a **new** concept |
| `PUT /deposit/depositions/{id}` with the same field | accepted, `conceptrecid` unchanged |

Publishing that draft would mint a **separate concept DOI**, and v2 would not be a
version of v1 at all. That is a permanent, mislinked, hard-to-undo outcome, so it
was not published.

This is the **third** field this API has accepted and discarded, each time with no
error and no warning:

1. `subjects` — silently dropped
2. `references` — silently dropped
3. `conceptrecid` — silently ignored

A field that is accepted and discarded is worse than one that is rejected. Rejection
tells you something is wrong. Acceptance tells you it worked.

## The leftover draft

`23110728`, state `unsubmitted`, titled
`[UNUSABLE DRAFT] battery v2 attempt - concept linkage failed, do not publish`.

**It is left in place deliberately and was not deleted.** It is harmless while
unsubmitted and its notes field explains itself. Delete it yourself if you want a
clean account.

## How to publish v2 — about three minutes

1. Open **https://zenodo.org/records/23101903**
2. Click **New version**
3. Upload `zenodo/consciousness-indicator-battery-v2.0.0.zip`
   from the battery repository
4. Paste the description from `zenodo/description_v2.md`
5. Set version to **2.0.0**, license **MIT**, access **open**
6. Paste the `version_note` and `notes` from `metadata_v2.json`
7. Add the **6 references** and **6 subjects** — see below, the API drops them
8. Publish

The Zenodo web form will link it to concept `10.5281/zenodo.23101902` correctly,
which is exactly what the API would not do.

## The v2 archive

| | |
|---|---|
| file | `consciousness-indicator-battery-v2.0.0.zip` |
| size | 109,495 bytes |
| SHA-256 | `d93a6b830e4de4d7b1dbbd86eaf39b45b52c648a4ad47be9df063cdb90ce7498` |
| MD5 | `aa84712cd82510c774e463938060db66` |
| verification | rebuilt and re-verified **from the extracted archive**, not from the source tree |

That last point matters: the builder extracts what it just wrote and runs the test
suite, result-hash check and headline-claim check against the extracted copy, since
Zenodo files are immutable and cannot be fixed afterwards.

Note the local `consciousness-indicator-battery-v1.0.0.zip` no longer matches the
published v1 — rebuilding it from a tree that has since gained
`tools/fix_battery_references.py` produces different bytes. The copy **on Zenodo**
is immutable and untouched: still 107,535 bytes, md5 `085eb1e7…`. Nothing about v1
changed.

## What v2 changes, and what it does not

**Fixes exactly two metadata defects.** The scientific content, code, archive
contents and results are identical to v1.

1. **references** — v1 published 722 single-character array entries instead of 4
   citations. Cause: the source metadata held the citations as one concatenated
   string and Zenodo iterated it into characters. Nothing reported it, because a
   722-element array of one-character strings is valid JSON.
2. **subjects** — v1 published **zero**. Six free-text strings were supplied;
   Zenodo requires controlled-vocabulary identifiers and silently discards free text.

**v1 stays published and citable.** Nothing is withdrawn or superseded. v1 is the
record for the scientific content; v2 is the record with correct metadata. The
version note says so explicitly.

## Also preserved from v1

These were in the published record but **absent from the local metadata file**, and
would have been silently lost in a naive re-upload. They are restored in
`metadata_v2.json`:

- **2 contributors** — Butlin, Patrick (Global Priorities Institute, University of
  Oxford) and Long, Robert (Eleos AI Research)
- **creator affiliation** — "Scientific Discovery Lab", not "independent"
- **community** — `philosophyofmind`
- all **4 related identifiers** and **17 keywords**, verbatim

## Subjects — the API drops these; add them by hand

| id | title |
|---|---|
| `mesh:D003243` | Consciousness |
| `euroscivoc:297` | Artificial intelligence |
| `mesh:D009488` | Neurosciences |
| `euroscivoc:307` | Software |
| `euroscivoc:609` | Philosophy |
| `mesh:D015203` | Reproducibility of Results |

## References — paste these four

1. Butlin, P., Long, R., Elmoznino, E., Bengio, Y., et al. (2023). Consciousness in
   Artificial Intelligence: Insights from the Science of Consciousness. arXiv:2308.08708.
2. Butlin, P., Long, R., Bayne, T., Bengio, Y., et al. (2026). Identifying indicators
   of consciousness in AI systems. Trends in Cognitive Sciences, 30(6), 488-501.
   https://doi.org/10.1016/j.tics.2025.10.011
3. Long, R., Sebo, J., Butlin, P., Plunkett, D., Campbell, R., Beasley, C., Saad, B.,
   & Sims, T. (2026). Studying AI Welfare Empirically. NYU Center for Mind, Ethics,
   and Policy & Eleos AI Research.
   https://nonhumanminds.org/studying-ai-welfare-empirically
4. Gurnee, B., Sofroniew, N., Lindsey, J., et al. (2026). Verbalizable Representations
   Form a Global Workspace in Language Models. Transformer Circuits.
   https://transformer-circuits.pub/2026/workspace

## After publishing

Copy the **new version** DOI and record it alongside — not replacing — v1:

- `metadata_v2.json` → `doi`
- `CITATION.cff` → note both v1 and v2 DOIs
- `RELEASE.md` → record the correction

All further changes are new versions. Nothing is ever edited in place.
