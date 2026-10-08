"""Guard: CITATION.cff version must match the newest live version on the concept.

Failing this test is the exact failure mode that made the battery citation go
stale twice (v2.0.0 and v3.0.0 both shipped with CITATION.cff pointing at an
earlier version).  Phantom has test_citation.py for the same reason.
"""
from __future__ import annotations

import json
import re
import urllib.request
from pathlib import Path

CONCEPT = "23101902"
CIT_FILE = Path(__file__).resolve().parent.parent / "CITATION.cff"


def newest_version() -> tuple[str, str]:
    """Return (record_id, version) of the newest version on the concept."""
    with urllib.request.urlopen(
        f"https://zenodo.org/api/records/{CONCEPT}", timeout=60
    ) as r:
        data = json.loads(r.read())
    return data["id"], (data.get("metadata") or {}).get("version", "")


def cited_version() -> tuple[str, str]:
    text = CIT_FILE.read_text(encoding="utf-8")
    m_doi = re.search(r"^doi:\s*[\"']?(10\.5281/zenodo\.(\d+))", text, re.M)
    m_ver = re.search(r"^version:\s*[\"']?([^\"'\n]+)", text, re.M)
    doi = m_doi.group(1) if m_doi else ""
    rid = m_doi.group(2) if m_doi else ""
    version = m_ver.group(1).strip() if m_ver else ""
    return doi, rid, version


def test_citation_is_current() -> None:
    doi, rid, version = cited_version()
    live_rid, live_version = newest_version()
    assert str(rid) == str(live_rid), (
        f"CITATION.cff cites {rid} (v{version}) but {live_rid} (v{live_version}) "
        f"is the newest version on concept {CONCEPT}"
    )
    assert version == live_version, (
        f"CITATION.cff declares v{version} but the cited record is v{live_version}"
    )


def test_citation_has_required_fields() -> None:
    text = CIT_FILE.read_text(encoding="utf-8")
    for field in ("doi:", "concept-doi:", "version:"):
        assert field in text, f"CITATION.cff is missing required field: {field}"
