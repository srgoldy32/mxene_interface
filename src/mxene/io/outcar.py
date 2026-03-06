# src/mxene/io/outcar.py

from pathlib import Path

def get_wall_time(outcar_path: Path) -> str:
    with open(outcar_path, 'r') as f:
        for line in f:
            if "Elapsed time" in line:
                return float(line.split()[-1])
    raise ValueError(f"Elapsed time not found in {outcar_path}")

def get_final_energy(outcar_path: Path) -> float:
    with open(outcar_path, 'r') as f:
        for line in f:
            if "free  energy   TOTEN" in line:
                return float(line.split()[-2])
    raise ValueError(f"Final energy not found in {outcar_path}")