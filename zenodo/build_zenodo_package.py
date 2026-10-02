#!/usr/bin/env python3
"""Build the Zenodo deposit archive and verify its contents before upload.

Zenodo files are immutable once published, so the archive is verified here rather
than after. This script:

  1. stages the publishable tree into zenodo/package/
  2. writes manifest.json with a SHA-256 for every file
  3. builds the zip
  4. extracts to a scratch dir and runs the full test suite + hash verification
     against the extracted copy

Run from the repository root:

    python zenodo/build_zenodo_package.py

Exit code 0 means the archive is safe to upload.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZENODO = ROOT / "zenodo"
PACKAGE = ZENODO / "package"
ARCHIVE = ZENODO / "consciousness-indicator-battery-v1.0.0.zip"

VERSION = "1.0.0"
NAME = "consciousness-indicator-battery"

EXCLUDE_DIRS = {
    ".git", ".github", "__pycache__", ".pytest_cache", ".venv", "venv",
    "build", "dist", "zenodo", ".ruff_cache", ".mypy_cache",
}
EXCLUDE_SUFFIX = {".pyc", ".pyo", ".zip"}
EXCLUDE_NAMES = {"manifest.json"}


def sha256_file(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def stage() -> list[str]:
    if PACKAGE.exists():
        shutil.rmtree(PACKAGE)
    PACKAGE.mkdir(parents=True)

    staged: list[str] = []
    for src in sorted(ROOT.rglob("*")):
        rel = src.relative_to(ROOT)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        if rel.name in EXCLUDE_NAMES or src.suffix in EXCLUDE_SUFFIX:
            continue
        if not src.is_file():
            continue
        target = PACKAGE / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
        staged.append(str(rel).replace("\\", "/"))

    manifest = {
        "name": NAME,
        "version": VERSION,
        "built_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "file_count": len(staged),
        "note": (
            "SHA-256 per file, exact bytes. The instrument additionally records a "
            "canonical-JSON result hash in RESULTS/; those are computed over "
            "in-memory values, not file bytes, so they differ from the file hashes "
            "here by design."
        ),
        "files": {
            rel: sha256_file(PACKAGE / rel)
            for rel in sorted(staged)
        },
    }
    (PACKAGE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return staged


def build_zip() -> int:
    if ARCHIVE.exists():
        ARCHIVE.unlink()
    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(PACKAGE.rglob("*")):
            if path.is_file():
                zf.write(path, arcname=f"{NAME}/{path.relative_to(PACKAGE)}")
    return ARCHIVE.stat().st_size


def verify_archive() -> list[tuple[str, bool, str]]:
    """Extract the built archive and re-run verification against the extraction."""
    scratch = Path(tempfile.mkdtemp(prefix="zenodo-verify-"))
    results: list[tuple[str, bool, str]] = []
    try:
        with zipfile.ZipFile(ARCHIVE) as zf:
            zf.extractall(scratch)
        work = scratch / NAME

        # The lab-engine parity test is meaningless in an extracted deposit.
        steps = [
            ("test suite", [sys.executable, "-m", "pytest", "-q"]),
            (
                "result hash integrity",
                [
                    sys.executable, "experiment_verify.py",
                    "RESULTS/experiment.json", "RESULTS/experiment_C003.json",
                ],
            ),
            (
                "headline claims reproduce",
                [
                    sys.executable, "-c",
                    "from battery import calibrate_known_answers\n"
                    "from perturbation import compare_regions\n"
                    "cal = calibrate_known_answers()\n"
                    "assert cal.passed, cal.failures\n"
                    "r = compare_regions(seed=0)\n"
                    "assert r['verdict_detail']['load_claim_FB_holds_both']\n"
                    "print('calibration PASS; F-B holds both regions')\n",
                ],
            ),
        ]
        for label, cmd in steps:
            proc = subprocess.run(cmd, cwd=work, capture_output=True, text=True, timeout=900)
            out = [ln for ln in (proc.stdout + proc.stderr).strip().splitlines() if ln.strip()]
            results.append((label, proc.returncode == 0, out[-1] if out else ""))
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    return results


def main() -> int:
    print(f"staging {ROOT.name} -> {PACKAGE.relative_to(ROOT)}")
    staged = stage()
    print(f"  {len(staged)} files, manifest.json written")

    size = build_zip()
    print(f"archive: {ARCHIVE.name} ({size / 1024:.1f} KB)")

    print("\nverifying the EXTRACTED archive (Zenodo files are immutable after publish):")
    results = verify_archive()
    for label, ok, tail in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
        if tail:
            print(f"         {tail.strip()}")

    failed = [label for label, ok, _ in results if not ok]
    print()
    if failed:
        print(f"DO NOT UPLOAD -- {len(failed)} check(s) failed: {', '.join(failed)}")
        return 1

    print("ARCHIVE VERIFIED -- safe to upload to Zenodo")
    print(f"  {ARCHIVE}")
    print("\nNext: push the GitHub repository first (Zenodo-GitHub linking needs a")
    print("public non-empty repo), then follow zenodo/UPLOAD_INSTRUCTIONS.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
