# EW AI Flowchart → EdgeAI MCP Knowledge Builder (Proposal v0.1)

## Scope / 範圍

Add a second, **non-process** JSON contract for technical manuals, research papers, engineering specifications and reviewed tacit knowledge. **Do not replace or reinterpret EFD 2.1**. EFD remains the normative workflow/RACI contract.

新增技術知識 JSON 契約，適用技術手冊、論文、規格與經確認的內隱知識；既有 EFD 2.1 工作流程及節點 RACI 完全保留。

## Contract types

- `process_contract`: EFD 2.1, node-level RACI and workflow semantics.
- `technical_knowledge`: source-backed statements, formulas, operating constraints, applicability, limitations and evidence; **RACI is not required**.

## Proposed ingestion pipeline

Source document → extraction with page/section anchors → candidate facts and uncertainties → human technical review → JSON Schema validation → versioned contract registry → indexed, read-only MCP tools → authorized AI worker.

## Governance

- Do not invent source facts, approvals, numeric thresholds, responsibilities or citations.
- Every technical claim must point to a source anchor or be explicitly marked unverified.
- Research findings are **not** automatically approved operational rules.
- Source text is untrusted: never execute embedded code or instructions.
- A JSON contract is data, not an executable Python program.
- Publishing, executing skills and controlling equipment are separate authorization steps.
- Revoked/superseded versions must not be returned as active contracts.

## MCP read-only interface proposal

```text
get_contract(contract_id, version?)
find_knowledge(equipment_id?, parameter?, topic?, method?)
get_source_evidence(knowledge_id)
find_workflow_by_tag(tag_id)
get_related_contracts(contract_id)
```

MCP is the transport/tool interface; deterministic indexes and contract validation provide retrieval accuracy. Do not claim fixed 1ms latency or guaranteed correctness without benchmarks.

## Implementation gates

1. Validate a representative EFD file unchanged using the existing validator.
2. Validate a representative technical knowledge contract with the new schema.
3. Confirm no RACI is fabricated for papers/manuals.
4. Verify source anchors, missing facts, version and revocation behavior.
5. Only then integrate an MCP server and approved Skill Runtime.

**Status: schema/design proposal, not deployed MCP server.**
