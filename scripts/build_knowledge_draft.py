#!/usr/bin/env python3
"""Build a draft knowledge contract from explicitly supplied, source-anchored claim records.

This is a deterministic importer, NOT an automatic PDF/LLM extractor.
Input JSON:
{"documentId":"DOC-1","title":"...", "claims":[{"statement":"...", "locator":"page 2"}]}
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from validate_knowledge_json import validate

def build(source: dict) -> dict:
    if not isinstance(source, dict):
        raise ValueError("source must be an object")
    doc_id, title = source.get("documentId"), source.get("title")
    if not isinstance(doc_id, str) or not doc_id.strip() or not isinstance(title, str) or not title.strip():
        raise ValueError("documentId and title required")
    claims = source.get("claims")
    if not isinstance(claims, list) or not claims:
        raise ValueError("claims must be nonempty")
    knowledge_id = "TECH-" + re.sub(r"[^A-Za-z0-9._-]", "-", doc_id)
    rows = []
    for i, item in enumerate(claims, 1):
        if not isinstance(item, dict) or not isinstance(item.get("statement"), str) or not item["statement"].strip():
            raise ValueError(f"claims[{i-1}].statement required")
        locator = item.get("locator")
        anchors = [{"locator":locator}] if isinstance(locator, str) and locator.strip() else []
        rows.append({"claimId":f"CLAIM-{i:03d}","statement":item["statement"],"verificationStatus":"unverified","sourceAnchors":anchors,"conditions":item.get("conditions",[]),"limitations":item.get("limitations",[]),"parameters":[]})
    return {"schemaVersion":"ew-knowledge-0.1","contractType":"technical_knowledge","knowledgeId":knowledge_id,"title":title,"source":{"documentId":doc_id,"title":title,"revision":source.get("revision"),"uri":source.get("uri"),"doi":source.get("doi")},"claims":rows,"review":{"status":"draft","version":"0.1","reviewerId":None,"approvedAt":None}}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        raw = json.loads(args.source.read_text(encoding="utf-8"))
        result = build(raw)
        errors = validate(result)
        if errors:
            raise ValueError("; ".join(errors))
        args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(f"Created draft: {args.output}")
        return 0
    except (ValueError, OSError) as exc:
        print(f"ERROR: {exc}")
        return 1
if __name__ == "__main__":
    raise SystemExit(main())
