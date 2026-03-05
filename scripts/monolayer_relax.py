#!/usr/bin/env python3

from pathlib import Path
import argparse

from mxene.io.paths import UNITS_DIR, RUNS_DIR, CALCS_DIR, JOBS_TEMPLATE_DIR
from mxene.compute.relax import prepare_relaxation, submit_job
from mxene.structures.monolayer import make_monolayer_vacancy
from mxene.io.poscar import write_poscar

def relax_monolayer(size: str, spec: str, shift: int, vacancy_condition: str):
    """
    Relax a given monolayer
    """
    
    target_dir = RUNS_DIR / "monolayer" / f'{size}' / f'{spec}' / f'n{shift}' / f'{vacancy_condition}'
    target_dir.mkdir(parents=True, exist_ok=False)

    monolayer_str = make_monolayer_vacancy(size=size, spec=spec, shift=shift, vacancy_condition=vacancy_condition)
    write_poscar(monolayer_str, target_dir)

    slurm_file = prepare_relaxation(
        relax_dir=target_dir,
        poscar_path=target_dir / "POSCAR",
        calc_incar=CALCS_DIR / "relax_pbe",
        slurm_template=JOBS_TEMPLATE_DIR / "vasp_std.slurm",
    )
    # print(f"Relaxation setup complete for {spec} with vacancy condition {vacancy_condition} at {target_dir}")
    # Optionally submit job (comment out for dry-run testing)
    submit_job(slurm_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a monolayer structure with or without a vacancy')
    parser.add_argument('size', type=str, 
                        help='The size of the supercell, e.g. 1x1, 3x3, etc.')
    parser.add_argument('spec', type=str, 
                        help='The chemical formula of the system, e.g. Ti2C, Ti3C2O2, etc.')
    parser.add_argument('shift_number', type=int, 
                        help='Shift the registry by a certain number of positions (default: 0)')
    parser.add_argument('vacancy_condition', type=str, 
                        help='The condition of the vacancy to create (default: None/pristine)')
    args = parser.parse_args()
    try:
        relax_monolayer(args.size, args.spec, args.shift_number, args.vacancy_condition)
    except FileExistsError as exc:
        raise FileExistsError(
            f"Target run directory already exists: {exc.filename}. "
            "Choose a different configuration or remove the existing directory."
        ) from exc
    
    