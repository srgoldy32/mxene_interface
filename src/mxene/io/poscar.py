from pathlib import Path
import shutil

def copy_poscar(src: Path, dest: Path):
    shutil.copy(src, dest / "POSCAR")

def get_system_name(poscar_path: Path) -> str:
    with open(poscar_path, 'r') as f:
        return f.readline().strip()
    
def write_poscar(poscar_text: str, dest: Path):
    with open(dest / "POSCAR", 'w') as f:
        f.write(poscar_text)

def get_header(poscar_path: Path) -> str:
    with open(poscar_path, 'r') as f:
        return f.readline().strip()