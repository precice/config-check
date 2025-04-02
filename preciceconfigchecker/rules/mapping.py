from networkx.classes import Graph
from precice_config_graph.nodes import ParticipantNode, MeshNode, MappingNode, Direction, MappingConstraint, \
    MappingType, CouplingSchemeNode, MultiCouplingSchemeNode, CouplingSchemeType, ExchangeNode

from preciceconfigchecker.rule import Rule
from preciceconfigchecker.severity import Severity
from preciceconfigchecker.violation import Violation


class MappingRule(Rule):
    name = "Mapping rules."
    severity = Severity.ERROR

    class IncorrectExchangeMappingViolation(Violation):
        """
            This class handles two participants specifying a mapping between them, but only an incorrect exchange
            alongside it, i.e., no exchange on the mesh indicated by the mapping.
        """

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh: MeshNode, direction: Direction):
            self.parent = parent
            self.stranger = stranger
            self.mesh = mesh
            self.direction = direction
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"

        def format_explanation(self) -> str:
            out: str = (f"The participant {self.parent.name} is specifying a {self.direction.value}-mapping "
                        f"{self.connecting_word} participant {self.stranger.name}, but the exchange in the coupling-"
                        f"scheme between them is incorrect.")
            out += (
                f"\n     For a {self.direction.value}-mapping, the mesh {self.mesh.name} should be used to exchange "
                f"data and the participant specifying the {self.connecting_word}-mesh should be the "
                f"{self.connecting_word}-participant in the exchange.")
            return out

        def format_possible_solutions(self) -> list[str]:
            out: list[str] = []
            # In a 'read' mapping, the 'from' mesh is by Stranger => Stranger should be from-participant in exchange.
            if self.direction == Direction.READ:
                out += [f"Add an exchange from participant {self.stranger.name} to participant {self.parent.name}, "
                        f"which uses participant {self.stranger.name}'s mesh {self.mesh.name} to the coupling-scheme "
                        f"between them."]
            # In a 'write' mapping, the 'to' mesh is by Stranger => Stranger should be to-participant in exchange.
            elif self.direction == Direction.WRITE:
                out += [f"Add an exchange from participant {self.parent.name} to participant {self.stranger.name}, "
                        f"which uses participant {self.stranger.name}'s mesh {self.mesh.name}, to the coupling-scheme "
                        f"between them."]
            return out

    class MissingExchangeMappingViolation(Violation):
        """
            This class handles two participants specifying a mapping between them, but no exchange alongside it,
            i.e., no exchange between the two.
        """

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh: MeshNode, direction: Direction):
            self.parent = parent
            self.stranger = stranger
            self.mesh = mesh
            self.direction = direction
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"

        def format_explanation(self) -> str:
            out: str = (f"The participant {self.parent.name} is specifying a {self.direction.value}-mapping "
                        f"{self.connecting_word} participant {self.stranger.name}, but there is no exchange for it in "
                        f"the coupling-scheme between them.")
            out += (f"     For a {self.direction.value}-mapping, the mesh {self.mesh.name} should be used to exchange "
                    f"data.")
            return out

        def format_possible_solutions(self) -> list[str]:
            out: list[str] = []
            # In a 'read' mapping, the 'from' mesh is by Stranger => Stranger should be from-participant in exchange.
            if self.direction == Direction.READ:
                out += [f"Add an exchange from participant {self.stranger.name} to participant {self.parent.name}, "
                        f"which uses participant {self.stranger.name}'s mesh {self.mesh.name} to the coupling-scheme "
                        f"between them."]
            # In a 'write' mapping, the 'to' mesh is by Stranger => Stranger should be to-participant in exchange.
            elif self.direction == Direction.WRITE:
                out += [f"Add an exchange from participant {self.parent.name} to participant {self.stranger.name}, "
                        f"which uses participant {self.stranger.name}'s mesh {self.mesh.name} to the coupling-scheme "
                        f"between them."]
            return out

    class MissingCouplingSchemeMappingViolation(Violation):
        """
            This class handles two participants specifying a mapping between them, but no coupling-scheme alongside it,
            i.e., no coupling-scheme exists between the two to exchange data.
        """

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh: MeshNode, direction: Direction):
            self.parent = parent
            self.stranger = stranger
            self.mesh = mesh
            self.direction = direction
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"

        def format_explanation(self) -> str:
            return (f"The participant {self.parent.name} is specifying a {self.direction.value}-mapping "
                    f"{self.connecting_word} participant {self.stranger.name}, but there does not exist a "
                    f"coupling-scheme between them.")

        def format_possible_solutions(self) -> list[str]:
            out: list[str] = []
            out += [f"Create a coupling scheme between participants {self.parent.name} and {self.stranger.name} with an"
                    f"exchange to exchange data between them."]
            out += ["Otherwise, please remove the mapping to improve readability."]
            return out

    class JustInTimeMappingPermissionViolation(Violation):
        """
            This class handles a participant (parent) specifying a just-in-time mapping with another participant
            (stranger), but the parent not having permission to read from/write to Stranger's mesh, i.e., Parent does
            not receive the mesh with api-access=true.
        """

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh: MeshNode, direction: Direction):
            self.parent = parent
            self.stranger = stranger
            self.mesh = mesh
            self.direction = direction
            self.connecting_word: str = ""
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"

        def format_explanation(self) -> str:
            return (f"The participant {self.parent.name} is specifying a just-in-time {self.direction.value}-"
                    f"mapping {self.connecting_word} participant {self.stranger.name}'s mesh {self.mesh.name}, but "
                    f"does not have access to it.")

        def format_possible_solutions(self) -> list[str]:
            return [f"Let participant {self.parent.name} receive mesh {self.mesh.name} from participant "
                    f"{self.stranger.name} with the attribute api-access=\"true\".",
                    f"Map the values from mesh {self.mesh.name} to a mesh by participant {self.parent.name}, before"
                    f" {self.direction.value}ing them.",
                    "Otherwise, please remove it to improve readability."]

    class ParallelCouplingMappingFormatViolation(Violation):
        """
            This class handles a mapping being specified by two participants which are running in parallel,
            i.e., they are both in the same parallel-coupling-scheme. For such participants, only the mapping
            formats read-consistent and write-conservative are allowed.
        """

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode,
                     mesh_parent: MeshNode, mesh_stranger, direction: Direction, constraint: MappingConstraint):
            self.parent = parent
            self.stranger = stranger
            self.mesh_parent = mesh_parent
            self.mesh_stranger = mesh_stranger
            self.direction = direction
            self.constraint = constraint

        def format_explanation(self) -> str:
            out: str = (f"The participants {self.parent.name} and "
                        f"{self.stranger.name} are executing in parallel.")
            out += (
                f"\n     Their {self.direction.value}-mapping on meshes {self.mesh_parent.name} and {self.mesh_stranger.name} "
                f"with constraint=\"{self.constraint.value}\" is is invalid.")
            out += (
                "\n     For parallel participants, only mappings of the form read-consistent and write-conservative are "
                "allowed.")
            return out

        def format_possible_solutions(self) -> list[str]:
            out: list[str] = []
            # Mapping format is "almost" correct
            # Mapping format is "almost" correct
            if self.direction == Direction.READ and self.constraint == MappingConstraint.CONSERVATIVE:
                out += [
                    f"Consider changing either the direction of the mapping between participants {self.parent.name} and "
                    f"{self.stranger.name} to direction=\"write\" or the constraint of the mapping to constraint="
                    f"\"consistent\"."]
                out += [f"The effect of a read-conservative mapping can be achieved by moving the mapping from "
                        f"participant {self.parent.name} to participant {self.stranger.name} and changing its direction "
                        f"to \"write\"."]
                out += [f"When moving the mapping, remember to update the <exchange .../> tag in the participants "
                        f"coupling-scheme."]
            elif self.direction == Direction.WRITE and self.constraint == MappingConstraint.CONSISTENT:
                out += [
                    f"Consider changing either the direction of the mapping between participants {self.parent.name} and "
                    f"{self.stranger.name} to direction=\"read\" or the constraint of the mapping to constraint="
                    f"\"conservative\"."]
                out += [f"The effect of a write-consistent mapping can be achieved by moving the mapping from "
                        f"participant {self.parent.name} to participant {self.stranger.name} and changing its direction "
                        f"to \"read\"."]
                out += [f"When moving the mapping, remember to update the <exchange .../> tag in the participants "
                        f"coupling-scheme."]
            # Generic answers for arbitrary constraints
            elif self.direction == Direction.READ:
                out += [f"Consider changing the constraint of the mapping between participants {self.parent.name} and "
                        f"{self.stranger.name} from \"{self.constraint.value}\" to \"consistent\"."]
            elif self.direction == Direction.WRITE:
                out += [f"Consider changing the constraint of the mapping between participants {self.parent.name} and "
                        f"{self.stranger.name} from \"{self.constraint.value}\" to \"conservative\"."]
            return out

    class MappingDirectionViolation(Violation):
        """
            This class handles a mapping being specified by two participants, but the to- and from-meshes not being
            according to the specified mapping direction.
        """

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode,
                     mesh_parent: MeshNode, mesh_stranger: MeshNode, direction: Direction):
            self.parent = parent
            self.stranger = stranger
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
            out: str = (f"The {self.direction.value}-mapping of participant {self.parent.name} and mesh "
                        f"{self.mesh_parent.name} {self.connecting_word} participant {self.stranger.name} and "
                        f"mesh {self.mesh_stranger.name} is in the wrong direction.")
            out += (f"\n     In {self.direction.value}-mappings, the {self.inverse_connector}=\"mesh\" has to be on a "
                    f"mesh that the participant provides.")
            return out

        def format_possible_solutions(self) -> list[str]:
            sol: list[str] = []
            sol += [
                f"Either change direction=\"{self.direction.value}\" to direction=\"{self.inverse_direction.value}\""
                f", or swap meshes {self.mesh_parent.name} and {self.mesh_stranger.name}."]
            sol += [f"Move the mapping from participant {self.parent.name} to participant "
                    f"{self.stranger.name}, change its direction and remember to switch the mesh used in the "
                    f"<exchange .../> tag in their coupling scheme."]
            sol += ["Otherwise, please remove it to improve readability."]
            return sol

    class JustInTimeMappingFormatViolation(Violation):
        """
            This class handles a just-in-time mapping being specified between two participants. For such mappings,
            only the formats read-consistent and write-conservative are allowed.
        """

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh: MeshNode,
                     direction: Direction,
                     constraint: MappingConstraint):
            self.parent = parent
            self.stranger = stranger
            self.mesh = mesh
            self.direction = direction
            self.connecting_word: str = ""
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"
            self.constraint = constraint

        def format_explanation(self) -> str:
            out: str = (
                f"The just-in-time {self.direction.value}-mapping of participant {self.parent.name} {self.connecting_word} "
                f"participant {self.stranger.name}'s mesh {self.mesh.name} is in direction="
                f"\"{self.direction.value}\" and has constraint=\"{self.constraint.value}\", which is invalid.")
            out += (
                "\n     Currently, only just-in-time mappings of the form read-consistent and write-conservative are "
                "supported.")
            return out

        def format_possible_solutions(self) -> list[str]:
            out: list[str] = []
            # Mapping format is "almost" correct
            if self.direction == Direction.READ and self.constraint == MappingConstraint.CONSERVATIVE:
                out += [
                    f"Consider changing either the direction of the mapping between participants {self.parent.name} and "
                    f"{self.stranger.name} to direction=\"write\" or the constraint of the mapping to constraint="
                    f"\"consistent\"."]
                out += [f"The effect of a read-conservative mapping can be achieved by moving the mapping from "
                        f"participant {self.parent.name} to participant {self.stranger.name} and changing its direction "
                        f"to \"write\"."]
                out += [f"When moving the mapping, remember to update the <exchange .../> tag in the participants "
                        f"coupling-scheme."]
            elif self.direction == Direction.WRITE and self.constraint == MappingConstraint.CONSISTENT:
                out += [
                    f"Consider changing either the direction of the mapping between participants {self.parent.name} and "
                    f"{self.stranger.name} to direction=\"read\" or the constraint of the mapping to constraint="
                    f"\"conservative\"."]
                out += [f"The effect of a write-consistent mapping can be achieved by moving the mapping from "
                        f"participant {self.parent.name} to participant {self.stranger.name} and changing its direction "
                        f"to \"read\"."]
                out += [f"When moving the mapping, remember to update the <exchange .../> tag in the participants "
                        f"coupling-scheme."]
            # Generic answers for arbitrary constraints
            elif self.direction == Direction.READ:
                out += [f"Consider changing the constraint of the mapping between participants {self.parent.name} and "
                        f"{self.stranger.name} from \"{self.constraint.value}\" to \"consistent\"."]
            elif self.direction == Direction.WRITE:
                out += [f"Consider changing the constraint of the mapping between participants {self.parent.name} and "
                        f"{self.stranger.name} from \"{self.constraint.value}\" to \"conservative\"."]
            return out

    class JustInTimeMappingDirectionViolation(Violation):
        """
            This class handles a just-in-time mapping being specified between two participants, but the to- or from-mesh
            not being according to the specified mapping direction.
        """

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh: MeshNode, direction: Direction):
            self.parent = parent
            self.stranger = stranger
            self.mesh = mesh
            self.direction = direction
            if self.direction == Direction.READ:
                # X reads "from" Y
                self.connecting_word = "from"
                self.inverse_direction = Direction.WRITE
            elif self.direction == Direction.WRITE:
                # X writes "to" Y
                self.connecting_word = "to"
                self.inverse_direction = Direction.READ

        def format_explanation(self) -> str:
            out: str = (f"The {self.direction.value}-mapping of participant {self.parent.name} "
                        f"{self.connecting_word} participant {self.stranger.name} and "
                        f"mesh {self.mesh.name} is in the wrong direction.")
            out += (
                f"\n     In just-in-time{self.direction.value}-mappings, the {self.connecting_word}=\"mesh\" has to "
                f"be on a stranger participants mesh.")
            return out

        def format_possible_solutions(self) -> list[str]:
            sol: list[str] = []
            sol += [f"Change direction=\"{self.direction.value}\" to direction=\"{self.inverse_direction.value}\"."]
            sol += [f"Move the mapping from participant {self.parent.name} to participant "
                    f"{self.stranger.name} and change its direction and remember to switch the mesh used in the "
                    f"<exchange .../> tag in their coupling scheme."]
            sol += ["Otherwise, please remove it to improve readability."]
            return sol

    class JustInTimeMappingFormatDirectionViolation(Violation):
        """
            This class handles a just-in-time mapping being specified between two participants, but the to- or from-mesh
            not being according to the specified mapping direction and the format not being either read-consistent or
            write-conservative.
        """

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh: MeshNode, direction: Direction,
                     constraint: MappingConstraint, type: MappingType):
            self.parent = parent
            self.stranger = stranger
            self.mesh = mesh
            self.direction = direction
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"
            self.constraint = constraint
            self.type = type

        def format_explanation(self) -> str:
            out: str = (f"The just-in-time-{self.direction.value}-mapping of type {self.type.value} with constraint "
                        f"{self.constraint.value} between participants {self.parent.name} and {self.stranger.name} is "
                        f"invalid.")
            out += (f"\n    Currently, only just-in-time mappings of the type \"nearest-neigbor\", \"rbf-pum-direct\" "
                    f"and \"rbf\" are supported.")
            out += (f"Additionally, only the formats \"write-conservative\" or \"read-consistent\" are implemented for "
                    f"just-in-time mappings.")

        def format_possible_solutions(self) -> list[str]:
            out: list[str] = []
            out += [f"Please update the type of the mapping between participants {self.parent.name} and "
                    f"{self.stranger.name} from {self.type.value} to one of \"nearest-neighbor\", \"rbf-pum-direct\" "
                    f"or \"rbf\"."]
            out += [f"Please update the format of the mapping between participants {self.parent.name} and "
                    f"{self.stranger.name} from {self.direction.value}-{self.constraint.value} to one of "
                    f"\"write-conservative\" or \"read-consistent\"."]

    class JustInTimeMappingTypeViolation(Violation):
        """
            This class handles a just-in-time mapping being specified between two participants, but its type is incorrect.
            Currently, for just-time-mappings, only the mapping-types nearest-neighbor, rbf-pum-direct and rbf are
            supported.
        """

        def __init__(self, parent: ParticipantNode, stranger: ParticipantNode, mesh: MeshNode, direction: Direction,
                     type: MappingType):
            self.parent = parent
            self.stranger = stranger
            self.mesh = mesh
            self.direction = direction
            if self.direction == Direction.READ:
                self.connecting_word = "from"
            elif self.direction == Direction.WRITE:
                self.connecting_word = "to"
            self.type = type

        def format_explanation(self) -> str:
            out: str = (
                f"The just-in-time {self.direction.value}-mapping of participant {self.parent.name} {self.connecting_word} "
                f"{self.stranger.name}'s mesh {self.mesh.name} is of type {self.type.value}, which is invalid.")
            out += (
                "\n     Currently, only just-in-time mappings of the types \"nearest-neighbor\", \"rbf-pum-direct\" and "
                "\"rbf\" are supported.")
            return out

        def format_possible_solutions(self) -> list[str]:
            return [f"Please change the type of the mapping from \"{self.type.value}\" to one of the types "
                    f"\"nearest-neighbor\", \"rbf-pum-direct\" or \"rbf\"."]

    def check(self, graph: Graph) -> list[Violation]:
        violations: list[Violation] = []

        couplings: list[CouplingSchemeNode | MultiCouplingSchemeNode] = filter_coupling_nodes(graph)
        parallel_couplings: list[CouplingSchemeNode | MultiCouplingSchemeNode] = filter_parallel_coupling_nodes(graph)

        mappings: list[MappingNode] = filter_mapping_nodes(graph)
        for mapping in mappings:
            type: MappingType = mapping.type
            direction: Direction = mapping.direction
            constraint: MappingConstraint = mapping.constraint
            participant_parent: ParticipantNode = mapping.parent_participant
            # Initialize to avoid keeping value for multiple iterations (mappings)
            mesh_parent: MeshNode = None
            mesh_stranger: MeshNode = None

            # Check only just-in-time (JIT) mappings here
            if mapping.just_in_time:
                # Either 'to' or 'from' tag does not exist
                if mapping.from_mesh and not mapping.to_mesh:
                    mesh_stranger = mapping.from_mesh
                elif not mapping.from_mesh and mapping.to_mesh:
                    mesh_stranger = mapping.to_mesh
                else:
                    # This case should not exist, if precice-tools --check ran.
                    pass
                participant_stranger = get_participant_of_mesh(graph, mesh_stranger)

                # Only the types nearest-neighbor, rbf-pum-direct and rbf are supported
                supported_types = [MappingType.NEAREST_NEIGHBOR, MappingType.RBF_PUM_DIRECT, MappingType.RBF]
                if type not in supported_types:
                    # DONE TODO: JIT wrong type Violation DONE
                    violations.append(
                        self.JustInTimeMappingTypeViolation(participant_parent, participant_stranger, mesh_stranger,
                                                            direction, type))

                # Only read-consistent and write-conservative are supported
                if direction == Direction.READ:
                    # For a read-mapping, the 'from' mesh needs to be defined
                    if mapping.from_mesh:
                        # Correct direction
                        # For a JIT-read-mapping, the constraint has to be consistent
                        if constraint == MappingConstraint.CONSISTENT:
                            # This is fine
                            pass
                        else:
                            # Correct direction, but wrong constraint
                            # DONE TODO: Wrong format violation
                            violations.append(
                                self.JustInTimeMappingFormatViolation(participant_parent, participant_stranger,
                                                                      mesh_stranger, direction, constraint))
                    else:
                        # Wrong direction
                        if constraint == MappingConstraint.CONSISTENT:
                            # Correct format
                            # DONE TODO: Wrong direction violation
                            violations.append(
                                self.JustInTimeMappingDirectionViolation(participant_parent, participant_stranger,
                                                                         mesh_stranger, direction))
                        else:
                            # Wrong format and wrong direction
                            # DONE TODO: Wrong direction+format violation
                            violations.append(
                                self.JustInTimeMappingFormatDirectionViolation(participant_parent, participant_stranger,
                                                                               mesh_stranger, direction, constraint,
                                                                               type))
                elif direction == Direction.WRITE:
                    # For a write-mapping, the 'to' mesh needs to be defined
                    if mapping.to_mesh:
                        # Correct direction
                        # For a JIT-write-mapping, the constraint has to be conservative
                        if constraint == MappingConstraint.CONSERVATIVE:
                            # This is fine
                            pass
                        else:
                            # Correct direction, but wrong constraint
                            # DONE TODO: Wrong format violation
                            violations.append(
                                self.JustInTimeMappingFormatViolation(participant_parent, participant_stranger,
                                                                      mesh_stranger, direction, constraint))
                    else:
                        # Wrong direction
                        if constraint == MappingConstraint.CONSERVATIVE:
                            # Correct format
                            # DONE TODO: Wrong direction violation
                            violations.append(
                                self.JustInTimeMappingDirectionViolation(participant_parent, participant_stranger,
                                                                         mesh_stranger, direction))
                        else:
                            # Wrong format and wrong direction
                            # DONE TODO: Wrong direction+format violation
                            violations.append(
                                self.JustInTimeMappingFormatDirectionViolation(participant_parent, participant_stranger,
                                                                               mesh_stranger, direction, constraint,
                                                                               type))

                # Check if participant receives mesh with api-access true
                receive_meshes = mapping.parent_participant.receive_meshes
                for receive_mesh in receive_meshes:
                    if receive_mesh.mesh == mesh_stranger:
                        # If api-access != true, then participant does not have permission to read from/write to it
                        if not receive_mesh.api_access:
                            # DONE TODO: NO PERMISSION VIOLATION
                            violations.append(
                                self.JustInTimeMappingPermissionViolation(participant_parent, participant_stranger,
                                                                          mesh_stranger, direction))

                # Check if mapping-participants also have a coupling scheme and then also an exchange
                coupling = get_coupling_scheme_of_mapping(couplings, participant_parent, participant_stranger)
                if not coupling:
                    # Participants try to map data, but there exists no coupling scheme between them
                    # DONE TODO: NO COUPLING VIOLATION
                    violations.append(
                        self.MissingCouplingSchemeMappingViolation(participant_parent, participant_stranger,
                                                                   mesh_stranger, direction))
                    # Continue with next mapping; this one cannot cause more violations
                    continue
                exchanges = get_exchange_of_participants(participant_parent, participant_stranger, coupling)
                if not exchanges:
                    # DONE TODO: NO EXCHANGE VIOLATION
                    violations.append(
                        self.MissingExchangeMappingViolation(participant_parent, participant_stranger, mesh_stranger,
                                                             direction))
                    # Continue with next mapping; this one cannot cause more violations
                    continue
                # Check if any exchange of the participants coupling-scheme is “correct”, i.e., on the strangers mesh
                if not any(exchange_belongs_to_mapping(exchange, direction, participant_stranger, mesh_stranger) for
                           exchange in exchanges):
                    # No correct exchange:
                    # DONE TODO: Exchange incorrect violation
                    #  Differentiate between incorrect direction / incorrect mesh ?
                    #  Maybe not, as they are connected
                    violations.append(
                        self.IncorrectExchangeMappingViolation(participant_parent, participant_stranger, mesh_stranger,
                                                               direction))

            # JIT-mappings have been handled
            else:

                if mapping.from_mesh in participant_parent.provide_meshes:
                    mesh_parent = mapping.from_mesh
                    mesh_stranger = mapping.to_mesh
                elif mapping.to_mesh in participant_parent.provide_meshes:
                    mesh_parent = mapping.to_mesh
                    mesh_stranger = mapping.from_mesh
                else:
                    # This case should not exist, if precice-tools --check ran.
                    pass
                participant_stranger = get_participant_of_mesh(graph, mesh_stranger)

                if direction == Direction.READ:
                    # In a read-mapping, the 'to'-mesh has to be by the parent, the 'from'-mesh by Stranger
                    if not mesh_parent == mapping.to_mesh:
                        # DONE TODO: Wrong direction violation
                        violations.append(
                            self.MappingDirectionViolation(participant_parent, participant_stranger, mesh_parent,
                                                           mesh_stranger, direction))
                elif direction == Direction.WRITE:
                    # In a write-mapping, the 'from'-mesh has to be by the parent, the 'to'-mesh by stranger
                    if not mesh_parent == mapping.from_mesh:
                        # DONE TODO: Wrong direction violation
                        violations.append(
                            self.MappingDirectionViolation(participant_parent, participant_stranger, mesh_parent,
                                                           mesh_stranger, direction))

                # Check if there exists a coupling-scheme between Parent and Stranger
                coupling = get_coupling_scheme_of_mapping(couplings, participant_parent, participant_stranger)
                if not coupling:
                    # DONE TODO: No coupling violation
                    violations.append(
                        self.MissingCouplingSchemeMappingViolation(participant_parent, participant_stranger,
                                                                   mesh_stranger, direction))
                    # Continue with next mapping; this one cannot cause more violations
                    continue

                # Check if the coupling-scheme between the participants is parallel
                if coupling in parallel_couplings:
                    # Now, check whether it has the correct format: Only read-consistent and write-conservative are
                    #  allowed for parallel couplings
                    if direction == Direction.READ:
                        if not constraint == MappingConstraint.CONSISTENT:
                            # DONE TODO: Parallel participants wrong format violation
                            violations.append(
                                self.ParallelCouplingMappingFormatViolation(participant_parent,
                                                                            participant_stranger, mesh_parent,
                                                                            mesh_stranger, direction, constraint))
                    elif direction == Direction.WRITE:
                        if not constraint == MappingConstraint.CONSERVATIVE:
                            # DONE TODO: Parallel participants wrong format violation
                            violations.append(
                                self.ParallelCouplingMappingFormatViolation(participant_parent,
                                                                            participant_stranger, mesh_parent,
                                                                            mesh_stranger, direction, constraint))

                exchanges = get_exchange_of_participants(participant_parent, participant_stranger, coupling)
                if not exchanges:
                    # DONE TODO: No exchange violation
                    violations.append(
                        self.MissingExchangeMappingViolation(participant_parent, participant_stranger, mesh_stranger,
                                                             direction))
                    # Continue with next mapping; this one cannot cause more violations
                    continue

                # Depending on the direction of the mapping, 'from'- and 'to'-mesh are defined differently
                if not any(exchange_belongs_to_mapping(exchange, direction, participant_stranger, mesh_stranger) for
                           exchange in exchanges):
                    # DONE TODO: EXCHANGE INCORRECT VIOLATION
                    violations.append(
                        self.IncorrectExchangeMappingViolation(participant_parent, participant_stranger, mesh_stranger,
                                                               direction))

        return violations


