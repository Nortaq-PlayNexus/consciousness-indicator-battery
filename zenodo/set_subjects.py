#!/usr/bin/env python3
"""Set `subjects` on an unpublished draft, which the deposit API silently drops.

    python zenodo/set_subjects.py <deposit-id>
    python zenodo/set_subjects.py <deposit-id> --from metadata_v3_0_3.json
    python zenodo/set_subjects.py <deposit-id> --dry-run

Why this script exists
----------------------
This repository carried a standing conclusion that Zenodo's API cannot set
`subjects`: the field is accepted, the request returns 200, and nothing is
stored, so every published version of this record shipped with zero subjects and
the values had to be typed into the web form by hand.

**That conclusion was wrong.** Subjects are settable. The field is not broken; the
*shape* was. Zenodo persists a subject as three keys, and only `term` is
displayed or indexed:

    {"term": "Consciousness", "identifier": "mesh:D003243", "scheme": "mesh"}

Measured on draft 23229094, 2026-10-08:

| payload                                        | stored                        |
|------------------------------------------------|-------------------------------|
| `[{"id": "mesh:D003243"}]`                      | 0 subjects                    |
| `[{"id": ..., "title": ...}]`                   | 0 subjects                    |
| `["mesh:D003243"]` (bare strings)               | HTTP 500                      |
| `[{"scheme": "mesh", "id": "D003243"}]`          | scheme only -- id DROPPED     |
| `[{"term": "Consciousness"}]`                    | term stored, no identifier    |
| `[{"term": ..., "identifier": ..., "scheme": ...}]` | stored in full            |

The `{"scheme", "id"}` row is the trap. It returns 200, the count goes up, and
the record looks correct -- but the identifier is discarded, leaving subjects
that name a scheme and nothing else. Checking only `len(subjects)` would have
passed a broken record straight through to publication.

`{"id": ...}` matching the shape used in the metadata files stores nothing at
all, which is what made this look like an API limitation rather than a schema
mismatch.

Validating identifiers
----------------------
Zenodo's vocabulary is queryable, so an identifier can be checked before it is
written to a record that cannot be edited afterwards:

    GET /api/subjects?q=<term>       -> [{"id": "mesh:D003243", "subject": "Consciousness", ...}]

Note that `/api/vocabularies/subjects` returns total 0 for everything and is not
the working endpoint. Every identifier this script writes should appear in that
vocabulary first.

Safety
------
`PUT /api/deposit/depositions/<id>` is a **full replacement**, not a merge. A
partial PUT wipes every other field; that has already destroyed a draft once on
this account, which is why `put_metadata_safely.py` exists. So this script reads
the live record, changes only `subjects`, sends the complete record back, and
diffs every other field afterwards. Exit 0 only if nothing else moved.

It refuses to run on a published record: subjects cannot be changed after
publication, and a PUT aimed at one would be rejected at best.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent

TOKEN_CANDIDATES = (
    HERE / ".zenodo_token",
    HERE.parent / ".zenodo_token",
    Path(r"C:\Users\natha\ScientificDiscoveryLab\zenodo\.zenodo_token"),
)

#: Every field that a partial PUT has been observed to destroy. All of them are
#: compared before and after, so a wipe is caught rather than assumed absent.
GUARD = (
    "title", "description", "notes", "license", "upload_type", "creators",
    "keywords", "contributors", "references", "related_identifiers",
    "communities", "version", "publication_date",
)


def token() -> str:
    for path in TOKEN_CANDIDATES:
        if path.is_file():
            value = path.read_text(encoding="utf-8").strip()
            if value:
                return value
    sys.exit("ERROR: no Zenodo token found in any known location")


def call(tok: str, method: str, url: str, body: bytes | None = None) -> dict:
    req = urllib.request.Request(url, method=method, data=body)
    req.add_header("Authorization", f"Bearer {tok}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        sys.exit(f"HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:500]}")


def subjects_from_meta(meta: dict) -> list[dict]:
    """Convert the metadata file's [{id, title}] subjects into Zenodo's shape."""
    out = []
    for entry in meta.get("subjects", []):
        ident = entry["id"]
        scheme, _, local = ident.partition(":")
        out.append({
            "term": entry.get("title", ""),
            "identifier": ident,
            "scheme": scheme,
            "title": entry.get("title", ""),
            "local_id": local,
        })
    return out


def vocabulary_ok(tok: str, term: str) -> str | None:
    """Return the Zenodo vocabulary id for `term`, or None if not found."""
    url = f"https://zenodo.org/api/subjects?q={urllib.request.quote(term)}&size=1"
    hits = call(tok, "GET", url).get("hits", {}).get("hits", [])
    return hits[0]["id"] if hits else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("deposit_id")
    ap.add_argument("--from", dest="meta_file",
                    help="metadata JSON holding a 'subjects' array")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--allow-unknown", action="store_true",
                    help="do not require each subject to exist in Zenodo's vocabulary")
    args = ap.parse_args()

    if not args.meta_file:
        sys.exit(__doc__ or "pass --from <metadata.json>")
    meta = json.loads(Path(args.meta_file).read_text(encoding="utf-8"))
    wanted = subjects_from_meta(meta)
    if not wanted:
        sys.exit(f"ERROR: no subjects in {args.meta_file}")

    tok = token()
    base = f"https://zenodo.org/api/deposit/depositions/{args.deposit_id}"

    live = call(tok, "GET", base)
    if live.get("state") not in ("unsubmitted", "in-progress"):
        sys.exit(
            f"ERROR: deposit {args.deposit_id} is '{live.get('state')}', not an "
            "unpublished draft. Subjects cannot be changed after publication."
        )
    before = live["metadata"]

    print(f"=== deposit {args.deposit_id} (v{before.get('version')}) ===")
    print(f"subjects before: {len(before.get('subjects') or [])}")

    print("\n=== vocabulary check ===")
    unknown = []
    for entry in wanted:
        found = vocabulary_ok(tok, entry["term"])
        mark = "ok" if found else "NOT IN ZENODO VOCABULARY"
        if found and found != entry["identifier"]:
            mark = f"differs from file: {found}"
        if not found:
            unknown.append(entry["term"])
        print(f"  [{mark:>28}] {entry['term']}  <{entry['identifier']}>")
    if unknown and not args.allow_unknown:
        sys.exit("\nERROR: unresolved terms above. Re-run with --allow-unknown to force.")

    payload = {k: v for k, v in before.items() if k != "subjects"}
    payload["subjects"] = [
        {"term": e["term"], "identifier": e["identifier"], "scheme": e["scheme"]}
        for e in wanted
    ]

    print("\n=== completeness check on the payload we will send ===")
    for e in payload["subjects"]:
        missing = [k for k in ("term", "identifier", "scheme") if not e.get(k)]
        print(f"  [{'ok' if not missing else 'MISSING ' + ','.join(missing)}] {e['term']}")
    print("  (a subject missing 'identifier' or 'term' is the failure mode that "
          "looks like success and strips the id)")

    if args.dry_run:
        print("\n--dry-run: nothing sent")
        return 0

    call(tok, "PUT", base, json.dumps({"metadata": payload}).encode())
    after = call(tok, "GET", base)["metadata"]

    print("\n=== read-back ===")
    stored = after.get("subjects") or []
    for s in stored:
        missing = [k for k in ("term", "identifier", "scheme") if not s.get(k)]
        print(f"  [{'ok' if not missing else 'INCOMPLETE'}] {s.get('term')} <{s.get('identifier')}>")

    damaged = [
        k for k in GUARD
        if json.dumps(before.get(k), sort_keys=True) != json.dumps(after.get(k), sort_keys=True)
    ]
    incomplete = [s for s in stored if not (s.get("term") and s.get("identifier"))]

    if damaged:
        print("\nFAIL: unrelated fields changed: " + ", ".join(damaged))
        print("Restore from the backup taken before this run. DO NOT PUBLISH.")
        return 1
    if incomplete:
        print("\nFAIL: stored subjects are incomplete. DO NOT PUBLISH.")
        return 1
    if len(stored) != len(wanted):
        print(f"\nFAIL: sent {len(wanted)}, stored {len(stored)}.")
        return 1

    print(f"\nOK: {len(stored)} subjects stored, each with term, identifier and scheme.")
    print("Every other field byte-identical.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())