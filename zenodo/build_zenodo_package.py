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
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ZENODO = ROOT / "zenodo"
PACKAGE = ZENODO / "package"

#: Version is read from the environment rather than hardcoded, because getting it
#: wrong is silent and expensive: Zenodo files are immutable, so an archive named
#: v1.0.0 uploaded as version 2.0.0 produces a record whose filename contradicts
#: its own metadata, and the only remedy is a third version. There was no such
#: protection when 2.0.0 was built with VERSION still hardcoded at 1.0.0.
VERSION = os.environ.get("BATTERY_VERSION", "1.0.0")
ARCHIVE = ZENODO / f"consciousness-indicator-battery-v{VERSION}.zip"

NAME = "consciousness-indicator-battery"

EXCLUDE_DIRS = {
    ".git", ".github", "__pycache__", ".pytest_cache", ".venv", "venv",
    "build", "dist", "zenodo", ".ruff_cache", ".mypy_cache",
}
EXCLUDE_SUFFIX = {".pyc", ".pyo", ".zip"}
#: `manifest.json` is generated during staging.
EXCLUDE_NAMES = {"manifest.json"}
#: RELEASE.md records the archive's own SHA-256. Including it in the archive
#: makes the checksum self-referential: writing the hash into the file changes the
#: file, which changes the hash, which invalidates the value just written. It is
#: release-management state rather than part of the deposit, so it stays in the
#: repository and out of the archive.
EXCLUDE_FROM_ARCHIVE = {"RELEASE.md"}


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
        if rel.name in EXCLUDE_NAMES or rel.name in EXCLUDE_FROM_ARCHIVE:
            continue
        if src.suffix in EXCLUDE_SUFFIX:
            continue
        if not src.is_file():
            continue
        target = PACKAGE / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
        staged.append(str(rel).replace("\\", "/"))

    # No build timestamp. It made the archive non-reproducible byte-for-byte, so
    # the SHA-256 recorded in RELEASE.md went stale every time the script ran —
    # which defeats the point of recording a checksum for an archive whose files
    # are immutable once uploaded. Every input here is either a committed file or
    # a deterministic function of one, so an identical tree must produce an
    # identical archive.
    manifest = {
        "name": NAME,
        "version": VERSION,
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
    # newline="\n" is load-bearing, not decoration. Without it, Python's text mode
    # translates "\n" to "\r\n" on Windows and leaves it alone on Linux, so the
    # same source tree produces two different manifests on two platforms -- and
    # therefore two different archives, from a tool whose entire claim is that an
    # identical tree yields an identical archive.
    #
    # This was not theoretical. The v3.0.0 archive carried a CRLF manifest.json,
    # which is one reason it does not rebuild from the repository: a rebuild here
    # and a rebuild on Linux would each disagree with what was published, in
    # different ways.
    (PACKAGE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return staged


def build_zip() -> int:
    """Build the archive byte-reproducibly.

    Two things otherwise vary between runs on identical input:

    - zip entries embed the source file's mtime, and `shutil.copy2` preserves it,
      so a plain `write()` would carry whatever timestamp each file happened to
      have;
    - entries are written in filesystem order, which is not guaranteed stable.

    Both are pinned here: a fixed epoch for every entry, and an explicit sort.
    The result is that the SHA-256 recorded in RELEASE.md stays valid across
    rebuilds, which matters because Zenodo files cannot be replaced once
    published.
    """
    # 1980-01-01 is the earliest timestamp the zip format can represent.
    fixed_date = (1980, 1, 1, 0, 0, 0)
    if ARCHIVE.exists():
        ARCHIVE.unlink()
    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(PACKAGE.rglob("*"), key=lambda p: str(p.relative_to(PACKAGE))):
            if not path.is_file():
                continue
            info = zipfile.ZipInfo(
                filename=f"{NAME}/{path.relative_to(PACKAGE).as_posix()}",
                date_time=fixed_date,
            )
            # 0o644 regular file; matches what a clean checkout produces on any
            # platform, so the archive does not encode the build machine's umask.
            info.external_attr = (0o100644 & 0xFFFF) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, path.read_bytes())
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
        # Line endings first, because it is the failure that actually shipped:
        # v3.0.0 went out with 858 CRLF pairs and does not rebuild from the repo.
        # A stray CRLF from any editor changes every digest in the manifest, so
        # the gate runs on the extracted archive rather than the working tree --
        # what matters is what a reader downloads.
        steps = [
            (
                "no CRLF in any archive entry",
                [
                    sys.executable, "-c",
                    "import pathlib,sys\n"
                    "bad=[p for p in sorted(pathlib.Path('.').rglob('*')) "
                    "if p.is_file() and b'\\r\\n' in p.read_bytes()]\n"
                    "print(str(len(bad)) + ' file(s) contain CRLF: ' + "
                    "', '.join(str(p) for p in bad[:5]))\n"
                    "sys.exit(1 if bad else 0)\n",
                ],
            ),
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
