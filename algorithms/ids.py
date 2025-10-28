from hlogedu.search.algorithm import Algorithm, Node, Solution
from hlogedu.search.containers import Stack

class TreeIDS(Algorithm):
    NAME = "my-tree-ids"
    
    def __init__(self, problem, max_depth=20):
        super().__init__(problem) 
        self.max_depth = max_depth
    
    def run(self, max_depth=None):
        if max_depth is None:
            max_depth = self.max_depth
            
        expand_counter = 0
        
        for depth_limit in range(max_depth + 1):
            cutoff = False 
            roots = [Node(s) for s in self.problem.get_start_states()]
            self.fringe = Stack()
            
            for n in roots:
                if self.problem.is_goal_state(n.state):
                    return Solution(self.problem, roots, solution_node=n, cutoff=False)
                self.fringe.push(n)
            
            while self.fringe:
                n = self.fringe.pop()
                
                if n.depth >= depth_limit:
                    cutoff = True
                else:
                    expand_counter += 1
                    n.expand_order = expand_counter
                    
                    for s, a, c in sorted(self.problem.get_successors(n.state), 
                                         key=lambda x: x[0]):
                        ns = Node(s, a, cost=n.cost + c, parent=n)
                        n.add_successor(ns)
                        
                        if self.problem.is_goal_state(ns.state):
                            return Solution(self.problem, roots, solution_node=ns, 
                                          cutoff=False)
                        
                        self.fringe.push(ns)
            if not cutoff:
                break
        
        return Solution(self.problem, roots, cutoff=cutoff)