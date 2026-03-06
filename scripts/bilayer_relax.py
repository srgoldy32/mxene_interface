#!/usr/bin/env python3

from pathlib import Path
import argparse

from mxene.io.paths import RUNS_DIR, CALCS_DIR, JOBS_TEMPLATE_DIR
from mxene.structures.bilayer import make_bilayer, fix_middles
from mxene.io.poscar import write_poscar
from mxene.constants.constants import SPEC2SHIFT
from mxene.compute.relax import prepare_relaxation, submit_job


def relax_bilayer(size: str,
                  bottom_spec: str, 
                  bottom_shift: int,
                  bottom_vacancy_condition: str,
                  top_spec: str,
                  top_shift: int,
                  top_vacancy_condition: str,
                  applied_gap: float):
    """
    Relax a given bilayer structure
    """

    target_dir = (RUNS_DIR / "bilayer" /
                   f'{size}' / 
                   f'{bottom_spec}_{top_spec}' / 
                   f'n{bottom_shift}_n{top_shift}' /
                   f'{bottom_vacancy_condition}_{top_vacancy_condition}' /
                   f'gap{applied_gap}')   
    target_dir.mkdir(parents=True, exist_ok=True)
    # make bilayer structure
    bottom_file = RUNS_DIR / "monolayer" / f'{size}' / f'{bottom_spec}' / f'n{bottom_shift}' / f'{bottom_vacancy_condition}' / "POSCAR"
    top_file = RUNS_DIR / "monolayer" / f'{size}' / f'{top_spec}' / f'n{top_shift}' / f'{top_vacancy_condition}' / "POSCAR"
    bilayer_str = make_bilayer(bottom_file=bottom_file, top_file=top_file, applied_gap=applied_gap)
    selective_dynamics_bilayer_str = fix_middles(bilayer_str)
    write_poscar(selective_dynamics_bilayer_str, target_dir)

    slurm_file = prepare_relaxation(
        relax_dir=target_dir,
        poscar_path=target_dir / "POSCAR",
        calc_incar=CALCS_DIR / "relax_pbe",
        slurm_template=JOBS_TEMPLATE_DIR / "vasp_std.slurm",
    )
    
    submit_job(slurm_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a monolayer structure with or without a vacancy')
    parser.add_argument('size', type=str, 
                        help='The size of the supercell, e.g. 1x1, 3x3, etc.')
    parser.add_argument('bottom_spec', type=str,
                        help='The chemical formula of the bottom layer, e.g. Ti2C, Ti3C2O2, etc.')
    # parser.add_argument('bottom_shift', type=int,
    #                     help='Shift the registry of the bottom layer by a certain number of positions (default: 0)')
    parser.add_argument('bottom_vacancy_condition', type=str,
                        help='The condition of the vacancy to create in the bottom layer (default: None/pristine)')
    parser.add_argument('top_spec', type=str,
                        help='The chemical formula of the top layer, e.g. Ti2C, Ti3C2O2, etc.')
        # parser.add_argument('top_shift', type=int,
        #                     help='Shift the registry of the top layer by a certain number of positions (default: 0)')
    parser.add_argument('top_vacancy_condition', type=str,
                        help='The condition of the vacancy to create in the top layer (default: None/pristine)')
    parser.add_argument('applied_gap', type=float,
                        help='The applied gap between the layers in Angstroms (default: 3.0)')
    args = parser.parse_args()
    try:
        bottom_shift = 0 # always starting with bottom layer unshifted, since registry shift is relative
        top_shift = SPEC2SHIFT[args.top_spec]
        relax_bilayer(args.size, args.bottom_spec, bottom_shift, args.bottom_vacancy_condition, args.top_spec, top_shift, args.top_vacancy_condition, args.applied_gap)
    except FileExistsError as exc:
        raise FileExistsError(
            f"Target run directory already exists: {exc.filename}. "
            "Choose a different configuration or remove the existing directory."
        ) from exc
    