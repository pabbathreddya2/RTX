import sys
import os
from RTXConfiguration import RTXConfiguration
from kg2_querier import KG2Querier
import expand_utilities as eu

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from converter.PathListToGraphConverter import PathListToGraphConverter
from converter.SimpleGraphToContentGraphConverter import SimpleGraphToContentGraphConverter
from converter.EdgeExtractorFromPloverDB import EdgeExtractorFromPloverDB


class GraphToKnowledgeGraphConverter:

    def __init__(
            self,
            qnode_1_id,
            qnode_2_id,
            edge_extractor
    ):
        self.qnode_1_id = qnode_1_id
        self.qnode_2_id = qnode_2_id
        self.edge_extractor = edge_extractor

    def convert(self, response, paths):
        nodes, edges = PathListToGraphConverter(self.qnode_1_id, self.qnode_2_id).convert(paths)

        nodes, edges = SimpleGraphToContentGraphConverter(
            self.edge_extractor
        ).convert(nodes, edges, response)

        qg_organized_knowledge_graph = (
            KG2Querier(response, self.edge_extractor.get_extractor_url())._load_plover_answer_into_object_model(
                {
                    "nodes": nodes,
                    "edges": edges
                },
                response
            )
        )
        return eu.convert_qg_organized_kg_to_standard_kg(qg_organized_knowledge_graph)
