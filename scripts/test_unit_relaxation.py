#!/usr/bin/env python3

from pathlib import Path
from mxene.compute.relax import prepare_relaxation, submit_job
from mxene.io.paths import UNITS_DIR, RUNS_DIR, CALCS_DIR, JOBS_TEMPLATE_DIR

def main():
    """
    Test the relaxation workflow on all units in units/atom_data
    """
    # Source template paths
    relax_template_incar = CALCS_DIR / "relax_pbe"
    slurm_template = JOBS_TEMPLATE_DIR / "vasp_std.slurm"

    # Ensure runs directory exists
    RUNS_DIR.mkdir(exist_ok=True)

    # Loop over POSCAR files

    for poscar_path in UNITS_DIR.glob("*.poscar"):
        unit_name = poscar_path.stem
        print(f"[TEST] Preparing relaxation for {unit_name}")

        # Target directory for this unit
        target_dir = RUNS_DIR / unit_name

        # Prepare relaxation (copies files, generates POTCAR, renders slurm)
        slurm_file = prepare_relaxation(
            poscar_path=poscar_path,
            relax_dir=target_dir,
            calc_incar=relax_template_incar,
            slurm_template=slurm_template,
        )

        # Optionally submit job (comment out for dry-run testing)
        # submit_job(slurm_file)

        print(f"[TEST] Relaxation prepared at {target_dir}")

if __name__ == "__main__":
    main()