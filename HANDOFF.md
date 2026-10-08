# HANDOFF — read this first in a new session

**Written 2026-10-03, corrected 2026-10-04. Authored for whoever picks this up
next, including an AI assistant with no memory of the session that produced it.**

Everything here was learned the hard way. Most of it cost a bug, a wasted
deposit, or a near-miss. If you change nothing else, preserve the following.

---

## 0. STANDING RULE — only create a deposit when it is ready to publish

**Stated by the maintainer, 2026-10-04: "only ever have posts drafts are if
there ready for me to post from now on okay."**

A draft is not a scratchpad. When a draft exists, the maintainer is expected to
publish it, so creating one asserts that everything behind it is final.

**Before creating any draft, all of these must be true:**

| gate | check |
|---|---|
| working tree clean | `git status --porcelain` empty — a cloner must get these bytes |
| tree is committed and pushed | the draft must match a commit anyone can fetch |
| archive built from that clean tree | not from a tree with pending edits |
| archive built twice, digests equal | reproducibility is the product's whole claim |
| digest recorded in metadata, and re-checked | a copied digest from another version is wrong — `manifest.json` records the version, so each version has its own digest |
| concept linkage verified | parent concept, not a new fork |
| description final | including the change note for this version |
| subjects and version note written down | for pasting into the web form, since the API discards both |

**After creating a draft, freeze the inputs.** Do not commit further changes to
files that go into the archive until the draft is published or explicitly
withdrawn. Say plainly that the draft is ready and then stop touching it.

### Why this rule exists

v3.0.1 (`10.5281/zenodo.23137224`) is a published record whose description claims
the archive "rebuilds byte-for-byte from the repository", and that is false of the
archive it shipped.

Sequence, exactly:

1. Draft `23137224` was staged with archive `md5:726b7584…`, built from a tree
   that had an **uncommitted** edit to `HANDOFF.md`.
2. Work continued. The commit landed, `HANDOFF.md` and `PUBLISH_CHECKLIST.md`
   were excluded from the archive as self-referential, and the correct archive
   became `md5:4f360ff9…` — 702 bytes different.
3. The maintainer published `23137224` during that window.
4. The published record was immutable, carried the superseded bytes, and made a
   false claim about itself.

The draft was not ready when it was created: it was built from a dirty tree. Every
gate above would have caught it. The maintainer is right that the rule belongs on
the creator, not on them.

`23137224` cannot be edited or deleted. The correction is v3.0.2
(`https://zenodo.org/deposit/23150723`), which supersedes it under the same
concept `23101902`.

---

## 1. What exists

| Project | Location | GitHub | Zenodo |
|---|---|---|---|
| consciousness-indicator-battery | `C:\Users\natha\AI_RESEARCH\consciousness-indicator-battery` | `Nortaq-PlayNexus/consciousness-indicator-battery` | published **v3.0.2 `10.5281/zenodo.23150723`**, concept `10.5281/zenodo.23101902` |
| phantom_vision_lab | `C:\Users\natha\code\phantom_vision_lab` | `Nortaq-PlayNexus/phantom_vision_lab` | published **v2 `10.5281/zenodo.23123095`**, concept `10.5281/zenodo.23112115` |
| ScientificDiscoveryLab | git copy `C:\Users\natha\AI_RESEARCH\ScientificDiscoveryLab`; **source of truth** `C:\Users\natha\ScientificDiscoveryLab` | `Nortaq-PlayNexus/ScientificDiscoveryLab` | published **v2 `10.5281/zenodo.23122787`**, concept `10.5281/zenodo.23109116` |

**All CI green.** Battery 48 tests. Phantom Vision Lab 28 tests, 5 jobs. Lab 543
tests, 5 jobs, 20 expected excluded-data failures.

### Fifteen records published — verified by API read-back 2026-10-08

**All published and verified against the live Zenodo API**, not against a publish
click. This section previously said the three umbrella records were staged drafts
awaiting a publish click, and later said battery v3.0.1 was still `unsubmitted`.
Both were true when written and stopped being true. The battery is now at
**v3.0.2**, and a fifteenth record exists that no document here mentioned.
`PUBLICATION_VERIFICATION.md` in the laboratory repository remains the record of
truth for the twelve of 2026-10-04.

