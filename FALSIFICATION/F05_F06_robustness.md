# F05, F06 — robustness of the EXP-C003 gates

These record the two failures found while running the perturbation experiment.
Both concern the experiment's own gate machinery, not consciousness.

## F05 — `EXPECTED_ORDER` omitted an anchor (FIXED)

**Symptom.** Gate F-A, "full canonical order exact", read **0.0000** in every run
of the plausible region. That looked like a strong falsification: the battery's
ordering collapsed under mild perturbation.

**Actual cause.** `EXPECTED_ORDER` listed five systems. The scored set contains
six — `feedforward_mlp` was missing. The gate sorted all six and compared the
result against a five-element tuple, which can never match.

So F-A was reporting the gate's own structural defect as a falsification of the
battery. A gate that cannot distinguish "the thing failed" from "the test is
broken" is worse than no gate, because it manufactures confident negatives.

**Fix.** Two parts:

1. `EXPECTED_ORDER` corrected to all six systems, with the ordering *rationale*
   written out rather than implied.
2. `run_perturbation` now raises `ValueError` if `EXPECTED_ORDER` does not
   cover exactly the scored system set. A partial order is a hard error.

**Regression test.** `test_expected_order_covers_every_anchor` and
`test_partial_expected_order_raises_rather_than_silently_scoring`.

**After the fix**, F-A reads **1.0000** in the plausible region. The original
"collapse" was entirely an artefact of the broken gate.

**Why this is recorded rather than quietly fixed.** The same class of bug already
bit EXP-C001 three times (per-indicator penalty, default-argument binding,
key-presence test). A fourth instance in a *different* experiment suggests the
real problem is that gate logic is written without a way to check that the gate
itself runs. That is now asserted in both experiments.

## F06 — `all_gates_pass` conflated two different questions (FIXED)

**Symptom.** `compare_regions` returned
`"ORDERING DOES NOT SURVIVE — battery is an artefact of its constants"`.

**Actual cause.** The verdict keyed on `all_gates_pass`, which requires F-A, F-B,
F-C and F-D together. F-B — that a fluent self-reporting system never outscores
the human — held at **1.0000** in both regions. That is the claim the battery
exists to make, and it survived everything. But F-C (adversarial anchor below an
absolute ceiling) failed under aggressive perturbation, so `all_gates_pass` was
False and the summary reported total collapse.

That is misleading in the opposite direction: it discards a robust result in
favour of a fragile one, and would have led a reader to discard the whole
instrument.

**Fix.** The verdict is now computed from the load-bearing gate, with
calibration gates reported separately. Two distinct questions, two distinct
answers:

- **ORDERING / architecture claim** — F-B, robust in both regions.
- **ABSOLUTE calibration** — F-A and F-C, robust in the plausible region only.

**After the fix:**

```
ORDERING ROBUST IN PLAUSIBLE REGION; ABSOLUTES NOT ROBUST
  F-B (fluency cannot beat architecture) HOLDS [1.0000 / 1.0000]
  exact ordering holds under plausible perturbation [1.0000]
  absolute calibration DOES NOT hold under aggressive perturbation
```

`verdict_detail` now carries the conclusion, what it authorises, and what it does
not.

**Standing caveat.** This fix changes a *reported* conclusion, not a measurement.
The underlying numbers are identical in both versions. Recorded here because a
verdict string is part of a result and must not be edited to look better — the
numbers that disagreed are preserved above.

## What neither F05 nor F06 changes

F01 stands. The perturbation experiment bounds how much F01 matters; it does not
resolve it. Even the F-B result is conditional: it holds *given* the anchor
assignments, which are still lab assumptions. Independent expert elicitation
remains the only thing that would discharge F01.