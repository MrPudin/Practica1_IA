import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Leer CSV
df = pd.read_csv("parsed_results_kiwis.csv")

# Ordenar algoritmos para mantener siempre el mismo orden
df = df.sort_values("algorithm").reset_index(drop=True)
algorithms = df["algorithm"]

# Valores numéricos, convertir a float y reemplazar NaN para timeouts
max_fringe = pd.to_numeric(df["max_fringe"], errors='coerce')
expanded = pd.to_numeric(df["expanded"], errors='coerce')
cost = pd.to_numeric(df["cost"], errors='coerce')

# Colores: timeout → rojo, resuelto → azul
bar_colors = df["timeout"].map({True: "red", False: "skyblue"})

# Posiciones para barras agrupadas
x = np.arange(len(algorithms))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))

# Barras: Max Fringe y Nodos Expandidos
bars1 = ax.bar(x - width/2, max_fringe, width, label="Max Fringe", color=bar_colors)
bars2 = ax.bar(x + width/2, expanded, width, label="Nodos Expandidos", color=bar_colors, alpha=0.7)

# Línea: Coste de solución
ax2 = ax.twinx()
ax2.plot(x, cost, color='green', marker='o', linestyle='-', label="Coste de Solución")

# Etiquetas timeout
for i, timeout in enumerate(df["timeout"]):
    if timeout:
        ax.text(i - width/2, 0.5, "X", color="red", ha='center', va='bottom', fontsize=12)
        ax.text(i + width/2, 0.5, "X", color="red", ha='center', va='bottom', fontsize=12)
        ax2.text(i, 0.5, "X", color="red", ha='center', va='bottom', fontsize=12)

# Ajustes estéticos
ax.set_xticks(x)
ax.set_xticklabels(algorithms, rotation=45, ha='right')
ax.set_ylabel("Max Fringe / Nodos Expandidos")
ax2.set_ylabel("Coste de Solución")
ax.set_title("Comparativa Algoritmos - Kiwis and Dogs Problem")
ax.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.tight_layout()
plt.savefig("kiwis_algorithms_compact.png", dpi=300)
plt.show()