| Record | Version | DOI | Published |
|---|---|---|---|
| battery | **3.0.2** | `10.5281/zenodo.23150723` | 2026-10-05 |
| battery (superseded) | 3.0.1 | `10.5281/zenodo.23137224` | 2026-10-04 |
| battery | 3.0.0 | `10.5281/zenodo.23122664` | 2026-10-03 |
| ScientificDiscoveryLab | 2.0.0 | `10.5281/zenodo.23122787` | 2026-10-03 |
| phantom vision lab | 2.0.0 | `10.5281/zenodo.23123095` | 2026-10-03 |
| speckle contrast law | 1.0.0 | `10.5281/zenodo.23132744` | 2026-10-04 |
| vortex density | 1.0.0 | `10.5281/zenodo.23132746` | 2026-10-04 |
| discrete vortex detection bias | 1.0.0 | `10.5281/zenodo.23132748` | 2026-10-04 |
| topology-measurement definition | 1.0.0 | `10.5281/zenodo.23132753` | 2026-10-04 |
| RNG certification | 1.0.0 | `10.5281/zenodo.23132759` | 2026-10-04 |
| percolation thresholds and exponents | 1.0.0 | `10.5281/zenodo.23132761` | 2026-10-04 |
| Feigenbaum universality | 1.0.0 | `10.5281/zenodo.23132763` | 2026-10-04 |
| prime gap statistics | 1.0.0 | `10.5281/zenodo.23132767` | 2026-10-04 |
| water acoustic response | 1.0.0 | `10.5281/zenodo.23132771` | 2026-10-04 |
| **COSMOS test suite** | **0.1.0** | `10.5281/zenodo.23204768` | 2026-10-07 |

**Subjects: 0 of 15.** Confirmed by read-back on every record. Zenodo's API
accepts the field, reports success and stores nothing; the web form did not take
them either, and published records are immutable. This is now permanent for all
fifteen. Fixing it means a new version of each with subjects typed into the form.
See D2 in `PUBLICATION_VERIFICATION.md`.

**Version notes: absent on all 15**, same cause.

### Battery version history — which to cite

Cite **v3.0.2** (`10.5281/zenodo.23150723`). No code, result, or claim differs
across any of these; they differ only in what the deposit contains and whether
it can be regenerated from the repository.

| version | DOI | rebuilds byte-for-byte? | note |
|---|---|---|---|
| 1.0.0 | `10.5281/zenodo.23101903` | no | references published as 722 one-character array entries |
| 2.0.0 | `10.5281/zenodo.23111535` | no | metadata-only correction of v1 |
| 3.0.0 | `10.5281/zenodo.23122664` | no | CRLF working copy; platform-dependent manifest generator |
| 3.0.1 | `10.5281/zenodo.23137224` | **no — see below** | superseded; do not cite |
| **3.0.2** | **`10.5281/zenodo.23150723`** | **yes** | **cite this one** |

v3.0.1's description claims the archive rebuilds byte-for-byte from the
repository, and that is false of the archive it shipped, because the draft was
built from a tree with an uncommitted edit. It is immutable and cannot be
corrected in place. v3.0.2 exists solely to correct that claim. See section 0.

### COSMOS test suite

`10.5281/zenodo.23204768`, v0.1.0, published 2026-10-07, **GPL-3.0**, repository
`Nortaq-PlayNexus/COSMOS-TEST-SUITE`, CI green. This record was not tracked in any
status document in any of these repositories until it was found by API read-back
on 2026-10-08. It is noted here so the next session does not discover it again.
| ScientificDiscoveryLab | 2.0.0 | `10.5281/zenodo.23122787` |
| phantom vision lab | 2.0.0 | `10.5281/zenodo.23123095` |
| speckle contrast law | 1.0.0 | `10.5281/zenodo.23132744` |
| vortex density | 1.0.0 | `10.5281/zenodo.23132746` |
| discrete vortex detection bias | 1.0.0 | `10.5281/zenodo.23132748` |
| topology-measurement definition | 1.0.0 | `10.5281/zenodo.23132753` |
| RNG certification | 1.0.0 | `10.5281/zenodo.23132759` |
| percolation thresholds and exponents | 1.0.0 | `10.5281/zenodo.23132761` |
| Feigenbaum universality | 1.0.0 | `10.5281/zenodo.23132763` |
| prime gap statistics | 1.0.0 | `10.5281/zenodo.23132767` |
| water acoustic response | 1.0.0 | `10.5281/zenodo.23132771` |

**Subjects: 0 of 12.** The web form did not take them either, and published
records are immutable, so this is now permanent for all twelve. Fixing it means a
new version of each with subjects typed into the form. See D2 in
`PUBLICATION_VERIFICATION.md`.

### ~~One record still staged: battery v3.0.1~~ — superseded, see above

This section previously said v3.0.1 (`23137224`) was `unsubmitted` with no DOI
minted. **It was published on 2026-10-04 and is superseded.** v3.0.2 was published
on 2026-10-05. Both are immutable. Do not cite v3.0.1.

