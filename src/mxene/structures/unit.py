# src/mxene/structures/unit.py
import atomman as am
import numpy as np

def get_possible_vacancies(spec):
    unit = am.load('poscar', f'units/contcars/{spec}.poscar')
    # sort atoms by z position
    height_sorted_inds = np.argsort(unit.atoms.pos[:,2])
    
    return height_sorted_inds

