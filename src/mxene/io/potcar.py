# src/mxene/io/potcar.py

def get_potcar_specs(potcar_path):
    specs = []
    with open(potcar_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "TITEL" in line:
                spec = line.split()[-2]
                date = line.split()[-1]
                specs.append(spec)
    return specs