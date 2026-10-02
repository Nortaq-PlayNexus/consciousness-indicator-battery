#!/usr/bin/env python3
"""One-shot repair for the battery deposit's corrupted `references` field.

    python tools/fix_battery_references.py

What went wrong
---------------
`zenodo/metadata.json` in the consciousness-indicator-battery repository stored
`references` as a list of 826 SINGLE CHARACTERS:

    ["B", "u", "t", "l", "i", "n", ",", "P", ".", ...]

Zenodo's API received that verbatim and iterated it, so the PUBLISHED record
10.5281/zenodo.23101903 currently carries a `references` array of 722 individual
characters rather than four citations. The four citations are not lost -- they
survive, concatenated, with whitespace collapsed -- but as stored the field is
unusable: any consumer reading it gets character noise, not references.

The cause is a string being iterated where a list was intended, most likely when
the metadata was assembled. Nothing warned about it, because a list of 722
one-character strings is a perfectly valid JSON array.

What this script does
---------------------
Recovers the intended citations by joining the characters and splitting on blank
lines, then writes them back as a proper list of four strings.

It cannot fix the published record. Zenodo records are immutable, so correcting
10.5281/zenodo.23101903 requires publishing a NEW VERSION. This script only
repairs the local source so that any future version carries the field correctly.
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
META = REPO / "zenodo" / "metadata.json"


def is_character_list(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(v, str) and len(v) == 1 for v in value)
    )


def main() -> int:
    if not META.is_file():
        print(f"ERROR: {META} not found")
        return 1

    meta = json.loads(META.read_text(encoding="utf-8"))
    refs = meta.get("references")

    if not is_character_list(refs):
        count = len(refs) if isinstance(refs, list) else 0
        print(f"references is not a character list (found {count} entries). Nothing to do.")
        return 0

    joined = "".join(refs)
    print(f"detected: references is a list of {len(refs)} single characters")

    # Recover the intended entries. Citations were separated by blank lines; the
    # characters carry newlines, so splitting on two or more newlines is reliable
    # here. Falling back to a single newline split keeps this from silently
    # producing one giant entry if the separator is missing.
    recovered = [part.strip() for part in joined.split("\n\n") if part.strip()]
    if len(recovered) < 2:
        recovered = [part.strip() for part in joined.split("\n") if part.strip()]

    print(f"recovered {len(recovered)} citations:")
    for i, ref in enumerate(recovered, 1):
        head = ref[:74] + ("..." if len(ref) > 74 else "")
        print(f"  {i}. {head}")

    meta["references"] = recovered
    meta["_references_repair_note"] = (
        "The references field was previously a list of individual characters, which "
        "Zenodo stored verbatim, so published record 10.5281/zenodo.23101903 carries "
        "722 one-character entries instead of four citations. The citations were "
        "recovered by concatenation and are correct here. Fixing the published record "
        "requires a new version, because Zenodo records are immutable."
    )

    META.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nrepaired {META}")
    print("The published record is NOT changed by this. See the note just written.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
