from py2neo import Graph, NodeMatcher, RelationshipMatch, Table

from cypher_engine.models import ModelFactory
from settings import Config
from src.bioengine.cypher_engine.connections import Connection


class KnowledgeGraphConnection(Connection):
    """
    A class abstracting a knowledge graph instance hosted in a neo4j graph
    """

    def execute_string_query(self, query, **kwargs) -> Table:
        pass

    def get_nodes(self, concept: str, node_query=None, factory: ModelFactory = None) -> list:
        return list(ols_node.match(self.driver).where(f"_.label = '{concept}'"))

    def __init__(self, config: dict = None):
        if config is None:
            config = Config().get_property('neo4j')['knowledge_graph']
        self.driver = Graph(config['uri'], auth=(config['user'], config['password']))
        self.node_matcher = NodeMatcher(self.driver)
        self.relation_matcher = RelationshipMatch(self.driver)