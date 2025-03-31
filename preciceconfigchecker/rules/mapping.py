from typing import List

from networkx.classes import Graph
from precice_config_graph.nodes import ParticipantNode, MeshNode, MappingNode, Direction

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
                    f"api-access=\"true\".",
                    f"Map the values from mesh {self.mesh.name} to a mesh by participant {self.participant.name}, before"
                    f" reading or writing it",
                    "Otherwise, please remove it to improve readability."]

    class MappingDirectionViolation(Violation):
        name = "Mapping direction."

        def __init__(self, participant_parent: ParticipantNode, participant_stranger: ParticipantNode,
                     mesh_parent: MeshNode, mesh_stranger: MeshNode, direction: str):
            self.participant_parent = participant_parent
            self.participant_stranger = participant_stranger
            self.mesh_parent = mesh_parent
            self.mesh_stranger = mesh_stranger
            self.direction = direction

        def format_explanation(self) -> str:
            return (f"The mapping of participant {self.participant_parent.name} and mesh {self.mesh_parent.name} "
                    f"{self.direction} {self.participant_stranger.name} and mesh {self.mesh_stranger.name} is in "
                    f"the wrong direction.")

        def format_possible_solutions(self) -> list[str]:
            sol: list[str] = [f"Please change the direction of the mapping between participant "
                              f"{self.participant_parent.name} and {self.participant_stranger.name}."]
            # 'to' corresponds to a 'write' mapping
            if self.direction == "to":
                sol += [f"Either change direction=\"write\" to direction=\"read\", or swap meshes "
                        f"{self.mesh_parent.name} and {self.mesh_stranger.name}."]
            # 'from' corresponds to a 'read' mapping
            elif self.direction == "from":
                sol += [f"Either change direction=\"read\" to direction=\"write\", or swap meshes "
                        f"{self.mesh_parent.name} and {self.mesh_stranger.name}."]
            sol += ["Otherwise, please remove it to improve readability."]
            return sol

    def check(self, graph: Graph) -> list[Violation]:
        violations: list[Violation] = []

        mappings: list[MappingNode] = filter_mapping_nodes(graph)
        for mapping in mappings:

            # Only consider just-in-time mappings here
            if mapping.just_in_time:
                # JIT mappings are missing either 'to' or 'from' attributes
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

            # 'just-in-time' mappings have already been handled
            elif not mapping.just_in_time:
                direction: Direction = mapping.direction
                # Get participants involved in mapping
                participant_parent: ParticipantNode = mapping.parent_participant
                if mapping.from_mesh in participant_parent.provide_meshes:
                    mesh_parent: MeshNode = mapping.from_mesh
                    mesh_stranger = mapping.to_mesh
                else:
                    mesh_parent: MeshNode = mapping.to_mesh
                    mesh_stranger = mapping.from_mesh
                participant_stranger: ParticipantNode = get_participant_from_mesh(graph, mesh_stranger)
                # TODO: Error if stranger = parent? Mappings should probably not be on the same participant
                if direction == Direction.WRITE:
                    # If the direction is 'write', then the 'to' mesh needs to be provided by Parent
                    if mapping.to_mesh == mesh_parent:
                        # Everything is fine here
                        pass
                    elif mapping.from_mesh == mesh_parent:
                        # Parent is trying to write _to_ Strangers mesh
                        violations.append(self.MappingDirectionViolation(participant_parent, participant_stranger,
                                                                         mesh_parent, mesh_stranger, "to"))
                elif direction == Direction.READ:
                    # If the direction is 'read', then the 'from' mesh needs to be by Parent
                    if mapping.from_mesh == mesh_parent:
                        # Everything is fine here
                        pass
                    elif mapping.to_mesh == mesh_parent:
                        # Parent is trying to read _from_ Stranger
                        violations.append(self.MappingDirectionViolation(participant_parent, participant_stranger,
                                                                         mesh_parent, mesh_stranger, "from"))

        return violations


MappingRule()


def get_participant_from_mesh(graph: Graph, mesh: MeshNode) -> ParticipantNode:
    participant: ParticipantNode = None
    for node in graph.nodes:
        if isinstance(node, ParticipantNode):
            if mesh in node.provide_meshes and participant is None:
                participant = node
            elif mesh in node.provide_meshes and participant is not None:
                # TODO: Error here? a mesh should not be provided by more than one participant
                pass
    # TODO: Error if participant does not exist?
    return participant


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
