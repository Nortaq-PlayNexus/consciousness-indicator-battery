"""Standalone-environment tests.

The published copy of this repo must pass its tests with ONLY `numpy`, `scipy`
and `pytest` installed — no `04_SHARED_ENGINE` on the path. These tests assert
that, because the standalone fallback RNG has to produce bit-identical streams to
the lab's canonical engine or every recorded hash in RESULTS/ becomes a lie.

Run: pytest -q
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

import _rng
import battery
import perturbation

ROOT = Path(__file__).resolve().parent


def test_rng_is_deterministic():
    a = _rng.rng("t", 0).integers(0, 10**9, size=16)
    b = _rng.rng("t", 0).integers(0, 10**9, size=16)
    assert (a == b).all()


def test_rng_depends_on_label_and_seed():
    assert not ( _rng.rng("a", 0).integers(0, 10**9, size=8)
                 == _rng.rng("b", 0).integers(0, 10**9, size=8) ).all()
    assert not ( _rng.rng("a", 0).integers(0, 10**9, size=8)
                 == _rng.rng("a", 1).integers(0, 10**9, size=8) ).all()


def test_seed_value_matches_documented_contract():
    """sha256("label:seed")[:16] as int — the contract both implementations share."""
    import hashlib

    expected = int(hashlib.sha256(b"q-c003-perturbation:0").hexdigest()[:16], 16)
    assert _rng.seed_value("q-c003-perturbation", 0) == expected


# The lab engine lives at ScientificDiscoveryLab/04_SHARED_ENGINE when this
# project sits inside a lab checkout:
#   ROOT                       = <lab>/03_INVESTIGATIONS/COMPUTATIONAL_SCIENCE/<investigation>
#   ROOT.parents[2]            = <lab>
_LAB_ENGINE = ROOT.parents[2] / "04_SHARED_ENGINE"


@pytest.mark.skipif(
    not _LAB_ENGINE.is_dir(),
    reason="standalone checkout: lab engine not present",
)
def test_fallback_rng_matches_lab_engine_bit_for_bit():
    """If the lab engine is reachable, the two RNGs must agree exactly.

    Otherwise every hash in RESULTS/ would depend on which implementation ran.
    """
    sys.path.insert(0, str(_LAB_ENGINE))
    from engine.utilities.core import rng as lab_rng
    from engine.utilities.core import seed_value as lab_seed

    for label, seed in (("q-c003-perturbation", 0), ("bootstrap-diff", 3), ("x", 42)):
        assert _rng.seed_value(label, seed) == lab_seed(label, seed)
        assert (
            _rng.rng(label, seed).integers(0, 10**9, size=32)
            == lab_rng(label, seed).integers(0, 10**9, size=32)
        ).all()


def test_works_without_lab_engine():
    """The repo must run on a bare install with no lab checkout present."""
    code = (
        "import sys; sys.modules['engine']=None\n"
        "import battery, perturbation\n"
        "r = battery.calibrate_known_answers()\n"
        "assert r.passed, r.failures\n"
        "assert perturbation.compare_regions(seed=0)['verdict_detail']"
        "['load_claim_FB_holds_both']\n"
        "print('OK')\n"
    )
    proc = subprocess.run(
        [sys.executable, "-c", code],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert proc.returncode == 0, proc.stderr
    assert "OK" in proc.stdout


# ------------------------------------------------------------------ hashes


@pytest.mark.parametrize("name", ["experiment.json", "experiment_C003.json"])
def test_recorded_hashes_verify(name):
    """Published results must not have been edited after the run."""
    from experiment_verify import verify_file

    report = verify_file(ROOT / "RESULTS" / name)
    assert report["valid"], report["errors"]


def test_verify_helper_detects_tampering():
    """The verifier must actually catch an edited result, or it is decoration."""
    import copy

    from experiment_verify import verify_experiment_result_hash
    import json

    record = json.loads((ROOT / "RESULTS" / "experiment.json").read_text(encoding="utf-8"))
    tampered = copy.deepcopy(record)
    tampered["result"]["calibration"]["passed"] = "tampered"

    report = verify_experiment_result_hash(tampered)
    assert report["valid"] is False
    assert report["result_hash_valid"] is False
    assert any("mismatch" in e for e in report["errors"])