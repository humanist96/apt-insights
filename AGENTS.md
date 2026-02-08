# Repository Guidelines

## Project Structure & Module Organization
- `api_01/`–`api_04/`: API-specific modules, CLI entry points (`main.py`), test scripts, and `output/` artifacts.
- `backend/`: data loading, analysis, and duplicated API modules used by the data pipeline.
- `frontend/`: Streamlit UI (`frontend/app.py`).
- Top-level utilities: `collect_data.py` (batch CLI), `batch_collector.py` (batch logic), `common.py` (XML parsing helpers), `config.py` (API key).
- Reference docs: `API_Ref.md`, `README.md`.

## Build, Test, and Development Commands
- Install deps: `pip install -r requirements.txt`
- Batch collection: `python collect_data.py <lawd_cd> <start_ym> <end_ym> --api api_01 api_02`
- Single API run: `python api_01/main.py <lawd_cd> <deal_ymd>`
- Scripted tests (per API): `python api_01/test_runner.py`
- Region-specific tests: `python api_01/test_suwon.py`
- UI: `streamlit run frontend/app.py`

## Coding Style & Naming Conventions
- Python only; use 4-space indentation and PEP 8 conventions.
- Functions/variables: `snake_case`; classes: `PascalCase`.
- API modules use `api_XX` directory naming (e.g., `api_03`).
- Test outputs follow `api_XX/output/test_results_YYYYMMDD_HHMMSS.json` and `test_report_YYYYMMDD_HHMMSS.md`.
- Normalized fields in `backend/data_loader.py` are prefixed with `_` (e.g., `_deal_amount_numeric`).

## Testing Guidelines
- Tests are script-driven, not pytest-based.
- Prefer `api_XX/test_runner.py` for batch test cases and report generation.
- Outputs are written to `api_XX/output/`; keep these directories organized and do not hand-edit generated files.
- Use stable inputs (`lawd_cd`, `deal_ymd`) so results are reproducible when possible.

## Commit & Pull Request Guidelines
- No git history is present in this workspace, so no established commit convention was found.
- If you initialize git, use short imperative commit subjects (e.g., “Add batch retry backoff”).
- PRs should include a concise summary, the commands run, and UI screenshots when the Streamlit app changes.

## Security & Configuration
- API keys live in `config.py` and `backend/config.py`; keep them in sync.
- Avoid committing real keys or test data that should be private; prefer local overrides or environment variables if adding new config.
