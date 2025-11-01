#!/bin/bash

PROBLEM="kiwis-and-dogs"
OUTPUT_DIR="results"
TIME_LIMIT=1200  # 20 minutos

mkdir -p "$OUTPUT_DIR"

# Obtener lista de algoritmos hlog-*
ALGORITHMS=$(hlogedu-search list | grep -o "hlog-[a-zA-Z0-9-]*")

echo "=== Ejecutando kiwis-and-dogs con algoritmos hlog-* ==="
echo "Tiempo límite por ejecución: $TIME_LIMIT segundos"
echo "Resultados en: $OUTPUT_DIR/"
echo ""

for ALG in $ALGORITHMS; do
    LOGFILE="$OUTPUT_DIR/${ALG}.log"
    
    echo "Ejecutando $ALG ..."
    
    # Ejecutar con límite de tiempo
    timeout $TIME_LIMIT \
        hlogedu-search run -a "$ALG" \
        -p "${PROBLEM}" \
        -o none \
        -v 3 > "$LOGFILE" 2>&1

    # Comprobar si terminó por timeout
    if [ $? -eq 124 ]; then
        echo "⏳ $ALG alcanzó el límite de tiempo" | tee -a "$LOGFILE"
    else
        echo "✅ $ALG completado"
    fi
done

echo ""
echo "✅ Todos los experimentos han finalizado"
