from hlogedu.search.problem import Problem, action, Categorical


class AiExam1516P4(Problem):
    NAME = "a"
    def __init__(self):
        self.graph = {
            ("A", "B"): 4,
            ("A", "C"): 2,
            ("B", "D"): 2,
            ("C", "A"): 0.5,
            ("C", "E"): 3,
            ("D", "G1"): 4,
            ("D", "G2"): 10,
            ("E", "G1"): 1,
            ("E", "G2"): 10,
        }

        self.start_states = ["A"]
        self.goal_states = set(["G1", "G2"])

    def get_start_states(self):
        return self.start_states

    def is_goal_state(self, state):
        return state in self.goal_states

    def is_valid_state(self, _):
        return True

    @action(Categorical(["A", "B", "C", "D", "E", "G1", "G2"]))
    def move(self, state, dest):
        edge = (state, dest)

        if edge in self.graph:
            return self.graph[edge], dest

        return None