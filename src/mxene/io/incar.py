from pathlib import Path
import shutil

def copy_incar(src: Path, dest: Path):
    shutil.copy(src, dest / "INCAR")

def change_system_name(incar_path: Path, new_name: str):
    with open(incar_path, 'r') as f:
        lines = f.readlines()
    
    with open(incar_path, 'w') as f:
        for line in lines:
            if line.startswith("SYSTEM"):
                f.write(f"SYSTEM = {new_name}\n")
            else:
                f.write(line)