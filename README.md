# FCR — Python Edition

Python implementation of the Field Change Request (FCR) dashboard.

This repository is independent from the .NET ERMS module maintained in [dibaah/fcr.net](https://github.com/dibaah/fcr.net).

## Development

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
python main.py
```

Run tests:

```bash
pytest
python tools/check_html.py
```

## Repository hygiene

Runtime database files, local settings/secrets, generated exports, backups, and build artifacts are not committed. See `.gitignore`.

## Plan

See [masterplan.md](masterplan.md) for the Python edition roadmap.