MappingRule()


# Helper functions
def exchange_belongs_to_mapping(exchange: ExchangeNode, direction: Direction, participant_stranger: ParticipantNode,
                                mesh_stranger: MeshNode) -> bool:
    """
        Evaluates whether the given exchange is correct for mapping corresponding to the given (stranger) participant,
        his mesh and the direction.

        It is known that the exchange belongs to both participants of the mapping and the given participant is NOT the
        parent of the mapping. Then, participant_stranger, mesh_stranger and direction should be enough to identify
        whether the exchange belongs to the mapping or not.
        :param exchange: The exchange to check.
        :param direction: The direction of the mapping to check.
        :param participant_stranger: The participant which is needed to check, whether the exchange belongs to the mapping
        :return: True if the exchange is in the correct direction and uses the correct mesh, False otherwise.
    """
    ex_dir: bool = False
    ex_mesh: bool = False
    if direction == Direction.READ:
        # In a read-mapping, Stranger should correspond to the exchange's from-participant
        if participant_stranger == exchange.from_participant:
            ex_dir = True
            # Otherwise, the direction is false
    elif direction == Direction.WRITE:
        # In a write-mapping, Stranger should correspond to the exchange's to-participant
        if participant_stranger == exchange.to_participant:
            ex_dir = True
            # Otherwise, the direction is false
    # In a mapping, Stranger's mesh should be used
    if mesh_stranger == exchange.mesh:
        ex_mesh = True
        # Otherwise, the mesh used is incorrect
    return ex_dir and ex_mesh


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


