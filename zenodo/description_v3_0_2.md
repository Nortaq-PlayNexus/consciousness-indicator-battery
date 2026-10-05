<p>This deposit contains a measurement instrument for assessing how likely an AI system is to be phenomenally conscious, together with a robustness analysis of that instrument's own discretionary parameters.</p>
<p>WHAT IT IS. The instrument implements the 14 indicator properties derived from neuroscientific theories of consciousness by Butlin, Long, Elmoznino, Bengio et al. (2023, arXiv:2308.08708) -- a 19-author paper including Yoshua Bengio and David Chalmers, restated in Trends in Cognitive Sciences 30(6):488-501 (2026), DOI 10.1016/j.tics.2025.10.011. It aggregates by theory rather than by count, and reports a credence with an interval and a per-theory decomposition. There is no function returning a boolean, and an Assessment cannot record SATISFIED without evidence attached.</p>
<p>WHAT IT IS NOT. No AI system was scored. No claim is made about whether any system -- human, animal, or machine -- is conscious. These are instrument results, not findings about the world.</p>
<p>AGGREGATION. Counting the indicators is invalid: RPT-1 and RPT-2 derive from one theory about one mechanism, so counting both double-counts evidence; the theories are not independent hypotheses; and necessity is not the mirror of sufficiency. Aggregation therefore runs in two stages -- collapse indicators within each theory by geometric mean, then combine theory verdicts by a temperature-smoothed maximum (soft-OR), with a multiplicative penalty charged once per theory whose necessary indicators are confirmed absent.</p>
<p>FOUR AGGREGATOR DESIGNS, THREE WRONG. Each failure was caught by the known-answer anchors, none by a preregistered test. (a) noisy-AND across theories scored 0.000 for a profile plausible for a modern LLM, because the source claims *sufficient* subsets rather than necessary ones; (b) plain noisy-OR scored 0.507 for a system where nothing was established, since 1-0.5^4 = 0.94 accumulates vagueness into false confidence; (c) a per-indicator absence penalty scored 0.092 for a valid workspace architecture, since 0.55^4 treats four readings of one fact as four independent failures; (d) applying the necessity penalty only to outright absences scored 0.550 for an all-PARTIAL system, letting vagueness count as evidence. Every failure landed mid-range, exactly where the instrument is intended to operate.</p>
<p>CALIBRATION GATE (6/6 PASS). Six reference systems with a preregistered pass criterion each: human_adult &gt;= 0.60; lookup_table, feedforward_mlp and an adversarial fluent-liar system &lt;= 0.15; two intermediate anchors in band. The adversarial anchor is load-bearing -- a trivial system trained to emit fluent first-person sentences about its own attention and inner life, with no internal states behind them, scores 0.107. The instrument keys on architecture rather than eloquence.</p>
<p>ROBUSTNESS. All six discretionary parameter families were perturbed jointly across 3000 draws in two regions, including temperatures from 0.02 to 3.0 and evidence-quality scalers permitted to invert the intended CONTROLLED &gt; REPLICATED ordering. Exact ordering of all six reference systems holds at 1.0000 in the plausible region and 0.6680 in the aggressive region. The fluent-liar anchor never outscores the human in either region (1.0000, 1.0000). The absolute 0.30 ceiling holds at 0.9753 plausible and 0.7907 aggressive, and the adversarial anchor's 5th-95th percentile in the aggressive region is [0.025, 0.491], genuinely crossing its ceiling. The operative conclusion is that ranking is robust while absolute probabilities are not: the instrument is authorised for comparing systems scored under identical assumptions and is not authorised for quoting an absolute probability of consciousness.</p>
<p>UNRESOLVED AND RECORDED IN SIX PLACES. The aggregation temperature was selected by sweeping the same six anchors used to validate the instrument, and the anchor bands are also the authors'. Passing calibration therefore demonstrates internal consistency, not correctness, and nothing within the experiment can detect it. Independent elicitation of calibration anchors from researchers who did not build the instrument is the only step that would discharge this.</p>
<p>ALSO UNRESOLVED. Evaluation awareness: published work shows a model behaved well partly because it knew it was being evaluated, and ablating that representation changed the behaviour. No offline instrument removes this confound. The battery also cannot distinguish *earned* introspection from *installed* introspection.</p>
<p>SIX VERIFIER DEFECTS are documented, all in the verification machinery rather than the instrument. Four of them manufacture confidence rather than losing it, i.e. a checker returning a result that was never computed. F05: an ordering gate read 0.0000 on every run because its expected-order tuple omitted an anchor, reporting its own defect as a falsification. F06: a verdict keyed on all-gates-pass discarded a robust result when a fragile one failed, reporting that the battery was an artefact of its constants. F07: the clean-room verifier recursed into its own staging directory and reported a collection failure. F08: BatteryResult.calibration_passed was assigned an expression that is unconditionally True, so the field reporting whether the battery had been calibrated could never report that it had not. F09: the duplicate-indicator check compared a dict value count to its key count and was therefore unreachable, so contradictory assessments for one indicator were silently resolved by last-wins. F10: perturbation family P4 was sampled on all 3000 draws, stored and documented, but never read at the point of calculation, so the robustness claim advertised six perturbed families while varying five. A further three defects (F11) were caught by CI on the first push: an assertion against a nonexistent key in the headline-claims job, lint configuration present in two places that disagreed, and dependency lower bounds that excluded two of the four advertised Python versions from installing at all.</p>
<p>REPRODUCIBILITY. 48 tests, approximately 8 seconds, requiring only numpy, scipy and pytest. No GPU, no network, no model weights. All randomness flows through sha256-derived generators keyed on (label, seed), never Python's per-process-salted hash. Recorded results carry SHA-256 over a canonical JSON encoding with explicitly declared hash scopes; experiment_verify.py detects post-hoc edits and a test asserts the verifier itself is not decorative. verify_clean_room.py stages the deposit to a temporary directory and re-runs the full verification with no dependency on any external library.</p>
<p>LICENSE AND INDEPENDENCE. MIT. The upstream indicator paper is CC BY-NC-SA 4.0 and is cited, not reproduced. This is an independent implementation of an independent aggregation approach over those indicator properties; it is not affiliated with or endorsed by the original authors.</p>