The byte-reproducibility work described below was real and did land: v3.0.2's
archive (109,791 B, `md5:cf7b2953325002e2c1ad913dea8e59fa`) does rebuild
byte-for-byte, and the manifest generator now pins `newline=""`.

### Not published, and why

| Directory | Why |
|---|---|
| `C:\Users\natha\code\EXP0008` | `FALSIFICATION_RECORD.md` finds the headline claims are **hand-authored** — `restore_csvs.py` writes them as string literals. Publish the null results only. |
| `C:\Users\natha\code\string-theory-questions` | Never independently verified. |
| `C:\Users\natha\code\coherent-optical-ai-sandbox` | **Already published** as `10.5281/zenodo.22849652`. Do not re-upload. 1.4 GB folder, only **142 MB real** — `.venv` 1.3 GB, `.pyc` 222 MB. |
| `C:\Users\natha\code\dmt-laser-s9-battery` | Already inside the lab at `AUDIT/S9_PROVENANCE_20260924/`, classified `SYNTHETIC_DERIVED_OUTPUT_NOT_EMPIRICAL_EVIDENCE`. |

---

## 2. Zenodo API — every trap, verified

**The most valuable part of this document.** The API accepts fields it does not
store, and reports success. Nothing warns you.

### Creating a new version — CORRECTED 2026-10-04

An earlier version of this file said Zenodo could not create a version
programmatically. **That was wrong.** Two APIs live under `/api/`:

| endpoint | result |
|---|---|
| `POST /api/deposit/depositions/<id>/actions/new_version` | **404** |
| `POST /api/deposit/depositions` with `metadata.conceptrecid` | 200, field **ignored**, draft lands on a *different concept* |
| **`POST /api/records/<id>/versions`** | **201, concept correctly linked** |

Use the third. Every example online uses the legacy one, which is why this cost
time.

`zenodo/new_version.py` (in all three repos) does it, and **verifies the linkage
before uploading anything** — it aborts if the draft's concept does not match the
parent's.

Note: the parent's `conceptrecid` is **not** the parent's own id. The battery's
record 23111535 has concept `23101902`. Using the record id there would silently
create a disconnected version.

### Fields accepted and silently discarded

Verified by read-back on three separate deposits:

| Field | Behaviour |
|---|---|
| `subjects` | accepted, success reported, **not persisted** |
| `version_note` | same |
| `conceptrecid` (legacy endpoint) | same |
| any partial metadata payload | **destroys every other field** |

### `references` — two distinct failure modes, both observed

- A **single concatenated string** → Zenodo iterates it into 722 one-character
  entries. This was battery v1's defect.
- A **list of objects** (`{id, type, title, citation}`) → **silently dropped**,
  0 stored. This hit the lab.

Both are wrong. It must be a **list of plain strings**. `new_version.py` flattens
objects to their citation string.

### `communities`

Must be `{"identifier": ...}`. A bare string or a `{"id": ...}` dict is rejected
with a 400 — and because the PUT is all-or-nothing, that rejection discards the
description, notes and references sent in the same request.

### PUT is a FULL REPLACEMENT, not a merge

Sending `{"metadata": {"version_note": "..."}}` wiped a draft's title,
description, notes, creators, keywords, version, and licence. The licence
silently reverted to Zenodo's default `cc-by-4.0`. It replied **"accepted"**.

**Never send a partial metadata PUT.** Guard: `zenodo/put_metadata_safely.py`
validates locally, rejects `cc-by-4.0` as the signature of a wiped record, and
compares field-by-field after sending.

### Description read-back needs HTML unescaping

Zenodo escapes `>` → `&gt;` when storing a description. A byte comparison always
fails. Found via a 13021-vs-13019 diff that was twelve escaped blockquote markers
and nothing else. Unescape before comparing, or a real difference hides in noise.

### Other specifics

- All fields nested under a `metadata` key. A flat payload is rejected with
  `"Unknown field"` once per key.
- Create: `POST /api/deposit/depositions` with **only** `{"metadata": {}}`. A
  sibling `bucket` key is rejected.
- Upload: **`PUT`** to `{bucket}/{filename}` with
  `Content-Type: application/octet-stream`. POST to the bare bucket → 405;
  `application/zip` → 415.
- Uploads can abort mid-transfer on a large archive. Retry transient failures;
  never retry 4xx.

### Token

`C:\Users\natha\ScientificDiscoveryLab\zenodo\.zenodo_token` — one token, all
deposits. Git-ignored. Regenerate at
`https://zenodo.org/account/settings/applications/tokens/new`.

