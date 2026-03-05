# src/mxene/structures/am_helper_functions.py
import atomman as am
import numpy as np

def remap_types(system, new_symbols):
    old_symbols = system.symbols
    mapping = {i+1: new_symbols.index(sym) + 1
               for i, sym in enumerate(old_symbols)}

    new_atype = np.array([mapping[t] for t in system.atoms.atype])

    new_system = am.System(
        atoms=system.atoms,
        box=system.box,
        pbc=system.pbc,
        symbols=new_symbols
    )

    new_system.atoms.atype = new_atype
    return new_system

def floor_zs(system, floor=0.0):
    min_z = system.atoms.pos[:,2].min()
    shift = floor - min_z
    system.atoms.pos[:,2] += shift
    new_z = system.atoms.pos[:,2].copy()
    system.atoms.pos[:,2] = new_z

    return system