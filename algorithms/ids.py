from hlogedu.search.algorithm import Algorithm, Node, Solution
from hlogedu.search.containers import Queue

"""Codigo Ejemplo para hacer luego el IDS"""
class TreeBfs(Algorithm):
    NAME = "my-tree-bfs"

    def __init__(self, problem):
        super().__init__(problem)
        self.fringe = Queue()

    def run(self):
        expand_counter = 0
        roots = [Node(s) for s in self.problem.get_start_states()]

        for n in roots:
            if self.problem.is_goal_state(n.state):
                return Solution(self.problem, roots, solution_node=n)
            self.fringe.push(n)

        while self.fringe:
            n = self.fringe.pop()
            expand_counter += 1
            n.expand_order = expand_counter
            # for s, a, c in self.problem.get_successors(n.state):
            for s, a, c in sorted(
                self.problem.get_successors(n.state), key=lambda x: x[0]
            ):
                ns = Node(s, a, cost=n.cost + c, parent=n)
                n.add_successor(ns)
                if self.problem.is_goal_state(ns.state):
                    return Solution(self.problem, roots, solution_node=ns)
                self.fringe.push(ns)

        return Solution(self.problem, roots)