from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
UNITS_DIR = PROJECT_ROOT / "units"
RUNS_DIR = PROJECT_ROOT / "runs"
CALCS_DIR = PROJECT_ROOT / "calcs"
JOBS_TEMPLATE_DIR = PROJECT_ROOT / "jobs" / "cluster"
