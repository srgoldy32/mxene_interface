# src/mxene/analysis/status.py

from pathlib import Path
from mxene.io.outcar import get_wall_time
from mxene.io.output import get_last_n_lines
from mxene.io.kpoints import get_kpoints

def read_wall(check_dir: Path) -> str:
    outcar_path = check_dir / "OUTCAR"
    if not outcar_path.exists():
        return "OUTCAR not found. Relaxation may still be running or failed to start."
    
    try:
        wall_time = get_wall_time(outcar_path)
        return f"{wall_time}"
    except ValueError:
        output_path = check_dir / "output"
        last_lines = get_last_n_lines(output_path, 3)
        for i in last_lines:
            print(i.strip())
        return "Not done yet. Last 3 lines of output above"
    
def read_kpoints(check_dir: Path) -> str:
    kpoints_path = check_dir / "KPOINTS"
    
    if not kpoints_path.exists():
        return "KPOINTS file not found."
    
    return get_kpoints(kpoints_path)