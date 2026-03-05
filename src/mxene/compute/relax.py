# src/mxene/compute/relax.py
from pathlib import Path
import subprocess
import shutil

from mxene.io.poscar import copy_poscar,get_system_name
from mxene.io.incar import copy_incar,change_system_name
from mxene.io.slurm import render_slurm
from mxene.io.setup_log import record_setup_log
from mxene.io.paths import name_with_n_parents

def prepare_relaxation(relax_dir: Path,
                       poscar_path: Path, 
                       calc_incar: Path,
                       slurm_template: Path):
    relax_dir.mkdir(exist_ok=True)
    # check for poscar in relax_dir to avoid overwriting
    if (relax_dir / "POSCAR").exists():
        pass # print(f"POSCAR already exists in {relax_dir}. Skipping copy to avoid overwriting.")
    else:   
        copy_poscar(poscar_path, relax_dir)
    header = get_system_name(poscar_path)
    system_name = get_system_name(poscar_path)
    # Copy INCAR
    copy_incar(calc_incar, relax_dir)
    change_system_name(relax_dir / "INCAR", system_name)
    
    # use vaspkit to generate POTCAR (103) and KPOINTS (102) 
    subprocess.run(
        ["vaspkit"],
        cwd=relax_dir,
        check=True,
        input="102\n2\n0.04\n",
        text=True,
        stdout=subprocess.DEVNULL,
    )
    # pull slurm template and render it
    slurm_file_path = relax_dir / slurm_template.name
    render_slurm(slurm_template, slurm_file_path, 
                 job_name=f'relax_{header}')
    record_setup_log(relax_dir, poscar_path, calc_incar, slurm_template)

    return slurm_file_path


def submit_job(slurm_file: Path):
    subprocess.run(["sbatch", slurm_file.name],
                   cwd=slurm_file.parent,
                   check=True)