# src/mxene/io/setup_log.py

from pathlib import Path


def record_setup_log(working_dir: Path, poscar_path: Path, incar_path: Path, slurm_template: Path):
    log_path = working_dir / "setup_log.txt"
    with open(log_path, 'w') as f:
        f.write(f"Working Directory: {working_dir}\n")
        f.write(f"POSCAR: {poscar_path}\n")
        f.write(f"INCAR: {incar_path}\n")
        f.write(f"Slurm Template: {slurm_template}\n")