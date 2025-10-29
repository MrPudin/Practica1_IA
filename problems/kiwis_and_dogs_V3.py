from dataclasses import dataclass
from hlogedu.search.problem import Problem, action, Categorical, DDRange


@dataclass(frozen=True, order=True)
class State:
    kiwis: tuple[str]
    dogs: tuple[str]
    prev_kiwis: tuple[str]  # nodos anteriores de cada kiwi
    prev_dogs: tuple[str]   # nodos anteriores de cada perro


# Problem
##############################################################################


class KiwisAndDogsProblemV2(Problem):
    NAME = "kiwis-and-dogsV2"

    def __init__(self):
        super().__init__()
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

    def get_start_states(self):
        start_kiwis = ("D", "F")
        start_dogs = ("C",)
        # Inicializamos prev_kiwis y prev_dogs como None
        prev_kiwis = tuple(None for _ in start_kiwis)
        prev_dogs = tuple(None for _ in start_dogs)
        return [State(kiwis=start_kiwis, dogs=start_dogs,
                      prev_kiwis=prev_kiwis, prev_dogs=prev_dogs)]

    def is_goal_state(self, state):
        kiwis_at_tree = all(pos == "A" for pos in state.kiwis)
        dogs_at_bones = all(pos == "E" for pos in state.dogs)
        return kiwis_at_tree and dogs_at_bones

    def is_valid_state(self, _):
        return True

    ###############
    #  AUX FUNC   #
    ###############

    def get_valid_moves(self, current_pos, state, previous_pos=None):
        valid_pos = []
        for (source, destination), (cost, conditions) in self.graph.items():
            if source != current_pos:
                continue
            # Evitamos regresar al nodo anterior
            if previous_pos is not None and destination == previous_pos:
                continue

            valid = True
            if conditions:
                for condition in conditions.split(","):
                    condition.strip()
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

    def get_move_cost(self, source, destination):
        return self.graph.get((source, destination), (None, ""))[0]

    ###############
    #   ACTIONS   #
    ###############

    @action(
        DDRange(0, 'num_kiwis'),
        Categorical(["A", "B", "C", "D", "E", "F", "G"])
    )
    def move_kiwi(self, state, kiwi_id, destination):
        current_pos = state.kiwis[kiwi_id]
        prev_pos = state.prev_kiwis[kiwi_id]
        valid_moves = self.get_valid_moves(current_pos, state, previous_pos=prev_pos)

        move_cost = None
        for dst, cost in valid_moves:
            if dst == destination:
                move_cost = cost
                break
        if move_cost is None:
            return None

        # Actualizamos posiciones
        new_kiwis = list(state.kiwis)
        new_prev_kiwis = list(state.prev_kiwis)
        new_prev_kiwis[kiwi_id] = current_pos  # posición actual se vuelve anterior
        new_kiwis[kiwi_id] = destination

        new_state = State(
            kiwis=tuple(new_kiwis),
            dogs=state.dogs,
            prev_kiwis=tuple(new_prev_kiwis),
            prev_dogs=state.prev_dogs
        )
        return move_cost, new_state

    @action(
        DDRange(0, 'num_dogs'),
        Categorical(["A", "B", "C", "D", "E", "F", "G"])
    )
    def move_dog(self, state, dog_id, destination):
        current_pos = state.dogs[dog_id]
        prev_pos = state.prev_dogs[dog_id]
        valid_moves = self.get_valid_moves(current_pos, state, previous_pos=prev_pos)

        move_cost = None
        for dst, cost in valid_moves:
            if dst == destination:
                move_cost = cost
                break
        if move_cost is None:
            return None

        # Actualizamos posiciones
        new_dogs = list(state.dogs)
        new_prev_dogs = list(state.prev_dogs)
        new_prev_dogs[dog_id] = current_pos
        new_dogs[dog_id] = destination

        new_state = State(
            kiwis=state.kiwis,
            dogs=tuple(new_dogs),
            prev_kiwis=state.prev_kiwis,
            prev_dogs=tuple(new_prev_dogs)
        )
        return move_cost, new_state