# FCR — Python Edition

**Version:** 2.0.0

Python implementation of the Field Change Request (FCR) dashboard.

This repository is independent from the .NET ERMS module maintained in [dibaah/fcr.net](https://github.com/dibaah/fcr.net).

## Development

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
python main.py
```

Run tests:

```bash
pytest
python tools/check_html.py
```

## Data and local configuration

The repository retains the Python app's existing SQLite database as its baseline data/fixture. Local settings (especially machine-specific attachment paths), secrets, backups, exports and generated artifacts should not be committed.

## Plan

See [masterplan.md](masterplan.md) for the Python edition roadmap.
