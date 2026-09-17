# Compatibility

Works with agents that support the Agent Skills format, or agents that can load SKILL.md and access the bundled resources/scripts.

Portable skill format: `SKILL.md` + `references/` + `templates/` + `examples/` + `skill/tools/` (pure Python) + `scripts/` (wrappers).

## Platform Matrix

| Platform | Skill Format Support | Installation Method | Python Execution | Status | Notes |
|----------|----------------------|---------------------|------------------|--------|-------|
| Agent with Agent Skills support (file system + Python) | Supported | Method A (Upload/install skill package, enable) | Required for calculations | Supported | Full — `python scripts/run_analysis.py --input examples/sample-project.json --output ./out` |
| Generic AI Agent (file system + Python, no native Skills) | Compatible | Method B (Copy directory into agent's skills directory) | Required for calculations | Compatible | Full via SKILL.md + bundled scripts |
| Manual / No-Skills Agent | Compatible | Method C (Provide SKILL.md + references + templates, optionally run scripts) | Optional | Compatible | Reasoning without Python; calculations need Python |
| Claude (Agent Skills compatible format) | Compatible | Method A | Required for calculations | Not Tested | Compatible format — not officially tested; use Method A |
| OpenAI / Codex (Skills compatible format) | Compatible | Method A | Required for calculations | Not Tested | Compatible format — not officially tested; use Method A |
| Gemini / Other LLM (Markdown + scripts) | Compatible | Method C | Optional | Not Tested | Compatible format — provide SKILL.md + references |
| No-code agent without Python | Manual | Method C (SKILL.md only) | Not Available | Manual | Prompt-only; no `skill/tools` execution |

## Notes

- **Supported**: Verified via self-contained test (clean extract → install → run).
- **Compatible**: Expected to work via Agent Skills format or Markdown+scripts loading; not blocked but not formally verified on that platform.
- **Manual**: Can be used by providing SKILL.md + references/templates; Python not available.
- **Not Tested**: Format-compatible but not executed on this platform in this release; use Method A/B/C as documented.
- No claim of officially supported status is made — only format compatibility as above.

## Execution Requirements

- Python ≥3.9, `pip install -r requirements.txt` (pyyaml, pandas, numpy, openpyxl)
- No API keys, tokens, passwords, or secrets — skill is credential-free.
- All paths relative to package root; no absolute `/home/...` paths.

## Verification

Self-contained test (see `MANIFEST.md` and Final QA) extracts archive to clean temp dir and runs:

```bash
pip install -r requirements.txt
python scripts/run_analysis.py --input examples/sample-project.json --output ./out
pytest -q
ruff check .
mypy skill
python examples/golden_project/run.py
```
