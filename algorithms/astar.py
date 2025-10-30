from hlogedu.search.algorithm import Algorithm, Node, Solution
from hlogedu.search.containers import PriorityQueue

class Tree_Astar(Algorithm):
    NAME = "my-tree-astar"

    def __init__(self, problem):
        super().__init__(problem)

    def run(self, heuristic=None):
        if heuristic is None:
            heuristic = self.problem.heuristic

        expand_counter = 0
        roots = [Node(s) for s in self.problem.get_start_states()]
        self.fringe = PriorityQueue(key=lambda node: node.state)  # Para tie-breaking estable

        # Inicializar fringe con nodos raíz
        for n in roots:
            if self.problem.is_goal_state(n.state):
                n.expand_order = 0
                return Solution(self.problem, roots, solution_node=n)
            self.fringe.push(n, n.cost + heuristic(n.state))

        while self.fringe:
            n = self.fringe.pop()

            # Si es objetivo → devolver inmediatamente
            if self.problem.is_goal_state(n.state):
                return Solution(self.problem, roots, solution_node=n)

            # Expandir nodo
            expand_counter += 1
            n.expand_order = expand_counter

            # Expandir sucesores en orden lexicográfico
            for s, a, c in sorted(self.problem.get_successors(n.state), key=lambda x: x[0]):
                ns = Node(s, a, cost=n.cost + c, parent=n)
                n.add_successor(ns)
                f_new = ns.cost + heuristic(ns.state)
                self.fringe.push(ns, f_new)

        return Solution(self.problem, roots)

class Graph_Astar(Algorithm):
    NAME = "my-graph-astar"

    def __init__(self, problem):
        super().__init__(problem)

    def run(self, heuristic=None):
        if heuristic is None:
            heuristic = self.problem.heuristic

        expand_counter = 0
        best_cost = {}  # Mejor coste g conocido para cada estado

        roots = [Node(s) for s in self.problem.get_start_states()]
        # PriorityQueue con key=node.state para romper empates de forma estable
        self.fringe = PriorityQueue(key=lambda node: node.state)

        # Inicializar fringe con los nodos raíz
        for n in roots:
            if self.problem.is_goal_state(n.state):
                n.expand_order = 0
                return Solution(self.problem, roots, solution_node=n)
            f = n.cost + heuristic(n.state)
            best_cost[n.state] = n.cost
            self.fringe.push(n, f)

        while self.fringe:
            n = self.fringe.pop()

            # Si es objetivo → devolver inmediatamente
            if self.problem.is_goal_state(n.state):
                return Solution(self.problem, roots, solution_node=n)

            # Poda clásica: ignorar si ya tenemos mejor coste
            if n.state in best_cost and n.cost > best_cost[n.state]:
                continue

            # Expandir nodo
            expand_counter += 1
            n.expand_order = expand_counter
            best_cost[n.state] = n.cost

            # Expandir sucesores en orden lexicográfico
            for s, a, c in sorted(self.problem.get_successors(n.state), key=lambda x: x[0]):
                g_new = n.cost + c

                # Solo agregar al fringe si mejora el coste o es nuevo
                if s not in best_cost or g_new < best_cost[s]:
                    ns = Node(s, a, cost=g_new, parent=n)
                    n.add_successor(ns)
                    f_new = g_new + heuristic(s)
                    self.fringe.push(ns, f_new)
                    best_cost[s] = g_new  # actualizar coste
