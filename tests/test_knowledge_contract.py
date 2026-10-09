#!/usr/bin/env python3
"""Regression checks for technical knowledge validation."""
import json
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_knowledge_json import validate

EXAMPLE = ROOT / "docs/contract-knowledge/example.knowledge.json"

class KnowledgeContractTests(unittest.TestCase):
    def setUp(self):
        self.doc = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_draft_example_valid(self):
        self.assertEqual(validate(self.doc), [])

    def test_reviewed_requires_source_anchor(self):
        self.doc["claims"][0]["verificationStatus"] = "reviewed"
        self.assertTrue(any("source evidence" in x for x in validate(self.doc)))

    def test_approval_requires_review(self):
        self.doc["review"]["status"] = "approved"
        self.assertTrue(validate(self.doc))

    def test_technical_contract_needs_no_raci(self):
        self.assertNotIn("raci", self.doc)
        self.assertEqual(validate(self.doc), [])

    def test_wrong_type_rejected(self):
        self.doc["contractType"] = "process_contract"
        self.assertTrue(validate(self.doc))

if __name__ == "__main__":
    unittest.main()
