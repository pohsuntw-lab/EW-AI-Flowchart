#!/usr/bin/env python3
"""Validate EW technical knowledge contracts without executing source content."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "docs/contract-knowledge/technical-knowledge.schema.json"
ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9._:-]*$")

def validate(doc: object) -> list[str]:
    errors = []
    if not isinstance(doc, dict):
        return ["$: expected object"]
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    # Minimal deterministic structural checks; not a full JSON Schema engine.
    for key in schema["required"]:
        if key not in doc:
            errors.append(f"$.{key}: required")
    if doc.get("schemaVersion") != "ew-knowledge-0.1":
        errors.append("$.schemaVersion: unsupported version")
    if doc.get("contractType") != "technical_knowledge":
        errors.append("$.contractType: must be technical_knowledge")
    for key in ("knowledgeId", "title"):
        if not isinstance(doc.get(key), str) or not doc[key].strip():
            errors.append(f"$.{key}: nonempty string required")
    if isinstance(doc.get("knowledgeId"), str) and not ID_RE.fullmatch(doc["knowledgeId"]):
        errors.append("$.knowledgeId: invalid stable ID")
    source = doc.get("source")
    if not isinstance(source, dict) or not all(isinstance(source.get(k), str) and source[k].strip() for k in ("documentId", "title")):
        errors.append("$.source: documentId and title required")
    review = doc.get("review")
    if not isinstance(review, dict) or review.get("status") not in {"draft","pending_review","approved","revoked","superseded"} or not isinstance(review.get("version"), str) or not review["version"]:
        errors.append("$.review: status and version required")
    claims = doc.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("$.claims: at least one claim required")
        return errors
    seen = set()
    for i, claim in enumerate(claims):
        p = f"$.claims[{i}]"
        if not isinstance(claim, dict):
            errors.append(f"{p}: object required")
            continue
        cid = claim.get("claimId")
        if not isinstance(cid, str) or not cid.strip() or cid in seen:
            errors.append(f"{p}.claimId: missing or duplicate")
        seen.add(cid)
        if not isinstance(claim.get("statement"), str) or not claim["statement"].strip():
            errors.append(f"{p}.statement: required")
        status = claim.get("verificationStatus")
        if status not in {"unverified","reviewed","rejected"}:
            errors.append(f"{p}.verificationStatus: invalid")
        anchors = claim.get("sourceAnchors")
        if not isinstance(anchors, list):
            errors.append(f"{p}.sourceAnchors: array required")
            anchors = []
        if status == "reviewed" and not anchors:
            errors.append(f"{p}.sourceAnchors: reviewed claim needs source evidence")
        for j, anchor in enumerate(anchors):
            if not isinstance(anchor, dict) or not isinstance(anchor.get("locator"), str) or not anchor["locator"].strip():
                errors.append(f"{p}.sourceAnchors[{j}]: source locator required")
    if isinstance(review, dict) and review.get("status") == "approved":
        if not review.get("reviewerId") or not review.get("approvedAt"):
            errors.append("$.review: approved contract needs reviewerId and approvedAt")
        if any(not isinstance(c, dict) or c.get("verificationStatus") != "reviewed" for c in claims):
            errors.append("$.claims: approved contract cannot contain unreviewed claims")
    return errors

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", type=Path)
    args = ap.parse_args()
    try:
        doc = json.loads(args.path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}")
        return 2
    errors = validate(doc)
    for e in errors:
        print("ERROR:", e)
    print(f"Validation: {len(errors)} error(s)")
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
