# Weather Data Analyzer

Level: 1 — Python, Data & Automation

Skills: Python, CSV-shaped JSON, grouping

Paste daily temperature rows. The response gives mean, median, min, max, and the mean by city. Empty input is refused.

```bash
pip install -r requirements.txt
pytest -q
```

This is a local laptop proof. It does not call a hosted model and it does not apply production changes.

## Ops plane

Workspaces, tenant isolation, job approval, and audit live under `/v1`. Production apply is refused. See `docs/ARCHITECTURE.md`.
