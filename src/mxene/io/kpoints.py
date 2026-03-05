# src/mxene/io/kpoints.py

def get_kpoints(kpoints_path):
    with open(kpoints_path, 'r') as f:
        lines = f.readlines()
    x_line = lines[3].split()
    out = f'{lines[2].split()[0]} - {x_line[0]}x{x_line[1]}x{x_line[-1]} - {lines[0].split()[0]} {lines[0].split()[-1]} '
    return out