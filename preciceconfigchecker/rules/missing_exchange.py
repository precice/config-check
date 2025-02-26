from typing import List

import networkx as nx
from networkx import Graph
from precice_config_graph.nodes import ExchangeNode, CouplingSchemeNode, MultiCouplingSchemeNode
from rule import Rule
from severity import Severity
from violation import Violation


class MissingExchangeRule(Rule):
    # A coupling-scheme without an exchange is not allowed.
    severity = Severity.ERROR
    name = "Missing data exchange in a coupling-scheme."

    class MissingExchangeViolation(Violation):
        """
        This class handles coupling-schemes missing data-exchanges.
        """

        def __init__(self, coupling_scheme: CouplingSchemeNode | MultiCouplingSchemeNode) -> None:
            self.coupling_scheme = coupling_scheme

        def format_explanation(self) -> str:
            if isinstance(self.coupling_scheme, CouplingSchemeNode):
                return (f"The coupling-scheme between participants {self.coupling_scheme.first_participant} and "
                        f"{self.coupling_scheme.second_participant} is missing an exchange.")
            else:
                return (f"The multi-coupling-scheme of control-participant {self.coupling_scheme.control_participant} "
                        f"is missing an exchange.")

        def format_possible_solutions(self) -> List[str]:
            return ["Please add an exchange to the coupling-scheme.",
                    "Otherwise, please remove it to improve readability."]

    def check(self, graph: Graph) -> None:
        # Only exchange and coupling-scheme nodes remain
        g1 = nx.subgraph_view(graph, filter_node=filter_exchange_coupling_scheme_nodes)
        # Check all of them
        for node in g1.nodes():
            if isinstance(node, CouplingSchemeNode):
                # Check whether the coupling-scheme node has any exchange node neighbors
                if not g1.neighbors(node):
                    # If not, then it does not have an exchange
                    self.violations.addpend(self.MissingExchangeViolation(node))


# Initialize a rule object to add it to the rules-array.
MissingExchangeRule()


# Helper functions
def filter_exchange_coupling_scheme_nodes(node) -> bool:
    """
    A function filtering exchange and (multi-)coupling-scheme nodes in the graph.

    Args:
        node: the node to check

    Returns:
        True, if the node is an exchange or (multi-)coupling-scheme node.
    """
    return isinstance(node, CouplingSchemeNode) or MultiCouplingSchemeNode or isinstance(node, ExchangeNode)
