# Repository Guidelines

## Project Structure & Module Organization
`gmsc_mapper/` contains the Python package and CLI entry point (`main.py`) plus focused modules such as `predict.py`, `translate.py`, and `map_*.py`. `tests/` holds pytest-based unit and integration checks, along with expected output fixtures in subdirectories like `tests/diamond_contig/`. `examples/` provides sample inputs, reference metadata, and example outputs for manual runs. Packaging and environment setup live in `setup.py`, `requirements.txt`, `environment.yml`, and `tests.sh`.

## Build, Test, and Development Commands
Create the recommended environment with `conda env create -f environment.yml` or install Python dependencies with `pip install -r requirements.txt`. Install the package locally with `python setup.py install`; this exposes the `gmsc-mapper` CLI.

Run the main automated checks with `python -m pytest ./tests`. Use `bash tests.sh` for the end-to-end smoke workflow that creates mock DIAMOND and MMseqs databases and validates generated outputs. For quick manual verification, run commands such as `gmsc-mapper createdb -i examples/target.faa -o examples/ -m diamond` and `gmsc-mapper -i examples/example.fa -o examples_output/ --dbdir examples/`.

## Coding Style & Naming Conventions
Follow the existing Python style: 4-space indentation, `snake_case` for functions and variables, and small single-purpose modules. Keep CLI option handling in `gmsc_mapper/main.py` and shared helpers in dedicated modules such as `utils.py`. Match existing naming patterns for tests and fixtures: `test_*.py` for pytest files and descriptive output folders such as `tests/mmseqs_contig/`. No formatter or linter is configured here, so keep changes minimal and consistent with adjacent code.

## Testing Guidelines
Pytest is the canonical test runner and is the workflow used in `.github/workflows/test_gmsc_mapper.yml` across Python 3.8-3.11. Add or update tests whenever CLI behavior, mapping logic, or output formats change. Prefer deterministic assertions against fixture files and dictionaries, following examples like `tests/test_translate.py` and `tests/test_predict.py`.

## Commit & Pull Request Guidelines
Recent history uses short prefixes in the subject line: `ENH`, `BUG`, `TST`, and `RLS` (for example, `BUG fix sensitivity of diamond`). Keep commit subjects imperative and concise. Pull requests should describe the behavior change, list the commands used to verify it, and note any dependency or database-index implications. Include sample output snippets only when CLI output or generated files changed materially.

## ChangeLog
When making user-visible changes, add an entry to the `ChangeLog` file under the `Unreleased` section.

## Markdown Style
Use HTML entities (`&lt;` and `&gt;`) for angle brackets in Markdown files instead of literal `<` and `>`.

## Import Style
Avoid heavy top-level imports in `gmsc_mapper/main.py` since it is the CLI entry point and slow imports (e.g., `pandas`, `numpy`) penalize startup time for every invocation. Keep heavy imports inside the functions that need them.

## External Tools & Data
Many workflows depend on external aligners: DIAMOND and MMseqs2. Document any version-sensitive changes, especially if they affect `createdb`, alignment output, or fixture regeneration.
