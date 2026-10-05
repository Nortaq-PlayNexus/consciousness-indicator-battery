#!/usr/bin/env python3
"""Derive v3.0.2 metadata and description from v3.0.1.

    python zenodo/make_v3_0_2.py

v3.0.1 (10.5281/zenodo.23137224) was published with the archive built before
the session-document circularity was found, so it does not rebuild from any
commit and has zero subjects. It fails at the one job it existed to do.

v3.0.2 ships the archive that does rebuild:

    109,791 bytes, md5:4f360ff96de79ad6765d871b14f6c7e7
    from commit fdb9d3c, clean working tree, two builds identical

No code, result, or claim differs across v3.0.0, v3.0.1 and v3.0.2. All three
differ only in which documentation and tooling are inside the deposit, and
whether the archive can be regenerated from source.

Metadata is derived from metadata_v3_0_1.json rather than retyped, and the script
aborts if any field would change or if the source version is not 3.0.1.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_META = ROOT / "zenodo" / "metadata_v3_0_1.json"
SRC_DESC = ROOT / "zenodo" / "description_v3_0_1.md"
OUT_META = ROOT / "zenodo" / "metadata_v3_0_2.json"
OUT_DESC = ROOT / "zenodo" / "description_v3_0_2.md"

BASE_VERSION = "3.0.1"
NEW_VERSION = "3.0.2"

MUST_CARRY = (
    "title", "upload_type", "license", "language", "access_right",
    "creators", "keywords", "subjects", "references", "related_identifiers",
)

ARCHIVE = "consciousness-indicator-battery-v3.0.2.zip"
#: Digest of the archive built with BATTERY_VERSION=3.0.2 from commit fdb9d3c
#: with a clean working tree. Two builds of that give this value.
#:
#: Note this is NOT the digest of the 3.0.1 build, which differs. manifest.json
#: records the version, so a different version is a different archive by design --
#: an earlier draft of this file carried the 3.0.1 digest here and the upload-time
#: check caught it.
ARCHIVE_BYTES = 109791
ARCHIVE_MD5 = "cf7b2953325002e2c1ad913dea8e59fa"
SOURCE_COMMIT = "fdb9d3c"

APPENDIX = """
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
git checkout """ + SOURCE_COMMIT + """
BATTERY_VERSION=3.0.2 python zenodo/build_zenodo_package.py
```

Expected archive: **109,791 bytes**,
`md5:cf7b2953325002e2c1ad913dea8e59fa`.

The build refuses to report success if any check fails, including a gate added
here that rejects any file in the extracted archive containing CRLF. That gate was
tested by deliberately leaving a stray CRLF in the tree and confirming the build
blocked with exit code 1.
"""


def main() -> int:
    meta = json.loads(SRC_META.read_text(encoding="utf-8"))
    desc = SRC_DESC.read_text(encoding="utf-8")

    if meta.get("version") != BASE_VERSION:
        print(f"  ABORT: expected source version {BASE_VERSION}, "
              f"found {meta.get('version')}")
        return 1

    new = dict(meta)
    new["version"] = NEW_VERSION
    new["archive"] = ARCHIVE
    new["archive_sha256"] = ARCHIVE_MD5
    new["archive_bytes"] = ARCHIVE_BYTES
    new["supersedes"] = "https://doi.org/10.5281/zenodo.23137224"
    new["supersedes_note"] = (
        "3.0.2 ships the archive that actually rebuilds from source. 3.0.1 did "
        "not: it contained HANDOFF.md, which quotes the deposit's own digest, so "
        "the archive could never match the repository. 3.0.1 remains citable and "
        "verifies against its own manifest. No code, result or claim differs."
    )
    new["version_note_requested"] = (
        "v3.0.2 - ships the archive that rebuilds byte-for-byte from the "
        "repository (109,791 B, md5:4f360ff9..., commit fdb9d3c, two builds "
        "identical). v3.0.1 did not, because the deposit contained a session "
        "document quoting its own digest; v3.0.0 did not, because of CRLF line "
        "endings and a platform-dependent manifest generator. No code, result or "
        "claim changed in any version. v3.0.0 and v3.0.1 remain citable."
    )

    missing = [f for f in MUST_CARRY if f not in new]
    if missing:
        print(f"  ABORT: fields absent from derived metadata: {missing}")
        return 1
    for f in MUST_CARRY:
        if new[f] != meta[f]:
            print(f"  ABORT: {f} changed during derivation")
            return 1

    if "What changed in 3.0.2" not in desc:
        desc = desc.rstrip() + "\n" + APPENDIX

    OUT_META.write_text(
        json.dumps(new, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8", newline="\n")
    OUT_DESC.write_text(desc, encoding="utf-8", newline="\n")

    print(f"  {OUT_META.name}")
    print(f"    version     {meta.get('version')} -> {NEW_VERSION}")
    print(f"    subjects    {len(new['subjects'])} carried over "
          f"(PASTE INTO THE WEB FORM -- the API discards them)")
    print(f"    description {len(desc)} chars")
    print(f"    archive     {ARCHIVE}  {ARCHIVE_BYTES:,} B")
    print(f"\n  carried unchanged and verified: {', '.join(MUST_CARRY)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())