from typing import List

import networkx as nx
from networkx import Graph
from precice_config_graph.nodes import DataNode, ExchangeNode, MeshNode, ParticipantNode
from rule import Rule
from severity import Severity
from violation import Violation


class MissingExchangeRule(Rule):
    # To communicate data, it needs to be exchanged in a coupling scheme. Declaring and using data,
    # but without an exchange is an error.
    severity = Severity.ERROR
    name = "Data gets used but not exchanged in a coupling-scheme."

    class MissingExchangeViolation(Violation):

        def __init__(self, data_node: DataNode, mesh: MeshNode, reader: ParticipantNode,
                     writer: ParticipantNode) -> None:
            self.data_node = data_node
            self.mesh = mesh
            self.reader = reader
            self.writer = writer

        def format_explanation(self) -> str:
            return f"Data {self.data_node.name} does not get exchanged in a coupling-scheme."

        def format_possible_solutions(self) -> List[str]:
            return [""]

    def check(self, graph: Graph) -> None:
        g1 = nx.subgraph_view(graph, filter_node=filter_data_exchange_nodes)

        for node in g1.nodes():
            # Check all data nodes
            if isinstance(node, DataNode):
                adjacents = nx.neighbors(g1, node)
                # No adjacent nodes mean that there are no exchanges with this data-node
                if not adjacents:
                    # Now we have to get the mesh, reader and writer of data for the output message
                    # TODO
                    self.violations.append(self.MissingExchangeViolation(node))


# Initialize a rule object to add it to the rules-array.
MissingExchangeRule()


# Helper functions
def filter_data_exchange_nodes(node) -> bool:
    """
    A function filtering coupling nodes in the graph.

    Args:
        node: the node to check

    Returns:
        True, if the node is a coupling node.
    """
    return isinstance(node, DataNode) or isinstance(node, ExchangeNode)
