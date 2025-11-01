import os
import re
import csv

RESULTS_DIR = "."  # Carpeta donde están los .log
OUTPUT_CSV = "parsed_results_kiwis.csv"

# Regex para extraer métricas
patterns = {
    "max_fringe": re.compile(r"Max fringe size:\s*(\d+)"),
    "cost": re.compile(r"Solution Cost:\s*(\d+)"),
    "length": re.compile(r"Solution Length:\s*(\d+)"),
    "expanded": re.compile(r"Search nodes expanded:\s*(\d+)"),
}

timeout_text = "alcanzó el límite de tiempo"

results = []

for filename in os.listdir(RESULTS_DIR):
    if not filename.endswith(".log"):
        continue

    algorithm = filename.replace(".log", "")

    full_path = os.path.join(RESULTS_DIR, filename)
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

        data = {"algorithm": algorithm, "filename": filename}

        if timeout_text in content:
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

# Escribir CSV
with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["algorithm", "timeout", "max_fringe", "cost", "length", "expanded", "filename"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print(f"✅ Resultados parseados correctamente → {OUTPUT_CSV}")



