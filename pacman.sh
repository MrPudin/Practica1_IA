#!/bin/bash

# --- Configuración ---
PROBLEM="Pacman"
LAYOUT_DIR="problems/layouts"
OUTPUT_DIR="results_pacman"
TIME_LIMIT=300  # segundos por ejecución

# Crear directorio de salida
mkdir -p "$OUTPUT_DIR"

# Validar que el directorio de layouts existe
if [ ! -d "$LAYOUT_DIR" ]; then
    echo "❌ Error: No se encontró el directorio $LAYOUT_DIR"
    exit 1
fi

# --- Algoritmos (ya incluyen graph/tree en el nombre) ---
ALGORITHMS=(
    "hlog-graph-bfs"
    "hlog-tree-bfs"
    "hlog-graph-ucs"
    "hlog-tree-ucs"
    "hlog-graph-astar"
    "hlog-tree-astar"
    "my-graph-astar"
    "my-tree-astar"
    "my-tree-ids"
)

# --- Heurísticas para A* ---
HEURISTICS=(
    "PacmanManhattanHeuristic"
    "PacmanEuclideanHeuristic"
)

# --- Layouts ---
LAYOUTS=($(ls "$LAYOUT_DIR"/*.lay 2>/dev/null | xargs -n1 basename))

# Validar que hay layouts
if [ ${#LAYOUTS[@]} -eq 0 ]; then
    echo "❌ Error: No se encontraron archivos .lay en $LAYOUT_DIR"
    exit 1
fi

echo "📋 Layouts encontrados: ${#LAYOUTS[@]}"
echo "🔍 Algoritmos a ejecutar: ${#ALGORITHMS[@]}"
echo ""

# --- Función para ejecutar ---
run_algorithm() {
    local alg="$1"
    local layout="$2"
    local heuristic="$3"
    
    # Nombre del archivo de log
    local LOGFILE="$OUTPUT_DIR/${alg}"
    [ -n "$heuristic" ] && LOGFILE+="-${heuristic}"
    LOGFILE+="_${layout%.lay}.log"
    
    # Saltar si ya existe
    if [ -f "$LOGFILE" ]; then
        echo "⏩ Saltando $LOGFILE (ya existe)"
        return 0
    fi
    
    echo "🚀 Ejecutando: $alg | $layout ${heuristic:+| $heuristic}"
    
    # Ejecutar con timeout
    if [ -n "$heuristic" ]; then
        timeout $TIME_LIMIT hlogedu-search run \
            -a "$alg" \
            -p "$PROBLEM" \
            -o none \
            -pp file="$LAYOUT_DIR/$layout" \
            -hf "$heuristic" \
            > "$LOGFILE" 2>&1
    else
        timeout $TIME_LIMIT hlogedu-search run \
            -a "$alg" \
            -p "$PROBLEM" \
            -o none \
            -pp file="$LAYOUT_DIR/$layout" \
            > "$LOGFILE" 2>&1
    fi
    
    # Verificar resultado
    local exit_code=$?
    
    if [ $exit_code -eq 124 ]; then
        echo "⏳ TIMEOUT: $alg alcanzó el límite de tiempo ($TIME_LIMIT segundos)" | tee -a "$LOGFILE"
        return 1
    elif [ $exit_code -eq 0 ]; then
        echo "✅ $alg completado exitosamente"
        return 0
    else
        echo "❌ $alg falló con código de error: $exit_code" | tee -a "$LOGFILE"
        return 1
    fi
}

# --- Loop principal ---
TOTAL=0
COMPLETED=0
FAILED=0

for layout in "${LAYOUTS[@]}"; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📂 Procesando layout: $layout"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    for alg in "${ALGORITHMS[@]}"; do
        
        # Detectar si es A* para probar heurísticas
        if [[ "$alg" == *"astar"* ]]; then
            for h in "${HEURISTICS[@]}"; do
                ((TOTAL++))
                run_algorithm "$alg" "$layout" "$h"
                if [ $? -eq 0 ]; then
                    ((COMPLETED++))
                else
                    ((FAILED++))
                fi
            done
        else
            # BFS, UCS, IDS (sin heurística)
            ((TOTAL++))
            run_algorithm "$alg" "$layout" ""
            if [ $? -eq 0 ]; then
                ((COMPLETED++))
            else
                ((FAILED++))
            fi
        fi
    done
    
    echo ""
done

# --- Resumen final ---
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 RESUMEN DE EJECUCIÓN"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📈 Total de ejecuciones: $TOTAL"
echo "✅ Completadas exitosamente: $COMPLETED"
echo "❌ Fallidas: $FAILED"
echo "📁 Directorio de resultados: $OUTPUT_DIR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✨ Experimento finalizado"