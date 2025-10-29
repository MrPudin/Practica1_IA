from dataclasses import dataclass
from hlogedu.search.problem import Problem, action, Categorical, DDRange


@dataclass(frozen=True, order=True)
class State:
    kiwis: tuple[str]
    dogs: tuple[str]


class KiwisAndDogsProblemExample(Problem):
    NAME = "kiwis-and-dogs-example"

    def __init__(self):
        super().__init__()
        # Grafo con condiciones y costos
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
        kiwis_at_tree = all(pos == "A" for pos in state.kiwis)
        dogs_at_bones = all(pos == "E" for pos in state.dogs)
        return kiwis_at_tree and dogs_at_bones

    def is_valid_state(self, _):
        return True

    # -------------------------------------------------------------------------
    # Función auxiliar: calcula movimientos posibles y condiciones
    # -------------------------------------------------------------------------
    def _get_possible_moves(self, current_pos, state):
        possible = []
        for (src, dst), (cost, conds) in self.graph.items():
            if src != current_pos:
                continue

            # Comprobación de condiciones
            valid = True
            if conds:
                for cond in conds.split(","):
                    cond = cond.strip()
                    if cond.startswith("nobody("):
                        node = cond[8:-1]
                        if node in state.kiwis or node in state.dogs:
                            valid = False
                    elif cond.startswith("somebody("):
                        node = cond[9:-1]
                        if node not in state.kiwis and node not in state.dogs:
                            valid = False

            if valid:
                possible.append((dst, cost))
        return possible

    # -------------------------------------------------------------------------
    # Función auxiliar para costo dinámico
    # -------------------------------------------------------------------------
    def _get_move_cost(self, src, dst):
        """Devuelve el costo del movimiento src → dst"""
        return self.graph.get((src, dst), (None, ""))[0]

    # -------------------------------------------------------------------------
    # 🥝 Acción: mover kiwi con costo dinámico
    # -------------------------------------------------------------------------
    @action(DDRange(0, 'num_kiwis'), Categorical(["A", "B", "C", "D", "E", "F", "G"]),
            cost=lambda self, state, kiwi_idx, destination: self._get_move_cost(state.kiwis[kiwi_idx], destination))
    def move_kiwi(self, state, kiwi_idx, destination):
        current_pos = state.kiwis[kiwi_idx]
        valid_moves = [dst for (dst, _) in self._get_possible_moves(current_pos, state)]
        if destination not in valid_moves:
            return None

        new_kiwis = list(state.kiwis)
        new_kiwis[kiwi_idx] = destination
        return State(kiwis=tuple(new_kiwis), dogs=state.dogs)

    # -------------------------------------------------------------------------
    # 🐶 Acción: mover perro con costo dinámico
    # -------------------------------------------------------------------------
    @action(DDRange(0, 'num_dogs'), Categorical(["A", "B", "C", "D", "E", "F", "G"]),
            cost=lambda self, state, dog_idx, destination: self._get_move_cost(state.dogs[dog_idx], destination))
    def move_dog(self, state, dog_idx, destination):
        current_pos = state.dogs[dog_idx]
        valid_moves = [dst for (dst, _) in self._get_possible_moves(current_pos, state)]
        if destination not in valid_moves:
            return None

        new_dogs = list(state.dogs)
        new_dogs[dog_idx] = destination
        return State(kiwis=state.kiwis, dogs=tuple(new_dogs))

