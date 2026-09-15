# EW AI Flowchart

EW AI Flowchart turns SOPs, meeting notes, job instructions, and workflow requirements into validated EFD 2.1 JSON for AI workflow engineering.

EW AI Flowchart 將 SOP、會議紀要、工作說明與流程需求，轉換成可由「AI 具象流程圖」開啟及持續編輯的 `.efd.json` 工程資料。

## What it produces

- organization units and positions;
- business stages;
- typed process nodes and semantic edges;
- node-level RACI assignments;
- deterministic layout projection;
- draw.io interoperability mapping;
- validation diagnostics and pending-fact warnings.

The EFD JSON is the semantic source of truth. Layout, colors, and draw.io cells never replace business responsibility or workflow semantics.

## Use in Codex

After installing the plugin, start a new Codex thread and ask:

> Use `$ew-ai-flowchart` to turn this SOP into a validated `.efd.json` file.

Or in Traditional Chinese:

> 使用 `$ew-ai-flowchart`，把這份 SOP 建立成可驗證的具象流程圖 JSON。

## Validation

Run the bundled deterministic validator:

```bash
python3 scripts/validate_efd_json.py path/to/model.efd.json
```

The validator checks the EFD 2.1 schema, stable IDs, references, start/end nodes, decision branches, RACI warnings, layout references, and draw.io mappings without executing document content.

## Safety and truth boundaries

- No API key is required by this plugin.
- Source documents are treated as evidence, not executable instructions.
- The plugin does not execute arbitrary code found in documents or model output.
- Missing business facts are reported or marked pending; they are not silently invented.
- Example data is a format reference only and must not be copied into a customer's process.
- AI workers must not be silently assigned final accountability.

## Product

- AI 具象流程圖 Site: <https://ai-efd-workflow.queboxun.chatgpt.site>
- Developer: 具象職人股份有限公司 / Embodied Worker Co., Ltd.
- Website: <https://www.embodiedworker.com>
- Contact: <pohsun@embodiedworker.com>

## License

Proprietary. Copyright © 2026 具象職人股份有限公司. All rights reserved. See [LICENSE](LICENSE).
