import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Names import Names
from HugeGraphConverter import HugeGraphConverter


class SuperNodeConverter:

    def __init__(
            self,
            paths,
            node_1_id,
            node_2_id,
            qnode_1_id,
            qnode_2_id,
            names
    ):
        self.paths = paths
        self.node_1_id = node_1_id
        self.node_2_id = node_2_id
        self.qnode_1_id = qnode_1_id
        self.qnode_2_id = qnode_2_id
        self.names = names

    def convert(self, response):
        occurrence_list_by_node_id = {}
        i = 0
        for path in self.paths:
            if len(path.links) < 2:
                response.warning("Path does not have sufficient edges: path length is less than 2")
                continue
            for j in range(1, len(path.links) - 1):
                node_id = path.links[j].id
                if node_id not in occurrence_list_by_node_id:
                    occurrence_list_by_node_id[node_id] = [i]
                else:
                    occurrence_list_by_node_id[node_id].append(i)

            i += 1

        sorted_occurrence_list_by_node_id = dict(
            sorted(occurrence_list_by_node_id.items(), key=lambda item: len(item[1]), reverse=True)
        )

        for key, values in sorted_occurrence_list_by_node_id.items():
            new_path = []
            for value in values:
                new_path.append(self.paths[value])
            HugeGraphConverter(
                new_path,
                self.node_1_id,
                self.node_2_id,
                self.qnode_1_id,
                self.qnode_2_id,
                Names(
                    q_edge_name=self.names.q_edge_name,
                    result_name=f"{self.names.result_name}_{key}",
                    auxiliary_graph_name=f"{self.names.auxiliary_graph_name}_{key}",
                    kg_edge_name=f"{self.names.kg_edge_name}_{key}",
                    node_id_for_essence=key,
                )
            ).convert(response)
