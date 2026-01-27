
# chronotes — setup

## Prerequisites
- Python **3.12+**
- **uv** installed (`pipx install uv` or system package)
- LaTeX toolchain *optional* (only needed if compiling PDFs)

---

## Fast path (recommended): uv

```bash
git clone git@github.com:tetrismegistus/chronotes.git
cd chronotes

uv sync --all-groups
```

Verify the environment:

```bash
uv run chronotes hello
uv run ruff check .
uv run pytest
```

If all three work, the project is correctly installed.

### Notes
- `uv sync` creates a local virtual environment in `.venv/`
- Console scripts (like `chronotes`) are installed because the project is packaged
- Dev tools (`ruff`, `pytest`) are included via dependency groups

---

## Fallback path (no uv)

If you don’t want uv, this project still installs cleanly using standard tooling.

```bash
python3.12 -m venv .venv
source .venv/bin/activate

pip install -U pip
pip install -e "[dev]"
```

Verify:

```bash
chronotes hello
ruff check .
pytest
```

---

## Optional dependencies

### Geocoding support

```bash
uv sync --all-groups --extra geo
```

or (pip):

```bash
pip install -e "[dev,geo]"
```


or (pip):

```bash
pip install -e "[dev,sky]"
```

---

## Project layout (brief)

- `src/chronotes/` — library + CLI
- `render/templates/` — LaTeX templates (primary layout surface)
- `providers/` — astronomy + geocoding backends
- `services/` — pure domain logic
- `tests/` — unit + contract tests

**Design rule:** Python owns *data and structure*. LaTeX owns *layout*.

---

## Common failure modes

### `chronotes: command not found`
- You forgot `uv sync`
- Or you installed without `-e` in the fallback path

### `ruff` / `pytest` missing
- You didn’t include dev dependencies
  - use `uv sync --all-groups` or `pip install -e "[dev]"`

### pytest loads random plugins
Run tests with isolation:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 uv run pytest
```

---

## Sanity reset (if things get weird)

```bash
rm -rf .venv
uv sync --all-groups
```

---

