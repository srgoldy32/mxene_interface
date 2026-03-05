# src/mxene/structures/bilayer.py
import atomman as am

from .am_helper_functions import remap_types, floor_zs
from mxene.constants.constants import ADDITIONAL_VACCUM
from mxene.io.poscar import get_header

def make_bilayer(bottom_file, top_file, applied_gap,):
    # header = f'{spec} monolayer, {size}, shift = {shift},  {vacancy_condition}'
    top_header = get_header(top_file)
    bottom_header = get_header(bottom_file)
    header = f'({bottom_header}) on ({top_header}) with applied gap = {applied_gap} Angstrom'


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