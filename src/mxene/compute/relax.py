# src/mxene/compute/relax.py
from pathlib import Path
import subprocess
import shutil

from mxene.io.poscar import copy_poscar,get_system_name
from mxene.io.incar import copy_incar,change_system_name
from mxene.io.slurm import render_slurm

def prepare_relaxation(poscar_path: Path, 
                       relax_dir: Path,
                       calc_incar: Path,
                       slurm_template: Path):
    relax_dir.mkdir(exist_ok=True)
    # copy POSCAR
    copy_poscar(poscar_path, relax_dir)
    system_name = get_system_name(poscar_path)
    # Copy INCAR
    copy_incar(calc_incar, relax_dir)
    print(system_name)
    change_system_name(relax_dir / "INCAR", system_name)
    
    # use vaspkit to generate POTCAR
    # subprocess.run(["vaspkit", "-task", "201"], cwd=relax_dir, check=True)
    # pull slurm template and render it
    render_slurm(slurm_template, relax_dir / "relax.slurm", job_name=f'relax_{poscar_path}')


def submit_job(slurm_file: Path):
    subprocess.run(["sbatch", slurm_file.name],
                   cwd=slurm_file.parent,
                   check=True)