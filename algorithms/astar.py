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
        self.fringe = PriorityQueue()
        
        for n in roots:
            if self.problem.is_goal_state(n.state):
                return Solution(self.problem, roots, solution_node=n)
            self.fringe.push(n, n.cost + heuristic(n.state))
        
        while self.fringe:
            n = self.fringe.pop()
            
            if self.problem.is_goal_state(n.state):
                return Solution(self.problem, roots, solution_node=n)
            
            expand_counter += 1
            n.expand_order = expand_counter
            
            for s, a, c in sorted(self.problem.get_successors(n.state),
                                  key=lambda x: x[0]):
                ns = Node(s, a, cost=n.cost + c, parent=n)
                n.add_successor(ns)
                self.fringe.push(ns, ns.cost + heuristic(ns.state))
        
        return Solution(self.problem, roots)

class Graph_Astar(Algorithm):
    NAME = "my-graph-astar"
    
    def __init__(self, problem):
        super().__init__(problem)
    
    def run(self, heuristic=None):
        if heuristic is None:
            heuristic = self.problem.heuristic
        
        expand_counter = 0
        expanded = {} 
        
        roots = [Node(s) for s in self.problem.get_start_states()]
        self.fringe = PriorityQueue()
        
        for n in roots:
            if self.problem.is_goal_state(n.state):
                return Solution(self.problem, roots, solution_node=n)
                
            expanded[n.state] = 0
            self.fringe.push(n, n.cost + heuristic(n.state))
        
        while self.fringe:
            n = self.fringe.pop()

            if self.problem.is_goal_state(n.state):
                return Solution(self.problem, roots, solution_node=n)
            
            expand_counter += 1 
            n.expand_order = expand_counter
            
            for s, a, c in sorted(self.problem.get_successors(n.state),
                                  key=lambda x: x[0]):
                g_new = n.cost + c
                
                if s in expanded and g_new >= expanded[s]:
                    continue
                
                expanded[s] = g_new
                
                ns = Node(s, a, cost=g_new, parent=n)
                n.add_successor(ns)

                self.fringe.push(ns, g_new + heuristic(s))
        
        return Solution(self.problem, roots)
