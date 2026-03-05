from pathlib import Path
import shutil

def copy_poscar(src: Path, dest: Path):
    shutil.copy(src, dest / "POSCAR")

def get_system_name(poscar_path: Path) -> str:
    with open(poscar_path, 'r') as f:
        return f.readline().strip()
    
def write_poscar(poscar_text: str, dest: Path):
    target_dir = dest / "POSCAR"
    if target_dir.exists():
        raise FileExistsError(f"POSCAR already exists at {target_dir}")
    with open(dest / "POSCAR", 'w') as f:
        f.write(poscar_text)

def get_header(poscar_path: Path) -> str:
    with open(poscar_path, 'r') as f:
        return f.readline().strip()

def get_ions(poscar_path: Path) -> list:
    with open(poscar_path, 'r') as f:
        lines = f.readlines()
    return sum([int(lines[6].split()[i]) for i in range(len(lines[6].split()))])