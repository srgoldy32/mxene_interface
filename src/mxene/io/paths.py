from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RUNS_DIR = PROJECT_ROOT / "runs"
CALCS_DIR = PROJECT_ROOT / "calcs"
JOBS_TEMPLATE_DIR = PROJECT_ROOT / "jobs" / "cluster"
DATA_DIR = PROJECT_ROOT / "data"
UNITS_DIR = DATA_DIR / "relaxed_units"

def name_with_n_parents(path: Path,n: int) -> str:
    parts = path.parts
    if len(parts) >= n:
        return str(Path(*parts[-n:]))
    return str(path)
