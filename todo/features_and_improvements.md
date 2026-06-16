# Features and Improvements

## Planned Features
- More built-in digit sets (Base32, Base58, Base85, DNA, Morse)
- Stdin pipe / --file batch mode for CLI
- Digit set validation warnings in GUI
- Copy-to-clipboard button in GUI
- GET /health API endpoint
- Dockerfile for API
- Web UI (Jinja2 + FastAPI)
- Custom digit set save/edit from GUI
- Conversion history panel in GUI
- Async batch rebase endpoint
- i18n support

## Planned Refactoring
- Replace manual OS path logic with `platformdirs`
- Make `run_gui` import lazy in `cli.py`
- Make `reload=True` conditional on env var
- Remove duplicate digit-set cache in `api/main.py`
- Consolidate `[project]` / `[tool.poetry]` in pyproject.toml
- Split GUI: extract `DigitSetWidget` from `main_window.py`
- Extract placeholder magic strings into constants

## Planned Testing Improvements
- CLI tests (`test_cli.py`)
- API tests (`test_api.py`)
- Config loader tests (`test_config_loader.py`)
- Digit sets tests
- GUI smoke test
- Add mypy type checking
