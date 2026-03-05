# src/mxene/io/setup_log.py

from pathlib import Path
from mxene.io.paths import name_with_n_parents
from mxene.io.poscar import get_header, get_ions
from mxene.io.kpoints import get_kpoints
from mxene.io.potcar import get_potcar_specs


def record_setup_log(working_dir: Path, poscar_path: Path, incar_path: Path, slurm_template: Path):
    log_path = working_dir / "setup_log.txt"
    with open(log_path, 'w') as f:
        f.write(f"Working Directory: {working_dir}\n")
        f.write(f"POSCAR header: {get_header(poscar_path)}\n")
        f.write(f"INCAR: {name_with_n_parents(incar_path, 2)}\n")
        f.write(f"KPOINTS: {get_kpoints(working_dir / 'KPOINTS')}\n")
        f.write(f"POTCAR Specs: {get_potcar_specs(working_dir / 'POTCAR')}\n")
        f.write(f"Ions: {get_ions(poscar_path)}\n")
        f.write(f"Slurm Template: {name_with_n_parents(slurm_template, 3)}\n")