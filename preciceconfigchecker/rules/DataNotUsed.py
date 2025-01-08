from typing import List

import networkx as nx
from networkx import Graph
from precice_config_graph.nodes import DataNode

from ..rule import Rule
from ..severity import Severity
from ..violation import Violation


class DataNotUsedRule(Rule):
    class DataNotUsedViolation(Violation):
        severity = Severity.WARNING

        def __init__(self, data_node):
            self.data_node = data_node

        def format_explanation(self) -> str:
            return f"Data {self.data_node.name} is declared but never used.\n"

        def format_possible_solutions(self) -> List[str]:
            return [f"Consider using {self.data_node.name} in a mesh or remove it to improve readability."]

        problem = "Data is declared but never used."

        def check(self, graph: Graph) -> None:

            data_nodes = nx.subgraph_view(graph, filter_node = filter_data_nodes)

            # get all data nodes in graph
            # for every data node:
            # check for outoing edges
            # if there are none, data node is never used -> add to violation


def filter_data_nodes(node) -> bool:
    if isinstance(node,DataNode):
        return True
    else:
        return False
