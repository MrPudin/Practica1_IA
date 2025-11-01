#!/bin/bash

PROBLEM="NQueensIR"
OUTPUT_DIR="results_nqueens_all"
TIME_LIMIT=300  # 5 minutos por ejecución

mkdir -p "$OUTPUT_DIR"

# Algoritmos GRAPH + TREE de UCS y A*
ALGORITHMS="hlog-graph-ucs hlog-graph-astar hlog-tree-ucs hlog-tree-astar"

echo "=== Experimentos NQueensIR con Graph & Tree ==="
echo "Directorio de resultados: $OUTPUT_DIR/"
echo ""

for ALG in $ALGORITHMS; do
  for N in 4 5 6 7 8 9 10; do
    for SEED in 1 2 3 4 5; do

      LOGFILE="$OUTPUT_DIR/${ALG}_N${N}_S${SEED}.log"

      # Si ya existe → se salta
      if [ -f "$LOGFILE" ]; then
        echo "⏩ Ya existe: $ALG N=$N SEED=$SEED — saltando"
        continue
      fi

      echo "▶ Ejecutando: $ALG | N=$N | SEED=$SEED"

      # Comando base
      CMD="hlogedu-search run -a $ALG -p $PROBLEM -o none \
           -pp n_queens=$N -pp seed=$SEED -v 3"

      # Si es A* ⇒ añadir heurística
      if [[ "$ALG" == *"astar"* ]]; then
        CMD="$CMD -hf RepairHeuristic"
      fi

      # Ejecutar con límite de tiempo
      timeout $TIME_LIMIT bash -c "$CMD" > "$LOGFILE" 2>&1

      # Comprobar timeout
      if [ $? -eq 124 ]; then
        echo "⏳ TIMEOUT $ALG N=$N SEED=$SEED" | tee -a "$LOGFILE"
      else
        echo "✅ Completado $ALG N=$N SEED=$SEED"
      fi

    done
  done
done

echo ""
echo "✅ Todos los experimentos terminados (o ya existentes)"
echo "Resultados en: $OUTPUT_DIR/"
