
# Enhanced Calculator (CLI)

An enhanced command-line calculator with full test coverage, and full REPL Interface

## Quickstart

```bash
# 1) Clone & enter
git clone <your-repo-url>
cd enhanced_calculator

# 2) Create venv
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3) Install deps
pip install -r requirements.txt

# 4) Run tests (100% coverage enforced by CI; locally you can check too)
pytest --cov=app tests/
coverage report

# 5) Run the REPL
python -m app.calculator_repl
```

## Commands

- `+ - * / ^ root <operands...>` perform operation
- `history` show history
- `save [path]` save history
- `load <path>` load history
- `undo` / `redo` history state via Memento
- `clear` clear history
- `help` show help
- `exit` quit

## Design

- **Strategy**: operation classes execute arithmetic.
- **Factory**: `operation_factory` instantiates a strategy by symbol.
- **Observer**: History notifies observers; CSV autosave observer persists on change.
- **Memento**: `Caretaker` tracks DF snapshots for undo/redo.
- **Facade**: `CalculatorFacade` is a thin façade for REPL.

## Tests & Coverage

- Run: `pytest --cov=app tests/`
- We intentionally mark non-testable CLI entry lines with `# pragma: no cover`.
- CI enforces `--fail-under=100`. If you intentionally skip lines, annotate them.
