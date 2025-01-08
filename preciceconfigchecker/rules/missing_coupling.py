from typing import List

import networkx as nx
from networkx import Graph
from precice_config_graph.nodes import CouplingNode, MultiCouplingNode

from ..rule import Rule
from ..severity import Severity
from ..violation import Violation


class MissingCouplingRule(Rule):
    class MissingCouplingViolation(Violation):
        # No nodes have to be passed: A coupling is missing and does not depend on anything else
        # from the config file
        def __init__(self) -> None:
            pass

        def format_explanation(self) -> str:
            return f"It seems like your configuration is missing a coupling."

        def format_possible_solutions(self) -> List[str]:
            return [f"Please add either a coupling or a multi-coupling to your configuration."]

    severity = Severity.ERROR
    problem = "The configuration does not have any (multi-)couplings."

    def check(self, graph: Graph) -> None:
        # Find violations in the graph and add them to the violations list in Rule.
        coupling_nodes = nx.subgraph_view(graph, filter_node=filter_coupling_nodes)
        multi_coupling_nodes = nx.subgraph_view(graph, filter_node=filter_multi_coupling_nodes)

        # If both subgraphs are empty, no coupling nodes exist
        if nx.is_empty(coupling_nodes) and not nx.is_empty(multi_coupling_nodes):
            self.violations.append(self.MissingCouplingViolation())


def filter_coupling_nodes(node) -> bool:
    """
    A function filtering coupling nodes in the graph.
    :param node: the node to check
    :return: true, if the node is a coupling node.
    """
    if isinstance(node, CouplingNode):
        return True
    else:
        return False


def filter_multi_coupling_nodes(node) -> bool:
    """
    A function filtering multi-coupling nodes in the graph.
    :param node: the node to check
    :return: true, if the node is a multi-coupling node.
    """
    if isinstance(node, MultiCouplingNode):
        return True
    else:
        return False


MissingCouplingRule()
