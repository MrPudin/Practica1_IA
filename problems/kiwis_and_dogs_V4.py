from dataclasses import dataclass

from hlogedu.search.problem import Problem, action, Categorical, DDRange


@dataclass(frozen=True, order=True)
class State:
    kiwis: tuple[str]
    dogs: tuple[str]


class KiwisAndDogsProblem(Problem):
    NAME = "kiwis-and-dogsV4"

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
        # We start with ---> 2 KIWIS, one on node D and another on node F
        #               ---> 1 DOG on node C
        return [State(kiwis=("D", "F"), dogs=("C",))]

    def is_goal_state(self, state):
        # Are all KIWIS in the TREE node and all DOGS in the BONE node?
        return all(pos == "A" for pos in state.kiwis) and all(pos == "E" for pos in state.dogs)

    def is_valid_state(self, _):
        # There's no restrictions about the amount of animals in a single node
        return True

    ###############
    #  AUX FUNC   #
    ###############

    """ 
    Given a state and a current position, this method returns a list containing
    touples of the possible destinations and the associated cost of the
    specific movement between current and destination position
    """

    def get_valid_moves(self, current_pos, state):
        valid_pos = []
        # We search on the graph the possible destinations we can go to from source
        for (source, destination), (cost, conditions) in self.graph.items():
            if source != current_pos:
                # We don't take movements were source != current position
                continue

            # We filter the possible movements according to the conditions of some of them
            valid = True
            if conditions:
                for condition in conditions.split(","):
                    condition = condition.strip()
                    if condition.startswith("nobody"):
                        node = condition[8:-1] # node = X where nobody(X)
                        if node in state.kiwis or node in state.dogs:
                            # Somebody is the node ---> movement NOT VALID
                            valid = False
                    elif condition.startswith("somebody"):
                        node = condition[9:-1] # node = X where somebody(X)
                        if node not in state.kiwis and node not in state.dogs:
                            # There's no one in the node ---> movement NOT VALID
                            valid = False
            if valid:
                # We take the valid movements
                valid_pos.append((destination, cost))
        return valid_pos

    ###############
    #   ACTIONS   #
    ###############

    """
    The implementation of moving a kiwi action
    !!! We need a dynamic cost because it depends on the source and destination parameters !!!
        ---> Solution : return the cost of the action and the result state
    """

    @action(
        DDRange(0, 'num_kiwis'),
        Categorical(["A", "B", "C", "D", "E", "F", "G"])
    )
    def move_kiwi(self, state, kiwi_id, destination):
        # Get current position  and the possible destinations
        current_pos = state.kiwis[kiwi_id]
        valid_moves = self.get_valid_moves(current_pos, state)

        # If destination is accessible from current position ---> YES : get the cost of the operation and continue
        #                                                    ---> NO  : Return None
        move_cost = None
        for dst, cost in valid_moves:
            if dst == destination:
                move_cost = cost
                break

        if move_cost is None:
            return None

        # Set the new position of the kiwi we wanted to move and return ---> cost of the operation + the result state
        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_id] = destination
        new_state = State(kiwis=tuple(new_kiwis), dogs=state.dogs)

        return move_cost, new_state
    
    """
    The implementation of moving a dog action
    !!! We need a dynamic cost because it depends on the source and destination parameters !!!
        ---> Solution : return the cost of the action and the result state
    """

    @action(
        DDRange(0, 'num_dogs'),
        Categorical(["A", "B", "C", "D", "E", "F", "G"])
    )
    def move_dog(self, state, dog_id, destination):
        # Get current position  and the possible destinations
        current_pos = state.dogs[dog_id]
        valid_moves = self.get_valid_moves(current_pos, state)

        # If destination is accessible from current position ---> YES : get the cost of the operation and continue
        #                                                    ---> NO  : Return None
        move_cost = None
        for dst, cost in valid_moves:
            if dst == destination:
                move_cost = cost
                break

        if move_cost is None:
            return None

        # Set the new position of the dog we wanted to move and return ---> cost of the operation + the result state
        new_dogs = list(state.dogs)
        new_dogs[dog_id] = destination
        new_state = State(kiwis=state.kiwis, dogs=tuple(new_dogs))

        return move_cost, new_state
