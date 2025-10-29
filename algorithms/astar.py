from hlogedu.search.algorithm import Algorithm, Node, Solution
from hlogedu.search.containers import PriorityQueue

class Tree_Astar(Algorithm):
    NAME = "my-tree-astar"
    
    def __init__(self, problem):
        super().__init__(problem)
    
    def run(self, heuristic=None):
        # Si no se proporciona heurística, usar la del problema
        if heuristic is None:
            heuristic = self.problem.heuristic
        
        expand_counter = 0
        roots = [Node(s) for s in self.problem.get_start_states()]
        self.fringe = PriorityQueue()
        
        for n in roots:
            if self.problem.is_goal_state(n.state):
                return Solution(self.problem, roots, solution_node=n)
            priority = n.cost + heuristic(n.state)
            self.fringe.push(n, priority)
        
        while self.fringe:
            n = self.fringe.pop()
            expand_counter += 1
            n.expand_order = expand_counter
            
            for s, a, c in sorted(self.problem.get_successors(n.state), 
                                 key=lambda x: x[0]):
                ns = Node(s, a, cost=n.cost + c, parent=n)
                n.add_successor(ns)
                
                if self.problem.is_goal_state(ns.state):
                    return Solution(self.problem, roots, solution_node=ns)
                
                priority = ns.cost + heuristic(ns.state)
                self.fringe.push(ns, priority)
        
        return Solution(self.problem, roots)
    
class Graph_Astar(Algorithm):
    NAME = "my-graph-astar"
    
    def __init__(self, problem):
        super().__init__(problem)
    
    def run(self, heuristic=None):
        # Si no se proporciona heurística, usar la del problema
        if heuristic is None:
            heuristic = self.problem.heuristic
        
        expand_counter = 0
        roots = [Node(s) for s in self.problem.get_start_states()]
        self.fringe = PriorityQueue()
        
        for n in roots:
            if self.problem.is_goal_state(n.state):
                return Solution(self.problem, roots, solution_node=n)
            priority = n.cost + heuristic(n.state)
            self.fringe.push(n, priority)
        
        while self.fringe:
            n = self.fringe.pop()
            expand_counter += 1
            n.expand_order = expand_counter
            
            for s, a, c in sorted(self.problem.get_successors(n.state), 
                                 key=lambda x: x[0]):
                ns = Node(s, a, cost=n.cost + c, parent=n)
                n.add_successor(ns)
                
                if self.problem.is_goal_state(ns.state):
                    return Solution(self.problem, roots, solution_node=ns)
                
                priority = ns.cost + heuristic(ns.state)
                self.fringe.push(ns, priority)
        
        return Solution(self.problem, roots)