# chronotes — setup

chronotes is a personal-first, professional-quality journal generator that produces LaTeX (and optionally PDF) daily pages spanning months or years. It integrates solar markers, planetary hours, and lunar phase data into a print-ready layout.

**Design rule:** Python owns *data and structure*. LaTeX owns *layout*.

---

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

If you don’t want to use `uv`, the project still installs cleanly with standard tooling.

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

## Example CLI usage

All commands write **LaTeX to stdout**. Redirect output to a file as needed.

---

### Primary workflow (city-based, implicit geocoding)

Use a city name as the primary location input.  
When coordinates are not supplied, geocoding is performed automatically.

```bash
chronotes render-year \
  --city "Indianapolis, IN" \
  --user-agent "chronotes/0.1 (you@example.com)" \
  --tz America/Indiana/Indianapolis \
  --year 2026 \
  > 2026.tex
```

Notes:
- `--user-agent` is required when using `--city` (Nominatim policy)
- Network IO occurs only in this mode
- No filesystem writes occur inside the tool

---

### Fallback / explicit workflow (lat/lon override)

Use explicit coordinates to bypass geocoding entirely.

```bash
chronotes render-year \
  --lat 39.7684 \
  --lon -86.1581 \
  --tz America/Indiana/Indianapolis \
  --year 2026 \
  > 2026.tex
```

Notes:
- `--lat` and `--lon` must be provided together
- When coordinates are supplied, `--city` is optional and used only as a printed label
- This path performs **no network IO**

---

### Debug / development workflow (single day)

Render a single day using explicit markers.  
No providers, no network access, no filesystem writes.

```bash
chronotes render-day \
  --city "Indianapolis, IN" \
  --day 2026-01-27 \
  --day-ruler-key sun \
  --moon-phase "Waxing Crescent" \
  --sunrise 2026-01-27T07:55:00 \
  --solar-noon 2026-01-27T13:20:00 \
  --sunset 2026-01-27T17:45:00 \
  --next-sunrise 2026-01-28T07:54:00
```

This command exists primarily for testing, layout iteration, and debugging.

---

## Location resolution rules

Location resolution follows a strict precedence:

1. **Explicit coordinates** (`--lat` + `--lon`)  
   → Always win; no geocoding performed.
2. **City name** (`--city`)  
   → Geocoded automatically (requires `--user-agent`).
3. **Neither provided**  
   → Error.

This policy is enforced centrally and consistently across commands.

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

### Skyfield astronomy backend (optional)

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

---

## Common failure modes

### `chronotes: command not found`
- You forgot `uv sync`
- Or you installed without `-e` in the fallback path

### `ruff` / `pytest` missing
- You didn’t include dev dependencies  
  Use:
  ```bash
  uv sync --all-groups
  ```
  or:
  ```bash
  pip install -e "[dev]"
  ```

### pytest loads unexpected plugins
Run tests with isolation:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 uv run pytest
```

---

## San