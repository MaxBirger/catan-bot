# catan/board_graph.py

import networkx as nx

class BoardGraph:
    def __init__(self):
        self.graph = nx.Graph()
        self._create_intersections_and_edges()

    def _create_intersections_and_edges(self):
        # This is a placeholder layout: full Catan has 54 intersections and 72 edges
        # We'll need to define a proper map or adjacency list later
        for i in range(54):
            self.graph.add_node(i, building=None, owner=None)  # Each node is a potential settlement spot

        for a, b in self._get_example_edges():
            self.graph.add_edge(a, b, owner=None)

    def _get_example_edges(self):
        # Sample manually defined edges; needs to be expanded to full board logic
        return [
            (0, 1), (1, 2), (2, 3),
            (3, 4), (4, 5), (5, 0),  # Hex ring example
            (1, 6), (2, 7), (3, 8)   # Stub connections
        ]

    def build_road(self, a, b, player_id):
        if self.graph.has_edge(a, b):
            self.graph[a][b]['owner'] = player_id

    def build_settlement(self, node, player_id):
        if self.graph.nodes[node]['building'] is None:
            self.graph.nodes[node]['building'] = 'settlement'
            self.graph.nodes[node]['owner'] = player_id

