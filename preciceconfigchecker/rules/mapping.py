from typing import List

from networkx.classes import Graph
from precice_config_graph.nodes import ParticipantNode, MeshNode, MappingNode

from preciceconfigchecker.rule import Rule
from preciceconfigchecker.severity import Severity
from preciceconfigchecker.violation import Violation


class MappingRule(Rule):
    name = "Mapping rules."
    severity = Severity.ERROR

    class JustInTimeMappingViolation(Violation):
        """
            This violation handles a mapping being of type "just-in-time", while the participant specifying the mapping
            does not have access to the corresponding mesh, i.e., he does not have "api-access" to the mesh.
        """

        def __init__(self, participant: ParticipantNode, mesh: MeshNode, direction: str):
            self.participant = participant
            self.mesh = mesh
            self.direction = direction

        def format_explanation(self) -> str:
            return (
                f"The participant {self.participant.name} is specifying a just-in-time mapping {self.direction} mesh "
                f"{self.mesh.name}, but does not have access to it.")

        def format_possible_solutions(self) -> list[str]:
            return [f"Let participant {self.participant.name} receive mesh {self.mesh.name} with the attribute "
                    f"\"api-access=true\".",
                    f"Map the values from mesh {self.mesh.name} to a mesh by participant {self.participant.name}, before"
                    f" reading or writing it",
                    "Otherwise, please remove it to improve readability."]

    def check(self, graph: Graph) -> list[Violation]:
        violations: list[Violation] = []

        mappings: list[MappingNode] = filter_mapping_nodes(graph)
        for mapping in mappings:

            # Only consider just-in-time mappings here
            if mapping.just_in_time:
                # JIT mappings are missing either "to" or "from" attributes
                direction: str = ""
                mesh: MeshNode = None
                # Find out which
                if mapping.from_mesh:
                    direction = "from"
                    mesh = mapping.from_mesh
                elif mapping.to_mesh:
                    direction = "to"
                    mesh = mapping.to_mesh

                # Check if participant receives mesh with api-access true
                receive_meshes = mapping.parent_participant.receive_meshes
                for receive_mesh in receive_meshes:
                    if receive_mesh.mesh == mesh:
                        # If api-access != true, then participant does not have permission to read/write from/to it
                        if not receive_mesh.api_access:
                            violations.append(
                                self.JustInTimeMappingViolation(mapping.parent_participant, mesh, direction))
        return violations

MappingRule()


def filter_mapping_nodes(graph: Graph) -> list[MappingNode]:
    """
        This function returns all mapping nodes of the given graph.
        :param graph:The graph to check.
        :return: All mapping nodes of the graph.
    """
    mappings: list[MappingNode] = []
    for node in graph.nodes:
        if isinstance(node, MappingNode):
            mappings.append(node)
    return mappings
