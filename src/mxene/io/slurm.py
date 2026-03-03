# io/slurm.py

from pathlib import Path

def render_slurm(template_path: Path, output_path: Path, job_name: str):
    content = template_path.read_text()
    content = content.replace("JOBNAME", job_name)
    output_path.write_text(content)