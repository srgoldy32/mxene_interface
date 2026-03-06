# src/mxene/structures/bilayer.py
import atomman as am
from pathlib import Path
import numpy as np

from .am_helper_functions import remap_types, floor_zs
from mxene.constants.constants import ADDITIONAL_VACCUM
from mxene.io.poscar import get_header

def make_bilayer(bottom_file: Path, top_file: Path, applied_gap: float):
    if bottom_file.exists() == False:
        raise FileNotFoundError(f"Bottom file not found: {bottom_file}")
    if top_file.exists() == False:
        raise FileNotFoundError(f"Top file not found: {top_file}")
    top_header = get_header(top_file)
    bottom_header = get_header(bottom_file)
    header = f'({bottom_header}) on ({top_header}) with applied gap = {applied_gap} Angstrom'
    print('AM Making bilayer: ', header)

    bottom = am.load('poscar', bottom_file)
    top = am.load('poscar', top_file)


    dzs = [layer.atoms.pos[:,2].max() - layer.atoms.pos[:,2].min() for layer in [bottom, top]]
    
    full_z = sum(dzs) + ADDITIONAL_VACCUM
    mid_z = full_z/2


    half_gap = applied_gap/2
  

    top = floor_zs(top)
    top.atoms.pos[:,2] += mid_z + half_gap - dzs[1]/2 # shift the top layer up by its thickness
    new_z = top.atoms.pos[:,2].copy()
    top.atoms.pos[:,2] = new_z

    bottom = floor_zs(bottom)
    bottom.atoms.pos[:,2] += mid_z - half_gap - dzs[0]/2 # shift the bottom layer down by its thickness
    new_z = bottom.atoms.pos[:,2].copy()
    bottom.atoms.pos[:,2] = new_z
    
    # combine symbols and remap
    symbols = list(dict.fromkeys(bottom.symbols + top.symbols))
    bottom_new = remap_types(bottom, symbols)
    top_new = remap_types(top, symbols)

    
    new_sys = bottom_new.atoms_extend(top_new.atoms)
    new_sys.box.set(vects=[new_sys.box.avect,new_sys.box.bvect,[0,0,full_z]])
    new_sys.wrap()

    info = new_sys.dump('poscar')


    output = f"{header}{info}"
    return output

def fix_middles(bilayer_poscar_output:str):
    
    fixed = ' F F F'
    unfixed = ' T T T'
    lines = bilayer_poscar_output.split('\n')


    # collect the atomic z positions
    zs_frac = []
    for pos_line in lines[8:]:
        strip_line = pos_line.rstrip('\n')
        z_pos_frac = float(strip_line.split()[-1])  # fractional coordinate

        zs_frac.append(z_pos_frac)


    # # find middle of bottom layer and top layer
    zs_frac.sort()
    zs_frac = np.array(zs_frac)
    
    # layer_natoms = len(zs_frac) // 2

    mid_z = (zs_frac.max() + zs_frac.min()) / 2


    bottom_layer = [z for z in zs_frac if z < mid_z]
    top_layer = [z for z in zs_frac if z > mid_z]

    

    middle_zs_frac = [(max(bottom_layer) + min(bottom_layer)) / 2, (max(top_layer) + min(top_layer)) / 2]


    # remove new line character from this line
    for i in range(len(lines[8:])):
        lines[i+8] = lines[i+8].rstrip('\n')
        z_pos_frac = float(lines[i+8].split()[-1])  # fractional coordinate
        fix_condition = False
        for m in middle_zs_frac:
            if abs(z_pos_frac - m) < 0.01:
                fix_condition = True
        if fix_condition:
            lines[i+8] = lines[i+8] + fixed
        else:
            lines[i+8] = lines[i+8] + unfixed

    # inset selective dynamics flag
    lines.insert(7, 'Selective dynamics')
    

    return '\n'.join(lines)
