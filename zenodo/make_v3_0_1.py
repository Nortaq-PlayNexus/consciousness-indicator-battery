#!/usr/bin/env python3
"""Derive v3.0.1 metadata and description from the published v3.0.0 set.

    python zenodo/make_v3_0_1.py

v3.0.1 exists for one reason: v3.0.0 is not byte-reproducible from its own
repository, because it was built from a working copy with CRLF line endings and
the manifest generator was platform-dependent. No code differs between the two
versions, so this changes no result and revives no claim.

Metadata is derived from metadata_v2.json rather than retyped, so a field cannot
be quietly dropped between versions. The script asserts that every field carried
over unchanged, and fails loudly if one did not.

Subjects are carried over as data even though the API discards them, so the
values are in one place for the web form. See HANDOFF.md: both endpoints accept
the field, report success and store nothing.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_META = ROOT / "zenodo" / "metadata_v2.json"
SRC_DESC = ROOT / "zenodo" / "description_v2.md"
OUT_META = ROOT / "zenodo" / "metadata_v3_0_1.json"
OUT_DESC = ROOT / "zenodo" / "description_v3_0_1.md"

NEW_VERSION = "3.0.1"
BASE_VERSION = "3.0.0"

#: Fields that must survive the version bump untouched. If one of these differs,
#: the derivation did something other than bump the version, which is the failure
#: mode this script exists to make loud.
MUST_CARRY = (
    "title", "upload_type", "license", "language", "access_right",
    "creators", "keywords", "subjects", "references", "related_identifiers",
)

ARCHIVE = "consciousness-indicator-battery-v3.0.1.zip"
ARCHIVE_BYTES = 116848
ARCHIVE_MD5 = "726b7584f439c46d7da0e89d4ebe03da"

APPENDIX = """
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
   `\\n` to `\\r\\n` on Windows and leaves it alone on Linux, so the same source
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

Expected archive: **116,848 bytes**, `md5:726b7584f439c46d7da0e89d4ebe03da`.

The build refuses to report success if any check fails, including the new
line-ending gate. It was tested by deliberately leaving a stray CRLF in the tree
and confirming the build blocked with exit code 1.
"""


def main() -> int:
    meta = json.loads(SRC_META.read_text(encoding="utf-8"))
    desc = SRC_DESC.read_text(encoding="utf-8")

    if meta.get("version") != BASE_VERSION:
        print(f"  ABORT: expected source version {BASE_VERSION}, "
              f"found {meta.get('version')}")
        print("  Deriving from a different base would silently carry the wrong "
              "metadata forward.")
        return 1

    new = dict(meta)
    new["version"] = NEW_VERSION
    new["archive"] = ARCHIVE
    new["archive_sha256"] = ARCHIVE_MD5
    new["archive_bytes"] = ARCHIVE_BYTES
    new["supersedes"] = "https://doi.org/10.5281/zenodo.23122664"
    new["supersedes_note"] = (
        "3.0.1 exists to restore byte-reproducibility. 3.0.0 remains valid and "
        "citable, and verifies against its own manifest; it simply cannot be "
        "regenerated from source. No code or result differs between them."
    )
    new["version_note_requested"] = (
        "v3.0.1 - rebuilds byte-for-byte from the repository; v3.0.0 does not, "
        "because it was built from a CRLF working copy and the manifest "
        "generator was platform-dependent. No code, result or claim changed. "
        "v3.0.0 remains citable and self-consistent."
    )

    # Fail loudly rather than quietly dropping a field.
    missing = [f for f in MUST_CARRY if f not in new]
    if missing:
        print(f"  ABORT: fields absent from derived metadata: {missing}")
        return 1
    for f in MUST_CARRY:
        if new[f] != meta[f]:
            print(f"  ABORT: {f} changed during derivation")
            return 1

    if "What changed in 3.0.1" not in desc:
        desc = desc.rstrip() + "\n" + APPENDIX

    OUT_META.write_text(
        json.dumps(new, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8", newline="\n")
    OUT_DESC.write_text(desc, encoding="utf-8", newline="\n")

    print(f"  {OUT_META.name}")
    print(f"    version      {meta.get('version')} -> {NEW_VERSION}")
    print(f"    subjects     {len(new['subjects'])} carried over "
          f"(paste into the web form -- the API discards them)")
    print(f"    description  {len(desc)} chars "
          f"(+{len(APPENDIX)} for the change note)")
    print(f"    archive      {ARCHIVE}  {ARCHIVE_BYTES:,} B")
    print(f"\n  carried unchanged and verified: {', '.join(MUST_CARRY)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
