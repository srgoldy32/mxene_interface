from pathlib import Path
import shutil

def copy_poscar(src: Path, dest: Path):
    shutil.copy(src, dest / "POSCAR")
def get_system_name(poscar_path: Path) -> str:
    with open(poscar_path, 'r') as f:
        return f.readline().strip()