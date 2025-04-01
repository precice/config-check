from typing import List

from networkx.classes import Graph
from precice_config_graph.nodes import ParticipantNode, MeshNode, MappingNode, Direction, MappingConstraint, \
    MappingType, CouplingSchemeNode, MultiCouplingSchemeNode

from preciceconfigchecker.rule import Rule
from preciceconfigchecker.severity import Severity
from preciceconfigchecker.violation import Violation


class MappingRule(Rule):
    name = "Mapping rules."
    severity = Severity.ERROR

    class JustInTimeMappingTypeViolation(Violation):
        """
            This class handles the just-in-time mapping being of the wrong type,
            i.e., not of one of the following types:
            nearest-neighbor, rbf-pum-direct and rbf.
        """

        def __init__(self, participant: ParticipantNode, mesh: MeshNode, direction: Direction, type: MappingType):
            self.participant = participant
            self.mesh = mesh
            self.direction = direction
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"
            self.type = type

        def format_explanation(self) -> str:
            out: str = (f"The just-in-time mapping of participant {self.participant.name} {self.connecting_word} mesh "
                        f"{self.mesh.name} is of type {self.type.value} and is invalid.")
            out += (
                "\n     Currently, only just-in-time mappings of the types \"nearest-neighbor\", \"rbf-pum-direct\" and "
                "\"rbf\" are supported.")
            return out

        def format_possible_solutions(self) -> list[str]:
            return [f"Please change the type of the mapping from {self.type.value} to one of the types "
                    f"\"nearest-neighbor\", \"rbf-pum-direct\" and \"rbf\"."]

    class JustInTimeMappingDirectionConstraintViolation(Violation):
        """
            This class handles a just-in-time mapping being of the wrong form,
            i.e., neither of the form read-consistent nor write-conservative.
        """

        def __init__(self, participant: ParticipantNode, mesh: MeshNode, direction: Direction,
                     constraint: MappingConstraint):
            self.participant = participant
            self.mesh = mesh
            self.direction = direction
            self.connecting_word: str = ""
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"
            self.constraint = constraint

        def format_explanation(self) -> str:
            out: str = (f"The just-in-time mapping of participant {self.participant.name} {self.connecting_word} mesh "
                        f"{self.mesh.name} has direction=\"{self.direction.value}\" and has constraint=\""
                        f"{self.constraint.value}\" and is invalid.")
            out += (
                "\n     Currently, only just-in-time mappings of the form read-consistent and write-conservative are "
                "supported.")
            return out

        def format_possible_solutions(self) -> list[str]:
            out: list[str] = []
            # One parameter is correct
            if self.direction == Direction.READ and self.constraint == MappingConstraint.CONSERVATIVE:
                out += [
                    f"Consider changing either the direction of the mapping to direction=\"write\" or the constraint"
                    f"of the mapping to constraint=\"consistent\"."]
            # One parameter is correct
            elif self.direction == Direction.WRITE and self.constraint == MappingConstraint.CONSISTENT:
                out += [
                    f"Consider changing either the direction of the mapping to direction=\"read\" or the constraint "
                    f"of the mapping to constraint=\"conservative\"."]
            # Both parameters are incorrect
            else:
                out += ["Please change the direction of the mapping to direction=\"write\" and the constraint of the "
                        "mapping to constraint=\"conservative\" or change the direction of the mapping to direction="
                        "\"read\" and the constraint of the mapping to constraint=\"consistent\"."]
            return out

    class JustInTimeMappingViolation(Violation):
        """
            This violation handles a mapping being of type "just-in-time", while the participant specifying the mapping
            does not have access to the corresponding mesh, i.e., he does not have "api-access" to the mesh.
        """

        def __init__(self, participant: ParticipantNode, mesh: MeshNode, direction: Direction):
            self.participant = participant
            self.mesh = mesh
            self.direction = direction
            self.connecting_word: str = ""
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"

        def format_explanation(self) -> str:
            return (f"The participant {self.participant.name} is specifying a just-in-time {self.direction.value}-"
                    f"mapping {self.connecting_word} mesh {self.mesh.name}, but does not have access to it.")

        def format_possible_solutions(self) -> list[str]:
            return [f"Let participant {self.participant.name} receive mesh {self.mesh.name} with the attribute "
                    f"api-access=\"true\".",
                    f"Map the values from mesh {self.mesh.name} to a mesh by participant {self.participant.name}, before"
                    f" {self.direction.value}ing it.",
                    "Otherwise, please remove it to improve readability."]

    class ParallelParticipantsMappingViolation(Violation):
        """
            This class handles participant, which run in parallel, having a wrong form of mapping,
            i.e., are not of the form read-consistent or write-conservative.
        """

        def __init__(self, participant_parent: ParticipantNode, participant_stranger: ParticipantNode,
                     mesh_parent: MeshNode, mesh_stranger, direction: Direction, constraint: MappingConstraint):
            self.participant_parent = participant_parent
            self.participant_stranger = participant_stranger
            self.mesh_parent = mesh_parent
            self.mesh_stranger = mesh_stranger
            self.direction = direction
            if self.direction == Direction.READ:
                # X reads "from" Y
                self.connecting_word = "from"
                self.inverse_connector = "to"
                self.inverse_direction = Direction.WRITE
            elif self.direction == Direction.WRITE:
                # X writes "to" Y
                self.connecting_word = "to"
                self.inverse_connector = "from"
                self.inverse_direction = Direction.READ
            self.constraint = constraint

        def format_explanation(self) -> str:
            out: str = (f"The participants {self.participant_parent.name} and "
                        f"{self.participant_stranger.name} are executing in parallel.")
            out += (f"\n     Their {self.direction.value}-mapping on meshes {self.mesh_parent.name} and {self.mesh_stranger.name} "
                    f"with constraint=\"{self.constraint.value}\" is is invalid.")
            out += (
                "\n     For parallel participants, only mappings of the form read-consistent and write-conservative are "
                "allowed.")
            return out

        def format_possible_solutions(self) -> list[str]:
            out: list[str] = []
            # One parameter is correct
            if self.direction == Direction.READ and self.constraint == MappingConstraint.CONSERVATIVE:
                out += [
                    f"Consider changing either the direction of the mapping to direction=\"write\" or the constraint"
                    f"of the mapping to constraint=\"consistent\"."]
                out += [f"If you change its direction to direction=\"write\", you need to move"
                        f" the mapping from {self.participant_parent.name} to {self.participant_stranger.name} and "
                        f"update the exchange=\"...\" tags in their coupling scheme."]
            # One parameter is correct
            elif self.direction == Direction.WRITE and self.constraint == MappingConstraint.CONSISTENT:
                out += [f"Consider changing either the direction of the mapping to direction=\"read\" or the constraint"
                        f" of the mapping to constraint=\"conservative\"."]
                out += [f"If you change its direction to direction=\"read\", you need to move"
                        f" the mapping from {self.participant_parent.name} to {self.participant_stranger.name} and "
                        f"update the exchange=\"...\" tags in their coupling scheme."]
            # Both parameters are incorrect
            else:
                out += ["Please change the direction of the mapping to direction=\"write\" and the constraint of the "
                        "mapping to constraint=\"conservative\" or change the direction of the mapping to direction="
                        "\"read\" and the constraint of the mapping to constraint=\"consistent\"."]
                out += [f"Please also check that data between {self.participant_parent.name} and "
                        f"{self.participant_stranger.name} gets exchanged correctly in their coupling scheme."]
            return out

    class MappingDirectionViolation(Violation):

        def __init__(self, participant_parent: ParticipantNode, participant_stranger: ParticipantNode,
                     mesh_parent: MeshNode, mesh_stranger: MeshNode, direction: Direction):
            self.participant_parent = participant_parent
            self.participant_stranger = participant_stranger
            self.mesh_parent = mesh_parent
            self.mesh_stranger = mesh_stranger
            self.direction = direction
            if self.direction == Direction.READ:
                # X reads "from" Y
                self.connecting_word = "from"
                self.inverse_connector = "to"
                self.inverse_direction = Direction.WRITE
            elif self.direction == Direction.WRITE:
                # X writes "to" Y
                self.connecting_word = "to"
                self.inverse_connector = "from"
                self.inverse_direction = Direction.READ

        def format_explanation(self) -> str:
            out: str = (f"The {self.direction.value}-mapping of participant {self.participant_parent.name} and mesh "
                        f"{self.mesh_parent.name} {self.connecting_word} participant {self.participant_stranger.name} and "
                        f"mesh {self.mesh_stranger.name} is in the wrong direction.")
            out += (f"\n     In {self.direction.value}-mappings, the {self.inverse_connector}=\"mesh\" has to be on a "
                    f"mesh that the participant provides.")
            return out

        def format_possible_solutions(self) -> list[str]:
            sol: list[str] = []
            if self.direction == Direction.WRITE:
                sol += [f"Either change direction=\"write\" to direction=\"read\", or swap meshes "
                        f"{self.mesh_parent.name} and {self.mesh_stranger.name}."]
            elif self.direction == Direction.READ:
                sol += [f"Either change direction=\"read\" to direction=\"write\", or swap meshes "
                        f"{self.mesh_parent.name} and {self.mesh_stranger.name}."]
            sol += [f"Move the mapping from participant {self.participant_parent.name} to participant "
                    f"{self.participant_stranger.name} and change its direction."]
            sol += ["Otherwise, please remove it to improve readability."]
            return sol

    def check(self, graph: Graph) -> list[Violation]:
        violations: list[Violation] = []

        mappings: list[MappingNode] = filter_mapping_nodes(graph)
        parallel_couplings: list[CouplingSchemeNode | MultiCouplingSchemeNode] = filter_parallel_coupling_nodes(graph)

        for mapping in mappings:

            # Only consider just-in-time mappings here
            if mapping.just_in_time:
                type: MappingType = mapping.type
                direction: Direction = mapping.direction

                # JIT mappings are missing either 'to' or 'from' attributes
                mesh: MeshNode = None
                # Find out which
                if mapping.from_mesh:
                    mesh = mapping.from_mesh
                elif mapping.to_mesh:
                    mesh = mapping.to_mesh

                # Only the types nearest-neighbor, rbf-pum-direct and rbf are supported
                supported_types = [MappingType.NEAREST_NEIGHBOR, MappingType.RBF_PUM_DIRECT, MappingType.RBF]
                if type not in supported_types:
                    violations.append(
                        self.JustInTimeMappingTypeViolation(mapping.parent_participant, mesh, direction, type))

                constraint: MappingConstraint = mapping.constraint

                if direction == Direction.WRITE and constraint == MappingConstraint.CONSERVATIVE:
                    # This is fine
                    pass
                elif direction == Direction.READ and constraint == MappingConstraint.CONSISTENT:
                    # This is fine
                    pass
                else:
                    # This is not fine anymore 😡
                    violations.append(
                        self.JustInTimeMappingDirectionConstraintViolation(mapping.parent_participant, mesh, direction,
                                                                           constraint))

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
                constraint: MappingConstraint = mapping.constraint
                # Get participants involved in mapping
                participant_parent: ParticipantNode = mapping.parent_participant
                if mapping.from_mesh in participant_parent.provide_meshes:
                    mesh_parent: MeshNode = mapping.from_mesh
                    mesh_stranger: MeshNode = mapping.to_mesh
                elif mapping.to_mesh in participant_parent.provide_meshes:
                    mesh_parent: MeshNode = mapping.to_mesh
                    mesh_stranger: MeshNode = mapping.from_mesh
                else:
                    # This should not happen if precice-tools --check ran.
                    pass

                participant_stranger: ParticipantNode = get_participant_of_mesh(graph, mesh_stranger)
                if direction == Direction.WRITE:
                    # If the direction is 'write', then the 'from' mesh needs to be provided by Parent
                    if mapping.from_mesh == mesh_parent:
                        # Everything is fine here
                        pass
                    elif mapping.to_mesh == mesh_parent:
                        # Parent is trying to write _to_ Strangers mesh
                        violations.append(self.MappingDirectionViolation(participant_parent, participant_stranger,
                                                                         mesh_parent, mesh_stranger, direction))
                    # For parallel participants, only a write-conservative mapping is allowed
                    if mapping.constraint != MappingConstraint.CONSERVATIVE:
                        for coupling_scheme in parallel_couplings:
                            if isinstance(coupling_scheme, CouplingSchemeNode):
                                # Find coupling-scheme corresponding to mapping
                                if ((coupling_scheme.first_participant == participant_parent and
                                     coupling_scheme.second_participant == participant_stranger) or
                                        (coupling_scheme.first_participant == participant_stranger and
                                         coupling_scheme.second_participant == participant_stranger)):
                                    violations.append(self.ParallelParticipantsMappingViolation(participant_parent,
                                                                                                participant_stranger,
                                                                                                mesh_parent,
                                                                                                mesh_stranger,
                                                                                                direction, constraint))
                            elif isinstance(coupling_scheme, MultiCouplingSchemeNode):
                                # Find multi-coupling-scheme corresponding to mapping
                                if (participant_parent in coupling_scheme.participants and
                                        participant_stranger in coupling_scheme.participants):
                                    violations.append(self.ParallelParticipantsMappingViolation(participant_parent,
                                                                                                participant_stranger,
                                                                                                mesh_parent,
                                                                                                mesh_stranger,
                                                                                                direction, constraint))

                elif direction == Direction.READ:
                    # If the direction is 'read', then the 'to' mesh needs to be by Parent
                    if mapping.to_mesh == mesh_parent:
                        # Everything is fine here
                        pass
                    elif mapping.from_mesh == mesh_parent:
                        # Parent is trying to read _from_ Stranger
                        violations.append(self.MappingDirectionViolation(participant_parent, participant_stranger,
                                                                         mesh_parent, mesh_stranger, direction))
                    # For parallel participants, only a read-consistent mapping is allowed.
                    if mapping.constraint != MappingConstraint.CONSISTENT:
                        for coupling_scheme in parallel_couplings:
                            if isinstance(coupling_scheme, CouplingSchemeNode):
                                # Find coupling-scheme corresponding to mapping
                                if ((coupling_scheme.first_participant == participant_parent and
                                     coupling_scheme.second_participant == participant_stranger) or
                                        (coupling_scheme.first_participant == participant_stranger and
                                         coupling_scheme.second_participant == participant_stranger)):
                                    violations.append(self.ParallelParticipantsMappingViolation(participant_parent,
                                                                                                participant_stranger,
                                                                                                mesh_parent,
                                                                                                mesh_stranger,
                                                                                                direction, constraint))
                            elif isinstance(coupling_scheme, MultiCouplingSchemeNode):
                                # Find multi-coupling-scheme corresponding to mapping
                                if (participant_parent in coupling_scheme.participants and
                                        participant_stranger in coupling_scheme.participants):
                                    violations.append(self.ParallelParticipantsMappingViolation(participant_parent,
                                                                                                participant_stranger,
                                                                                                mesh_parent,
                                                                                                mesh_stranger,
                                                                                                direction, constraint))


        return violations


MappingRule()


def get_participant_of_mesh(graph: Graph, mesh: MeshNode) -> ParticipantNode:
    """
        This method returns the participant who owns the given mesh.
        :param graph: The graph of the preCICE config.
        :param mesh: The mesh of which the participant is needed.
        :return: The participant who owns the mesh.
    """
    participant: ParticipantNode = None
    for node in graph.nodes:
        if isinstance(node, ParticipantNode):
            if mesh in node.provide_meshes and participant is None:
                participant = node
            elif mesh in node.provide_meshes and participant is not None:
                # TODO: Error here? A mesh should not be provided by more than one participant
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


def filter_parallel_coupling_nodes(graph: Graph) -> list[CouplingSchemeNode | MultiCouplingSchemeNode]:
    """
        This function returns all parallel coupling-scheme nodes of the given graph.
        :param graph:The graph to check.
        :return: All mapping nodes of the graph, which are either of type multi or ...-parallel.
    """
    couplings: list[CouplingSchemeNode | MultiCouplingSchemeNode] = []
    for node in graph.nodes:
        if isinstance(node, CouplingSchemeNode) or isinstance(node, MultiCouplingSchemeNode):
            couplings.append(node)
    return couplings