def get_coupling_scheme_of_mapping(couplings: list[CouplingSchemeNode | MultiCouplingSchemeNode], participant_a,
                                   participant_b
                                   ) -> CouplingSchemeNode | MultiCouplingSchemeNode | None:
    """
        This method returns the coupling scheme between the given participants.
        :param graph: The graph of the preCICE config.
        :param participant_a: One of the participants for which the coupling scheme is needed.
        :param participant_b: The other participant.
        :return:The coupling scheme between the participants; None if there is no coupling-scheme between the participants.
    """
    for coupling in couplings:
        if isinstance(coupling, CouplingSchemeNode):
            if ((participant_a == coupling.first_participant and participant_b == coupling.second_participant) or
                    (participant_b == coupling.first_participant and participant_a == coupling.second_participant)):
                return coupling
        elif isinstance(coupling, MultiCouplingSchemeNode):
            if participant_a in coupling.participants and participant_b in coupling.participants:
                return coupling
    return None


def get_exchange_of_participants(participant_a: ParticipantNode, participant_b: ParticipantNode,
                                 coupling: CouplingSchemeNode | MultiCouplingSchemeNode) -> list[ExchangeNode] | None:
    """
        This method returns the exchange nodes between the given participants in the given coupling-scheme,
        if any exist.
        :param participant_a: One of the participants for which the exchange is needed.
        :param participant_b: The other participant.
        :param coupling: The coupling-scheme between the participants, in which the exchange should exist.
        :return: A list of exchange nodes between the two participants, if any exist, else None.
    """
    exchange_nodes: list[ExchangeNode] = []
    # Both coupling-scheme nodes and multi-coupling-scheme-nodes have the same attribute 'exchanges'
    for exchange in coupling.exchanges:
        if ((participant_a == exchange.to_participant and participant_b == exchange.from_participant) or
                (participant_b == exchange.to_participant and participant_a == exchange.from_participant)):
            exchange_nodes.append(exchange)
    return exchange_nodes if exchange_nodes else None


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


