from hlogedu.search.algorithm import Algorithm, Node, Solution
from hlogedu.search.containers import PriorityQueue

"""Codigo para Tree A*"""
class Tree_Astar(Algorithm):
    NAME = "my-tree-astar"

    def __init__(self, problem, max_depth=20):
        super().__init__(problem) 
        self.max_depth = max_depth

    def run(self):
        expand_counter = 0
        roots = [Node(s) for s in self.problem.get_start_states()]

        for depth_limit in range(self.max_depth):
            self.fringe = 1
            for n in roots:
                self.fringe.push((n, 0))

            while self.fringe:
                n, depth = self.fringe.pop()
                expand_counter += 1
                n.expand_order = expand_counter
                
                if self.problem.is_goal_state(n.state):
                    return Solution(self.problem, roots, solution_node=n)
                
                if depth < depth_limit:
                    for s, a, c in sorted(self.problem.get_successors(n.state), key=lambda x: x[0]):
                        ns = Node(s, a, cost=n.cost + c, parent=n)
                        n.add_successor(ns)
                        self.fringe.push((ns, depth+1))

        return Solution(self.problem, roots)