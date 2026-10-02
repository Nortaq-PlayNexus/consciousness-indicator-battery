#!/usr/bin/env python3
"""Create and populate Zenodo version 2 of the consciousness-indicator-battery deposit.

    python zenodo/upload_v2.py --draft

Creates a new version DRAFT under the existing concept DOI. Does not publish
unless --publish is passed. Never deletes a deposit.

Why a new version and not an edit: Zenodo records are immutable. Published
record 10.5281/zenodo.23101903 cannot be corrected in place, so v2 is a new
version record sharing the same concept DOI.

What v2 fixes, and what it does not:

  FIXES   references -- v1 published 722 single-character array entries instead
                        of four citations, because the source held one
                        concatenated string and Zenodo iterated it
          subjects   -- v1 published zero subjects, because free text is silently
                        discarded and controlled-vocabulary ids are required

  KEEPS   v1 remains published and citable. Nothing is withdrawn or replaced.
          The scientific content, code, archive contents and results are
          unchanged. This is a metadata-only correction.

Zenodo's deposition endpoint accepts `subjects` and `references` without error
and then does not persist them, and does not echo them back on read. So those two
fields are set here AND listed for manual entry in the web form, because the API
cannot be relied on for them. See zenodo/DEPOSIT_V2.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TOKEN_FILE = HERE / ".zenodo_token"
BASE = "https://zenodo.org/api"
CONCEPT_RECORD = "23101903"   # the published v1 record


def token() -> str:
    """Find the Zenodo token.

    One token serves both deposits, so it is stored once, in the ScientificDiscoveryLab
    repository. This script lives in the battery repository, which does not have it.
    Both locations are checked, then the environment, because a hard failure here
    after the archive is built and verified is an annoying way to learn about a
    missing file.
    """
    candidates = [
        TOKEN_FILE,
        ROOT / ".zenodo_token",
        Path(r"C:\Users\natha\ScientificDiscoveryLab\zenodo\.zenodo_token"),
    ]
    env = os.environ.get("ZENODO_TOKEN")
    if env:
        return env.strip()
    for candidate in candidates:
        if candidate.is_file():
            value = candidate.read_text(encoding="utf-8").strip()
            if value:
                return value
    sys.exit(
        "ERROR: no Zenodo token found.\n"
        "Looked in:\n"
        + "".join(f"  {c}\n" for c in candidates)
        + "Set ZENODO_TOKEN, or create one at\n"
        "  https://zenodo.org/account/settings/applications/tokens/new"
    )


def request(method: str, url: str, tok: str, body: bytes | None = None,
            content_type: str | None = None) -> dict:
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Authorization", f"Bearer {tok}")
    if content_type:
        req.add_header("Content-Type", content_type)
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            raw = resp.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:2000]
        sys.exit(f"HTTP {exc.code} on {method} {url}\n{detail}")
    except urllib.error.URLError as exc:
        sys.exit(f"network error: {exc}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def build_metadata(meta: dict, description: str) -> dict:
    payload: dict = {
        "upload_type": meta["upload_type"],
        "title": meta["title"],
        "description": description,
        "version": meta["version"],
        "license": meta["license"],
        "language": meta.get("language", "eng"),
        "access_right": meta.get("access_right", "open"),
        "creators": meta["creators"],
        "keywords": meta["keywords"],
        "related_identifiers": meta.get("related_identifiers", []),
        "notes": meta["notes"],
    }
    if meta.get("contributors"):
        payload["contributors"] = meta["contributors"]
    if meta.get("version_note"):
        payload["version_note"] = meta["version_note"]
    if meta.get("subjects"):
        payload["subjects"] = [{"id": s["id"]} for s in meta["subjects"]]
    if meta.get("references"):
        payload["references"] = meta["references"]
    if meta.get("communities"):
        # Legacy string ids, e.g. "philosophyofmind". The newer UUID form is not
        # interchangeable: this one resolved as published in v1, so it is reused
        # rather than "upgraded" to a form that might not.
        payload["communities"] = meta["communities"]
    return payload


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--metadata", default=str(HERE / "metadata_v2.json"))
    ap.add_argument("--description", default=str(HERE / "description_v2.md"))
    ap.add_argument("--archive", default=str(HERE / "consciousness-indicator-battery-v2.0.0.zip"))
    ap.add_argument("--reuse", type=int, default=None,
                    help="resume an existing v2 draft instead of creating one")
    ap.add_argument("--publish", action="store_true")
    args = ap.parse_args()

    tok = token()
    meta = json.loads(Path(args.metadata).read_text(encoding="utf-8"))
    description = Path(args.description).read_text(encoding="utf-8")
    archive = Path(args.archive).resolve()

    if not archive.is_file():
        sys.exit(f"ERROR: archive not found: {archive}")
    if meta["version"] not in archive.name:
        sys.exit(
            f"ERROR: metadata version {meta['version']} does not appear in the "
            f"archive filename {archive.name}. Zenodo files are immutable, so a "
            "mismatched name produces a permanent record whose filename "
            "contradicts its metadata."
        )

    print(f"archive : {archive.name}")
    print(f"size    : {archive.stat().st_size:,}")
    print(f"sha256  : {sha256_file(archive)}")
    print(f"version : {meta['version']}")

    if args.reuse:
        print(f"\nresuming draft {args.reuse}")
        dep = request("GET", f"{BASE}/deposit/depositions/{args.reuse}", tok)
    else:
        print(f"\ncreating new version under record {CONCEPT_RECORD}...")
        dep = request(
            "POST",
            f"{BASE}/deposit/depositions/{CONCEPT_RECORD}/actions/new_version",
            tok, b"", "application/json")
    dep_id = dep["id"]
    print(f"  draft id {dep_id}")

    print("\nuploading archive...")
    bucket = dep["links"]["bucket"].rstrip("/")
    target = f"{bucket}/{urllib.parse.quote(archive.name)}"
    # Only application/octet-stream is accepted; application/zip returns 415.
    uploaded = request("PUT", target, tok, archive.read_bytes(),
                       "application/octet-stream")
    print(f"  checksum {uploaded.get('checksum')}")

    print("\nattaching metadata...")
    request("PUT", f"{BASE}/deposit/depositions/{dep_id}", tok,
            json.dumps({"metadata": build_metadata(meta, description)}).encode(),
            "application/json")

    verified = request("GET", f"{BASE}/deposit/depositions/{dep_id}", tok)
    vm = verified["metadata"]
    print("\n" + "=" * 70)
    print(f"  draft      {dep_id}")
    print(f"  title      {vm.get('title')}")
    print(f"  version    {vm.get('version')}")
    print(f"  license    {vm.get('license')}")
    print(f"  keywords   {len(vm.get('keywords') or [])}")
    print(f"  creators   {len(vm.get('creators') or [])}")
    print(f"  contribs   {len(vm.get('contributors') or [])}")
    print(f"  related    {len(vm.get('related_identifiers') or [])}")
    print(f"  files      {len(verified.get('files') or [])}")
    print(f"  edit       https://zenodo.org/deposit/{dep_id}")
    print("=" * 70)

    record = {
        "draft_id": dep_id,
        "parent_record": CONCEPT_RECORD,
        "version": meta["version"],
        "archive": archive.name,
        "archive_bytes": archive.stat().st_size,
        "archive_sha256": sha256_file(archive),
        "published": False,
        "created": "2026-10-03",
    }
    out = HERE / f"DEPOSIT_V2_{dep_id}.json"
    out.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")

    if args.publish:
        print("\npublishing...")
        pub = request("POST",
                      f"{BASE}/deposit/depositions/{dep_id}/actions/publish",
                      tok, b"", "application/json")
        print(f"  version DOI  {pub.get('doi')}")
        print(f"  concept DOI  {pub.get('conceptdoi')}")
        record.update(published=True, doi=pub.get("doi"),
                      concept_doi=pub.get("conceptdoi"))
        out.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    else:
        print("\nDRAFT. Nothing published. v1 remains published and untouched.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
