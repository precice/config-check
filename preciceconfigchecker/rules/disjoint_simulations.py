import networkx as nx
from networkx import Graph
from precice_config_graph.nodes import ParticipantNode

from preciceconfigchecker.rule import Rule
from preciceconfigchecker.severity import Severity
from preciceconfigchecker.violation import Violation

default_possible_solutions = [
    "Consider splitting up the simulation into multiple configurations to improve maintainability of each simulation.",
]


class DisjointSimulationsRule(Rule):
    severity = Severity.DEBUG
    name = "Couplings must not be disjoint"

    class CommonDisjointSimulationsViolation(Violation):
        participant_sets: frozenset[frozenset[str]]

        def __init__(self, participant_sets: frozenset[frozenset[str]]):
            super()
            assert(len(participant_sets) > 1)
            self.participant_sets = participant_sets

        def _format_explanation(self, details: str) -> str:
            explanation = f"There are {len(self.participant_sets)} simulations that do not interact with each other{details}. "

            def format_set(set: frozenset[str]) -> str:
                return ", ".join(sorted(set))

            if len(self.participant_sets) == 2:
                [participants_a, participants_b] = list(self.participant_sets)

                participants_a_label = "Participants" if len(participants_a) > 1 else "Participant"
                do_str = "do" if len(participants_a) > 1 else "does"
                participants_b_label = "participants" if len(participants_b) > 1 else "participant"

                explanation += f"{participants_a_label} {format_set(participants_a)} {do_str} not communicate with {participants_b_label} {format_set(participants_b)}."
            else:
                explanation += f"Disjoint groups:"
                for component in self.participant_sets:
                    explanation += f"\n- {format_set(component)}"

            return explanation

    class FullyDisjointSimulationsViolation(CommonDisjointSimulationsViolation):
        def __init__(self, participant_sets: frozenset[frozenset[str]]):
            super().__init__(participant_sets)

        def format_explanation(self) -> str:
            return self._format_explanation("")

        def format_possible_solutions(self) -> list[str]:
            return default_possible_solutions + [
                "Add some data to be exchanged between these simulations.",
            ]

    class SharedDataDisjointSimulationsViolation(CommonDisjointSimulationsViolation):
        shared_data_name: str

        def __init__(self, participant_sets: frozenset[frozenset[str]], shared_data_name: str):
            super().__init__(participant_sets)
            self.shared_data_name = shared_data_name

        def format_explanation(self) -> str:
            return self._format_explanation(f", but share data {self.shared_data_name}")

        def format_possible_solutions(self) -> list[str]:
            return default_possible_solutions + [
                "Exchange the data between these simulations.",
            ]

    def check(self, graph: Graph) -> list[Violation]:
        def is_participant(node) -> bool:
            return isinstance(node, ParticipantNode)

        def has_participant(component) -> bool:
            return any(is_participant(node) for node in component)

        components_with_participant = list(filter(has_participant, nx.connected_components(graph)))

        if len(components_with_participant) > 1:
            participant_sets = frozenset([
                frozenset([participant.name for participant in filter(is_participant, component)])
                for component in components_with_participant
            ])

            return [self.FullyDisjointSimulationsViolation(participant_sets)]
        else:
            return []
