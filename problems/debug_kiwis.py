from kiwis_and_dogs import KiwisAndDogsProblem

problem = KiwisAndDogsProblem()

# Ver estado inicial
print("Estado inicial:")
start_states = problem.get_start_states()
for state in start_states:
    print(f"  {state}")

# Ver si es estado objetivo
print("\n¿Es estado objetivo?")
for state in start_states:
    print(f"  {problem.is_goal_state(state)}")

# Ver vértices disponibles
print("\nVértices del grafo:")
try:
    vertices = problem.get_graph_vertices(None)
    print(f"  {vertices}")
except Exception as e:
    print(f"  Error: {e}")

# Ver sucesores del estado inicial usando el framework
print("\nGenerando sucesores del estado inicial:")
state = start_states[0]

try:
    # El framework genera los sucesores automáticamente
    for action_name, successor_state, cost in problem.get_successors(state):
        print(f"  {action_name}: {successor_state} (costo: {cost})")
except Exception as e:
    print(f"  Error generando sucesores: {e}")
    import traceback
    traceback.print_exc()

# Ver información del estado objetivo
print("\nInformación del objetivo:")
print(f"  Árbol (tree): {problem.tree_vertex}")
print(f"  Hueso (bone): {problem.bone_vertex}")
print(f"  Kiwis en el estado inicial: {state.kiwis}")
print(f"  Perros en el estado inicial: {state.dogs}")