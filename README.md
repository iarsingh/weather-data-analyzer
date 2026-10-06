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

## Project documentation

- [Project architecture and component diagram](PROJECT_ARCHITECTURE.md)
- [Domain request and job approval flows](docs/PROCESS_FLOW.md)
- [Project-specific interview questions and answers](INTERVIEW_QA.md)

## Readiness upgrade

See [implemented improvements and local run instructions](docs/UPGRADES.md). The domain API adds validated inputs and explanatory outputs; ops approval is idempotent and container examples run without root. Interactive API documentation is available at `/docs`.

## Documentation checks

Project architecture, interview guides, and local source links are checked automatically on pushes and pull requests. Run the same check locally:

```bash
python3 .github/scripts/validate_project_docs.py
```
