from typing import List

import networkx as nx
from networkx import Graph
from precice_config_graph.nodes import ParticipantNode

from preciceconfigchecker.rule import Rule
from preciceconfigchecker.severity import Severity
from preciceconfigchecker.violation import Violation


class DisjointSimulationsRule(Rule):
    severity = Severity.WARNING
    name = "Couplings must not be disjoint"

    class DisjointSimulationsViolation(Violation):
        participant_sets: frozenset[frozenset[str]]

        def __init__(self, participant_sets: frozenset[frozenset[str]]):
            super()
            assert (len(participant_sets) > 1)
            self.participant_sets = participant_sets

        def format_explanation(self) -> str:
            if len(self.participant_sets) == 2:
                [participants_a, participants_b] = list(self.participant_sets)
                return f"There are multiple simulations that do not interact with each other, as participants {list(participants_a)} do not communicate with participants {list(participants_b)}."
            else:
                return f"There are multiple simulations that do not interact with each other. Disjoint groups: {list(self.participant_sets)}."

        def format_possible_solutions(self) -> List[str]:
            return [
                "Consider splitting up the simulation into multiple configurations to improve maintainability of each simulation.",
                "Add some data to be exchanged between these simulations.",
            ]

    def check(self, graph: Graph) -> list[Violation]:
        def is_participant(node: ParticipantNode) -> bool:
            return isinstance(node, ParticipantNode)

        def has_participant(component) -> bool:
            return any(is_participant(node) for node in component)

        components_with_participant = list(filter(has_participant, nx.connected_components(graph)))

        if len(components_with_participant) > 1:
            participant_sets = frozenset([
                frozenset([participant.name for participant in filter(is_participant, component)])
                for component in components_with_participant
            ])

            return [self.DisjointSimulationsViolation(participant_sets)]
        else:
            return []