### NEVER delete a deposit

The maintainer has said so explicitly. Discarding one is their decision.

`23110728` is a known-dead draft: `[UNUSABLE DRAFT]` in its title, no files, wrong
concept, notes explaining itself. Leave it or delete it yourself. **Do not create
another.**

---

## 3. Rules learned here

### A gate that cannot fail is worse than no gate

Three cases, all of which reported success while verifying nothing:

1. A CI step grepped `FAILED` lines for exception text. Those lines contain only
   node ids. 20 failures sat unexamined.
2. A script read UTF-8 when the writer produced UTF-16. Zero lines parsed, which
   looks like a clean run.
3. A documentation check excluded a section whose heading sat near the top of the
   file, truncating it to its opening paragraph.

**Every check needs a negative test** — inject the defect, confirm the check
fires. Two of the three were caught only because someone wrote one.

### A commit message claiming a fix is not the fix

The lab's v2 version note said "byte-identical to v1" when it was a rebuild of a
newer tree. A commit message asserted the correction had been made. It had not.
Re-read the claim instead of trusting the commit.

### If two files disagree, find out which is which

The battery's three files disagreed on one number. The live Zenodo API settled it
in one call — the record was published and the checkpoint note was stale.
**Verify against the source of truth before reasoning from a summary.**

### Do not run a staging script from inside its destination

`build_publishable.py --dest .` wipes the tree it is standing in. Twice. It
preserves `.git` and `zenodo-deposit`, nothing else. Always run it from the source
of truth: `C:\Users\natha\ScientificDiscoveryLab`.

### Documentation claiming what the code lacks

Phantom Vision Lab's README advertised "Blind Experiment Mode"; `blind` appeared
nowhere in the source. Also "15 pattern types" when there were 16 — and the same
sentence listed 16. And a `## License` section holding a disclaimer, with no
LICENSE file. Two are now enforced by tests, including a negative test proving the
enforcement fires.

### Determinism means cross-process

Calling the generator twice inside one process cannot catch a module-level RNG, a
lazily-initialised global, or a `PYTHONHASHSEED` dependence.

---

## 4. Before publishing anything else

- [ ] Read the project's own limitations section, and believe it
- [ ] Grep for `TODO`, `FIXME`, `hardcoded`, `_BACKUP`, `fix_`, `restore_`
- [ ] Check for post-hoc data repair. If results were patched after generation,
      the seed→result chain is broken and that must be disclosed
- [ ] Confirm every headline number is *computed*, not a literal
- [ ] Run tests in a clean checkout, not your working directory
- [ ] Byte-verify the archive against what the server stored
- [ ] **Set every metadata field before publishing**

---

## 5. Quick reference

```
verify a published record (no auth needed):
  https://zenodo.org/api/records/<id>

list your deposits:
  GET https://zenodo.org/api/deposit/depositions      (Bearer token)

create a new version:
  python zenodo/new_version.py <record-id> --metadata <f> --description <f> --archive <zip>
  # add --dry-run to validate without sending

rebuild + verify an archive:
  python zenodo/build_zenodo_package.py --out <zip> --verify
```

**If you are an AI assistant reading this:** Zenodo will accept fields it does not
store, and a partial PUT will delete everything else while reporting success. Do
not trust a success response. Read the record back. If two sources disagree,
query the live API rather than reasoning from a file. The user prefers to be asked
before anything irreversible, and does not want deposits deleted.

---

## Working-copy locations — do not use %TEMP%

| Repository | Location |
|---|---|
| consciousness-indicator-battery | `C:\Users\natha\AI_RESEARCH\consciousness-indicator-battery` |
| phantom_vision_lab | `C:\Users\natha\code\phantom_vision_lab` |
| ScientificDiscoveryLab (git) | `C:\Users\natha\AI_RESEARCH\ScientificDiscoveryLab` |
| ScientificDiscoveryLab (source of truth) | `C:\Users\natha\ScientificDiscoveryLab` |

The battery repository lived at
`C:\Users\natha\AppData\Local\Temp\opencode\cib-clean` until 2026-10-04, when
**that directory was cleared and the working copy was lost.** It was recovered by
cloning from GitHub — no committed work was lost — but uncommitted work would
have been, and a Zenodo working directory is not the place for that.

The twelve records published on 2026-10-04 live on Zenodo's servers and were never
at risk. So is battery v3.0.1 (draft `23137224`, still unsubmitted).

**Never keep a working copy under `%TEMP%`.** See `zenodo/PUBLISH_v3_0_1.md` for
the one record still awaiting a publish click.
