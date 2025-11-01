import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Leer CSV
df = pd.read_csv("parsed_results_nqueens.csv")

# Convertir columnas numéricas
num_cols = ["max_fringe", "cost", "expanded"]
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')  # coerce convierte vacíos en NaN

# Convertir timeout a boolean
df["timeout"] = df["timeout"].astype(bool)

# Crear columna combinada type-algorithm
df["label"] = df["type"] + "-" + df["algorithm"]

# Ordenar
df = df.sort_values(["N", "label", "seed"]).reset_index(drop=True)

# Colores por algoritmo
algo_colors = {
    "tree-ucs": "#1f77b4",
    "tree-astar": "#ff7f0e",
    "graph-ucs": "#2ca02c",
    "graph-astar": "#d62728"
}

# Preparar gráfico
N_values = sorted(df["N"].unique())
labels = df["label"].unique()
num_labels = len(labels)
width = 0.15
x = np.arange(len(N_values))

fig, ax = plt.subplots(figsize=(14, 7))

for i, label in enumerate(labels):
    subset = df[df["label"] == label]
    
    # Media ignorando NaN
    avg_max_fringe = subset.groupby("N")["max_fringe"].mean()
    timeout = subset.groupby("N")["timeout"].any()
    
    pos = x + (i - num_labels/2) * width + width/2
    
    for j, n in enumerate(N_values):
        val = avg_max_fringe.get(n, 0)
        # Solo poner label en la primera barra de cada algoritmo
        bar_label = label if j == 0 else "_nolegend_"
        
        if timeout.get(n, False) or np.isnan(val):
            # Timeout o valores vacíos → barra punteada
            ax.bar(pos[j], val if not np.isnan(val) else 0, width,
                   color=algo_colors[label], alpha=0.3, hatch='//',
                   label=bar_label)
            ax.text(pos[j], max(val*0.1 if not np.isnan(val) else 0.5, 0.5),
                    "X", color="black", ha='center', va='bottom', fontsize=10)
        else:
            ax.bar(pos[j], val, width, color=algo_colors[label], alpha=0.8,
                   label=bar_label)


# Línea coste promedio (ignora NaN)
ax2 = ax.twinx()
for label in labels:
    subset = df[df["label"] == label]
    avg_cost = subset.groupby("N")["cost"].mean()
    ax2.plot(x, avg_cost, marker='o', linestyle='-', label=f"Cost {label}")

# Ajustes
ax.set_xticks(x)
ax.set_xticklabels([f"N={n}" for n in N_values])
ax.set_ylabel("Max Fringe")
ax2.set_ylabel("Coste de Solución")
ax.set_title("Comparativa Algoritmos - NQueens Problem")
ax.legend(loc='upper left', fontsize=10)
ax2.legend(loc='upper right', fontsize=10)

plt.tight_layout()
plt.savefig("nqueens_algorithms_comparison.png", dpi=300)
plt.show()
