from typing import List

import networkx as nx
from networkx import Graph
from precice_config_graph.nodes import DataNode, MeshNode

from rule import Rule
from severity import Severity
from violation import Violation


class DataReadNotWrittenRule(Rule):
    class DataNeverWrittenViolation(Violation):
        severity = Severity.WARNING

        def __init__(self, data_node:DataNode):
            self.data_node = data_node

        def format_explanation(self) -> str:
            return ""

        def format_possible_solutions(self) -> List[str]:
            return [""]

        problem = ""

        def check(self, graph: Graph) -> None:
            data_nodes = nx.subgraph_view(graph, filter_node = filter_data_nodes)




def filter_data_nodes(node) -> bool:
    if isinstance(node,DataNode):
        return True
    else:
        return False
