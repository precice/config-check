from typing import List

import networkx as nx
from networkx import DiGraph
from precice_config_graph.nodes import CouplingNode, MultiCouplingNode
from rule import Rule
from severity import Severity
from violation import Violation


class MissingCouplingRule(Rule):
    # As participants need a coupling to communicate, a coupling must exist.
    # If no coupling exists, then this gets treated as an error.
    severity = Severity.ERROR
    problem = "The configuration does not have any (multi-)couplings."

    class MissingCouplingViolation(Violation):
        # No nodes have to be passed: A coupling is missing and does not depend on anything else
        # from the config file
        def __init__(self) -> None:
            pass

        def format_explanation(self) -> str:
            return "It seems like your configuration is missing a coupling."

        def format_possible_solutions(self) -> List[str]:
            return ["Please add either a coupling or a multi-coupling to your configuration."]

    def check(self, graph: DiGraph) -> None:
        # Find violations in the graph and add them to the violations list in Rule.
        coupling_nodes = nx.subgraph_view(graph, filter_node=filter_coupling_nodes)
        multi_coupling_nodes = nx.subgraph_view(graph, filter_node=filter_multi_coupling_nodes)

        # If both subgraphs are empty, no coupling nodes exist
        if nx.is_empty(coupling_nodes) and nx.is_empty(multi_coupling_nodes):
            self.violations.append(self.MissingCouplingViolation())


def filter_coupling_nodes(node) -> bool:
    """
    A function filtering coupling nodes in the graph.

    Args:
        node: the node to check

    Returns:
        true, if the node is a coupling node.
    """
    return isinstance(node, CouplingNode)


def filter_multi_coupling_nodes(node) -> bool:
    """
    A function filtering multi-coupling nodes in the graph.

    Args:
      node (Node): to check

    Returns:
      bool:  true, if the node is a multi-coupling node.
    """
    return isinstance(node, MultiCouplingNode)


MissingCouplingRule()
