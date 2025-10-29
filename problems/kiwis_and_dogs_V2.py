from dataclasses import dataclass

from hlogedu.search.problem import Problem, action, Categorical, DDRange


@dataclass(frozen=True, order=True)
class State:
    kiwis: tuple[str]
    dogs: tuple[str]


# Problem
##############################################################################


class KiwisAndDogsProblem(Problem):
    NAME = "kiwis-and-dogsV2"

    def __init__(self):
        super().__init__()
        # Assume we only have `nobody(X)` and `somebody(X)` conditions.
        # In case of having more than one condition, these will always be
        # a conjunction and will be separated by a comma.
        self.graph = {
            # A
            ("A", "B"): (3, "nobody(E)"),
            ("A", "C"): (4, ""),
            # B
            ("B", "A"): (3, "nobody(E)"),
            ("B", "C"): (1, ""),
            ("B", "G"): (5, ""),
            # C
            ("C", "B"): (1, ""),
            ("C", "D"): (2, "somebody(E),somebody(G)"),
            # D
            ("D", "C"): (2, "somebody(E),somebody(G)"),
            ("D", "E"): (8, "somebody(A)"),
            ("D", "F"): (3, "somebody(C)"),
            # E
            ("E", "D"): (8, "somebody(A)"),
            ("E", "F"): (5, ""),
            # F
            ("F", "D"): (3, "somebody(C)"),
            # G
            ("G", "F"): (7, ""),
            ("G", "B"): (5, ""),
        }
        self.num_kiwis = 2
        self.num_dogs = 1

        self.move_kiwi.cost = lambda state, kiwi_id, destination: \
        self.get_move_cost(state.kiwis[kiwi_id], destination)

        self.move_dog.cost = lambda state, dog_id, destination: \
        self.get_move_cost(state.dogs[dog_id], destination)

    def get_start_states(self):
        return [State(kiwis=("D", "F"), dogs=("C"))]

    def is_goal_state(self, state):
        kiwis_at_tree = all(pos == "A" for pos in state.kiwis)
        dogs_at_bones = all(pos == "E" for pos in state.dogs)
        return kiwis_at_tree and dogs_at_bones

    def is_valid_state(self, _):
        return True
    
    ###############
    #  AUX FUNC   #
    ###############

    """ 
    Given a state and a current position, this method returns a list containing
    touples of the possible destinations and the associated cost of the
    specific movement
    """

    def get_valid_moves(self, current_pos, state):
        valid_pos = []
        for (source, destination), (cost, conditions) in self.graph.items():
            if source != current_pos:
                continue
            valid = True
            if conditions: # "" ---> False, "something" ---> True
                for condition in conditions.split(","):
                    condition.strip()
                    if condition.startswith("nobody"):
                        node = condition[8:-1] # "nobody(X)" ---> node = "X"
                        if node in state.kiwis or node in state.dogs:
                            valid = False
                    elif condition.startswith("somebody"):
                        node = condition[9:-1]
                        if node not in state.kiwis and node not in state.dogs:
                            valid = False
            if valid:
                valid_pos.append((destination, cost))

        return valid_pos
    
    """
    Given a source and destination nodes, this method searchs the cost of the
    movement between them
    """
    def get_move_cost(self, source, destination):
        return self.graph.get((source, destination), (None, ""))[0]



    ###############
    #   ACTIONS   #
    ###############

    @action(
        # Kiwis range
        DDRange(0, 'num_kiwis'),
        
        # Dynamic Categorical ---> Accessible nodes from source node (appends the accessible nodes to a list)
        Categorical(["A", "B", "C", "D", "F", "G"]),
        
        # Dynamic cost
        cost = 0
    )
    def move_kiwi(self, state, kiwi_id, destination):
        current_pos = state.kiwis[kiwi_id]
        valid_moves = [dst for (dst, _) in self.get_valid_moves(current_pos, state)]
        if destination not in valid_moves:
            return None

        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_id] = destination
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)
    
    @action(
        # Dogs range
        DDRange(0, 'num_dogs'),

        # Dynamic Categorical ---> Accessible nodes from source node (appends the accessible nodes to a list)
        Categorical(["A", "B", "C", "D", "F", "G"]),

        # Dynamic cost
        cost = 0
    )
    def move_dog(self, state, dog_id, destination):
        current_pos = state.dogs[dog_id]
        valid_moves = [dst for (dst, _) in self.get_valid_moves(current_pos, state)]
        if destination not in valid_moves:
            return None

        new_dogs = list(state.dogs)
        new_dogs[dog_id] = destination
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))