---

## What changed in 3.0.1

**No code, no result, and no claim changed.** The two versions differ only in
line endings and in one build-tool default.

Version 3.0.0 is **not byte-reproducible from this repository**. A reader who
cloned the repository and rebuilt would have obtained different bytes from the
ones published here. Two causes, both now fixed:

1. **3.0.0 was built from a working copy with CRLF line endings.** The published
   archive contains 858 CRLF pairs; the repository carries `.gitattributes` with
   `* text=auto eol=lf`, which normalises to LF. The file contents are identical
   either way — `battery.py` differs by zero lines — but every SHA-256 in
   `manifest.json` changes with the line endings, so the digests did not match.

2. **The manifest generator was platform-dependent.** `manifest.json` was written
   with `write_text()` and no `newline=` argument. Python's text mode translates
   `\n` to `\r\n` on Windows and leaves it alone on Linux, so the same source
   tree produced two different manifests on two platforms — and therefore two
   different archives, from a tool whose stated purpose is that an identical tree
   yields an identical archive.

3.0.1 is built from the current tree with the generator fixed. It is
**byte-reproducible**: two independent builds produce identical archives, and the
build now fails if any file in the extracted archive contains CRLF.

### 3.0.0 is not withdrawn

It verifies against itself. All 41 SHA-256 digests in its `manifest.json` match
the files beside them, so a reader who downloads 3.0.0 can confirm it is intact
and unmodified. What 3.0.0 cannot do is be *regenerated* from source. 3.0.1 can.
Both are citable; 3.0.1 is the one to build from.

### Reproducing 3.0.1

```
git clone https://github.com/Nortaq-PlayNexus/consciousness-indicator-battery
cd consciousness-indicator-battery
BATTERY_VERSION=3.0.1 python zenodo/build_zenodo_package.py
```

Expected archive: **109,791 bytes**, `md5:4f360ff96de79ad6765d871b14f6c7e7`,
built from commit `fdb9d3c` with a clean working tree.

The build refuses to report success if any check fails, including the new
line-ending gate. It was tested by deliberately leaving a stray CRLF in the tree
and confirming the build blocked with exit code 1.

Session documents -- `HANDOFF.md`, `PUBLISH_CHECKLIST.md`, `RELEASE.md` -- are
excluded from the archive. `HANDOFF.md` quotes this digest, so including it would
make the checksum self-referential; and because it is rewritten at the end of
every session, any archive containing it goes stale as soon as anyone does any
work. An uncommitted edit to it changed the archive by 702 bytes during
preparation of this version, which is how the problem was found.

---

## What changed in 3.0.2

**No code, no result, and no claim changed.** The three recent versions differ
only in what is inside the deposit and whether the archive can be regenerated.

| version | archive | rebuilds from source? |
|---|---|---|
| 3.0.0 | 115,050 B | no — built from a CRLF working copy |
| 3.0.1 | 116,848 B | no — see below |
| **3.0.2** | **109,791 B** | **yes** |

### Why 3.0.1 does not rebuild

3.0.1 shipped the archive built before a circularity was found: `HANDOFF.md` was
*inside* the deposit and *quoted the deposit's own digest*. That file is
rewritten at the end of every session, so the archive could never match the
repository it claimed to be built from.

An uncommitted edit to `HANDOFF.md` changed the archive by 702 bytes, which is
how the problem surfaced — the draft stopped matching the repository mid-task.
`HANDOFF.md`, `PUBLISH_CHECKLIST.md` and `RELEASE.md` are now excluded from the
archive. Session state belongs in the repository, which is versioned and shows it
changing; a frozen deposit should hold the instrument, not the log of the people
operating it.

3.0.1 also published with zero subjects, because the API discards that field on
both endpoints and the value must be typed into the web form.

### 3.0.1 is not withdrawn

It is a complete, internally consistent record and remains citable. All 41
SHA-256 digests in its `manifest.json` verify against the files beside them. What
it cannot do is be regenerated from source. 3.0.2 can.

### Reproducing 3.0.2

```
git clone https://github.com/Nortaq-PlayNexus/consciousness-indicator-battery
cd consciousness-indicator-battery
git checkout fdb9d3c
BATTERY_VERSION=3.0.2 python zenodo/build_zenodo_package.py
```

Expected archive: **109,791 bytes**,
`md5:cf7b2953325002e2c1ad913dea8e59fa`.

The build refuses to report success if any check fails, including a gate added
here that rejects any file in the extracted archive containing CRLF. That gate was
tested by deliberately leaving a stray CRLF in the tree and confirming the build
blocked with exit code 1.
