# PREREGISTRATION — EXP-C002

## Hypothesis

HYP-C002: A small open-weights decoder (Qwen2.5-0.5B) scored via the
consciousness-indicator-battery, with GWT-2/3/4 indicators fed by jacobian-lens
J-space measurements (transported residual-stream activations decoded into
vocabulary), will produce a credence strictly below the calibration ceiling for
negative anchors (<=0.15) IF the battery's gating logic correctly rejects
systems that merely produce fluent text without genuine global broadcast.

## Design

- Model: Qwen/Qwen2.5-0.5B (open weights, fits on 8GB VRAM)
- Measurements: jacobians J_l over a generic web-text corpus; decode transported
  activations at each layer/position.
- Indicators scored: GWT-1..4 (from J-space broadcast signatures), plus RPT-1..3,
  HOT-1..3, AST-1 where measurable from architecture.
- UNTESTED for indicators requiring white-box internals not exposed by jlens.

## Calibration gate

Battery must pass calibrate_known_answers() (6/6) before any credence is reported.

## Falsification

- If the model scores >0.15 credence, the battery fails F3 (fluency masquerading
  as architecture) — a real result, not a failure of the experiment.
- If any indicator marked SATISFIED lacks controlled evidence, the assessment
  dataclass raises ValueError (built-in gate).

## Non-goals

- No claim about whether the model is conscious.
- No boolean output.
- No moral conclusion.

## Status

Scaffolded 2026-10-31. Preregistered before execution.
