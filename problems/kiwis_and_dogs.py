from dataclasses import dataclass

from hlogedu.search.problem import Problem, action, Categorical, DDRange


@dataclass(frozen=True, order=True)
class State:
    kiwis: tuple[str]
    dogs: tuple[str]


class KiwisAndDogsProblem(Problem):
    NAME = "kiwis-and-dogs"

    def __init__(self):
        super().__init__()
        self.graph = {
            ("A", "B"): (3, "nobody(E)"),
            ("A", "C"): (4, ""),
            ("B", "A"): (3, "nobody(E)"),
            ("B", "C"): (1, ""),
            ("B", "G"): (5, ""),
            ("C", "B"): (1, ""),
            ("C", "D"): (2, "somebody(E),somebody(G)"),
            ("D", "C"): (2, "somebody(E),somebody(G)"),
            ("D", "E"): (8, "somebody(A)"),
            ("D", "F"): (3, "somebody(C)"),
            ("E", "D"): (8, "somebody(A)"),
            ("E", "F"): (5, ""),
            ("F", "D"): (3, "somebody(C)"),
            ("G", "F"): (7, ""),
            ("G", "B"): (5, ""),
        }
        self.num_kiwis = 2
        self.num_dogs = 1

    def get_start_states(self):
        return [State(kiwis=("D", "F"), dogs=("C",))]

    def is_goal_state(self, state):
        return all(pos == "A" for pos in state.kiwis) and all(pos == "E" for pos in state.dogs)

    def is_valid_state(self, _):
        return True

    ###############
    #  AUX FUNC   #
    ###############

    def get_valid_moves(self, current_pos, state):
        valid_pos = []
        for (source, destination), (cost, conditions) in self.graph.items():
            if source != current_pos:
                continue
            valid = True
            if conditions:
                for condition in conditions.split(","):
                    condition = condition.strip()
                    if condition.startswith("nobody"):
                        node = condition[8:-1]
                        if node in state.kiwis or node in state.dogs:
                            valid = False
                    elif condition.startswith("somebody"):
                        node = condition[9:-1]
                        if node not in state.kiwis and node not in state.dogs:
                            valid = False
            if valid:
                valid_pos.append((destination, cost))
        return valid_pos

    ###############
    #   ACTIONS   #
    ###############

    @action(
        DDRange(0, 'num_kiwis'),
        Categorical(["A", "B", "C", "D", "E", "F", "G"])
    )
    def move_kiwi(self, state, kiwi_id, destination):
        current_pos = state.kiwis[kiwi_id]
        valid_moves = self.get_valid_moves(current_pos, state)

        move_cost = None
        for dst, cost in valid_moves:
            if dst == destination:
                move_cost = cost
                break

        if move_cost is None:
            return None

        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_id] = destination
        new_state = State(kiwis=tuple(new_kiwis), dogs=state.dogs)

        return move_cost, new_state

    @action(
        DDRange(0, 'num_dogs'),
        Categorical(["A", "B", "C", "D", "E", "F", "G"])
    )
    def move_dog(self, state, dog_id, destination):
        current_pos = state.dogs[dog_id]
        valid_moves = self.get_valid_moves(current_pos, state)

        move_cost = None
        for dst, cost in valid_moves:
            if dst == destination:
                move_cost = cost
                break

        if move_cost is None:
            return None

        new_dogs = list(state.dogs)
        new_dogs[dog_id] = destination
        new_state = State(kiwis=state.kiwis, dogs=tuple(new_dogs))

        return move_cost, new_state
