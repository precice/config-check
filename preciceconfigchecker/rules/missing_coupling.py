from typing import List

import networkx as nx
from networkx import Graph
from precice_config_graph.nodes import CouplingSchemeNode, MultiCouplingSchemeNode

from preciceconfigchecker.rule import Rule
from preciceconfigchecker.severity import Severity
from preciceconfigchecker.violation import Violation


class MissingCouplingSchemeRule(Rule):
    # As participants need a coupling-scheme to communicate, a coupling-scheme must exist.
    # If no coupling exists, then this gets treated as an error.
    severity = Severity.ERROR
    name = "Missing coupling-scheme"

    class MissingCouplingSchemeViolation(Violation):
        # No nodes have to be passed: A coupling-scheme is missing and does not depend on anything else
        # from the config file
        def __init__(self) -> None:
            pass

        def format_explanation(self) -> str:
            return "It seems like your configuration is missing a coupling-scheme."

        def format_possible_solutions(self) -> List[str]:
            return ["Please add a coupling-scheme to your configuration to exchange data between participants."]

    def check(self, graph: Graph) -> None:
        # Filter all coupling-nodes: Only coupling-scheme nodes remain
        coupling_nodes = nx.subgraph_view(graph, filter_node=filter_coupling_scheme_nodes)
        # Filter all multi-coupling-nodes: Only multi-coupling-scheme nodes remain
        multi_coupling_nodes = nx.subgraph_view(graph, filter_node=filter_multi_coupling_scheme_nodes)

        # If both subgraphs contain no nodes, no coupling nodes exist
        if not coupling_nodes.nodes and not multi_coupling_nodes.nodes:
            self.violations.append(self.MissingCouplingSchemeViolation())


# Initialize a rule object to add it to the rules-array.
MissingCouplingSchemeRule()


# Helper functions
def filter_coupling_scheme_nodes(node) -> bool:
    """
    A function filtering coupling nodes in the graph.

    Args:
        node: the node to check

    Returns:
        True, if the node is a coupling node.
    """
    return isinstance(node, CouplingSchemeNode)


def filter_multi_coupling_scheme_nodes(node) -> bool:
    """
    A function filtering multi-coupling nodes in the graph.

    Args:
      node (Node): to check

    Returns:
      True, if the node is a multi-coupling node.
    """
    return isinstance(node, MultiCouplingSchemeNode)
