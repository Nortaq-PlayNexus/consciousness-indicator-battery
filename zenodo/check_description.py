#!/usr/bin/env python3
"""Compare the stored description against the local file, character by character.

    python zenodo/check_description.py <deposit_id> <local.md>

Zenodo stores descriptions as HTML. A literal `>` comes back as `&gt;`, and
trailing whitespace is trimmed. Both are expected; anything else is a real
difference in what a reader sees.

Reports the first differing offset with context rather than a length pair, because
"9166 vs 9167" does not tell you what changed and a length comparison alone has
already produced one wrong conclusion in this project.
"""
from __future__ import annotations

import html
import json
import sys
import urllib.request
from pathlib import Path

TOKEN = Path(r"C:\Users\natha\ScientificDiscoveryLab\zenodo\.zenodo_token")


def main() -> int:
    dep_id = int(sys.argv[1])
    local_path = Path(sys.argv[2])

    tok = TOKEN.read_text(encoding="utf-8").strip()
    req = urllib.request.Request(
        f"https://zenodo.org/api/deposit/depositions/{dep_id}")
    req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=60) as resp:
        dep = json.loads(resp.read())

    remote_raw = dep["metadata"]["description"]
    local = local_path.read_text(encoding="utf-8")

    print(f"  deposit   {dep_id}")
    print(f"  local     {len(local)} chars")
    print(f"  remote    {len(remote_raw)} chars (raw HTML)")

    unescaped = html.unescape(remote_raw)
    if unescaped != remote_raw:
        n = sum(1 for a, b in zip(remote_raw, unescaped) if a != b)
        print(f"  unescaped {len(unescaped)} chars  ({n} HTML entities decoded)")

    # The invariant that matters is the *rendered* text. The local file stores
    # entities (`&gt;=`); Zenodo stores the decoded form (`>=`). A browser shows
    # `>` either way, so comparing raw strings reports a difference that no reader
    # can see. Comparing decoded-against-decoded tests the thing that matters.
    a = html.unescape(local).rstrip()
    b = unescaped.rstrip()

    print(f"\n  local  rendered  {len(a)}")
    print(f"  remote rendered  {len(b)}")

    if a == b:
        print("\n  IDENTICAL as rendered. The only differences are HTML entity")
        print("  encoding and trailing whitespace, neither of which a reader sees.")
        print("  Zenodo decoding `&gt;` to `>` is the readable direction.")
        return 0

    print("\n  DIFFERENT. First divergence:")
    n = min(len(a), len(b))
    i = next((k for k in range(n) if a[k] != b[k]), n)
    lo = max(0, i - 90)
    print(f"    at offset {i} of {n}")
    print(f"    local : ...{a[lo:i + 90]!r}")
    print(f"    remote: ...{b[lo:i + 90]!r}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())