def filter_coupling_nodes(graph: Graph) -> list[CouplingSchemeNode | MultiCouplingSchemeNode]:
    """
        This function returns all coupling-scheme nodes of the given graph.
        :param graph:The graph to check.
        :return: All (multi-)coupling-scheme nodes of the graph.
    """
    couplings: list[CouplingSchemeNode | MultiCouplingSchemeNode] = []
    for node in graph.nodes:
        if isinstance(node, CouplingSchemeNode) or isinstance(node, MultiCouplingSchemeNode):
            couplings.append(node)
    return couplings


def filter_parallel_coupling_nodes(graph: Graph) -> list[CouplingSchemeNode | MultiCouplingSchemeNode]:
    """
        This function returns all parallel coupling-scheme nodes of the given graph.
        :param graph:The graph to check.
        :return: All coupling-scheme nodes of the graph, which are either of type multi or ...-parallel.
    """
    couplings: list[CouplingSchemeNode | MultiCouplingSchemeNode] = []
    for node in graph.nodes:
        if isinstance(node, CouplingSchemeNode):
            if node.type in [CouplingSchemeType.PARALLEL_EXPLICIT, CouplingSchemeType.PARALLEL_IMPLICIT]:
                couplings.append(node)
        elif isinstance(node, MultiCouplingSchemeNode):
            couplings.append(node)
    return couplings
