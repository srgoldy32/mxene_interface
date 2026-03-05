# src/mxene/io/output.py
from pathlib import Path

def get_last_n_lines(output_path: Path, n):
    with open(output_path, 'r') as f:
        lines = f.readlines()
        return lines[-n:]