import os
import re
import csv

RESULTS_DIR = "."  # carpeta con los logs
OUTPUT_CSV = "parsed_results_nqueens.csv"

# Regex para extraer info del nombre del archivo
# Ej: hlog-tree-ucs_N7_S1.log
filename_regex = re.compile(
    r"hlog-(?P<type>tree|graph)-(?P<algorithm>ucs|astar)_N(?P<N>\d+)_S(?P<seed>\d+)\.log"
)

# Regex para métricas
patterns = {
    "max_fringe": re.compile(r"Max fringe size:\s*(\d+)"),
    "cost": re.compile(r"Solution Cost:\s*(\d+)"),
    "length": re.compile(r"Solution Length:\s*(\d+)"),
    "expanded": re.compile(r"Search nodes expanded:\s*(\d+)"),
}

# Detectar timeout o kill
timeout_text = "alcanzó el límite de tiempo"
killed_text = "Terminado (killed)"

results = []

for filename in os.listdir(RESULTS_DIR):
    if not filename.endswith(".log"):
        continue

    match = filename_regex.match(filename)
    if not match:
        print(f"⚠️ Nombre no válido, ignorado: {filename}")
        continue

    data = match.groupdict()
    data["filename"] = filename

    full_path = os.path.join(RESULTS_DIR, filename)
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

        # Detectar timeout o killed
        if timeout_text in content or killed_text in content:
            data["timeout"] = True
            data["max_fringe"] = ""
            data["cost"] = ""
            data["length"] = ""
            data["expanded"] = ""
        else:
            data["timeout"] = False
            for key, pattern in patterns.items():
                m = pattern.search(content)
                data[key] = m.group(1) if m else ""

    results.append(data)

# Guardar CSV
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["type", "algorithm", "N", "seed", "timeout", "max_fringe", "cost", "length", "expanded", "filename"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Resultados parseados correctamente → {OUTPUT_CSV}")
