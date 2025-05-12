# catan/board_graph.py
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from catan.board import hex_to_pixel, draw_hex, RESOURCE_COLORS

#Ports
HARBORS = [
    {"nodes": (68, 69), "type": "3:1"},
    {"nodes": (35, 36), "type": "wool"},
    {"nodes": (30, 31), "type": "ore"},
    {"nodes": (24, 25), "type": "3:1"},
    {"nodes": (45, 46), "type": "grain"},
    {"nodes": (51, 52), "type": "3:1"},
    {"nodes": (106, 107), "type": "lumber"},
    {"nodes": (93, 94), "type": "brick"},
    {"nodes": (81, 82), "type": "3:1"},
]

# === Intersections ===
INTERSECTION_POSITIONS = [
    (4, 0), (6, 0),
    (3, 1), (5, 1), (7, 1),
    (2, 2), (4, 2), (6, 2), (8, 2),
    (1, 3), (3, 3), (5, 3), (7, 3), (9, 3),
    (0, 4), (2, 4), (4, 4), (6, 4), (8, 4), (10, 4),
    (1, 5), (3, 5), (5, 5), (7, 5), (9, 5),
    (2, 6), (4, 6), (6, 6), (8, 6),
    (3, 7), (5, 7), (7, 7),
    (4, 8), (6, 8),

    (0,0), (0,0), (0,0), (0,0), (0,0),
    (0,0), (0,0), (0,0), (0,0), (0,0),
    (0,0), (0,0), (0,0), (0,0), (0,0),
    (0,0), (0,0), (0,0), (0,0), (0,0)
]

# === Legal Roads (edges between intersections) ===
INTERSECTION_EDGES = [
    (0, 2), (0, 3), (1, 3), (1, 4),
    (2, 5), (2, 6), (3, 6), (3, 7), (4, 7), (4, 8),
    (5, 9), (5, 10), (6, 10), (6, 11), (7, 11), (7, 12), (8, 12), (8, 13),
    (9, 14), (9, 15), (10, 15), (10, 16), (11, 16), (11, 17),
    (12, 17), (12, 18), (13, 18), (13, 19),
    (14, 20), (15, 20), (15, 21), (16, 21), (16, 22),
    (17, 22), (17, 23), (18, 23), (18, 24), (19, 24), (19, 25),
    (20, 26), (21, 26), (21, 27), (22, 27), (22, 28),
    (23, 28), (23, 29), (24, 29), (24, 30), (25, 30),
    (26, 31), (27, 31), (27, 32), (28, 32), (28, 33),
    (29, 33), (29, 34), (30, 34),
    (31, 35), (32, 35), (32, 36), (33, 36), (33, 37),
    (34, 37), (34, 38),
    (35, 39), (36, 39), (36, 40), (37, 40)
]

class BoardGraph:
    def __init__(self, board, hex_size=1):
        self.graph = nx.Graph()
        self.coord_to_node = {}  # Maps rounded (x, y) → node index
        self.next_node_id = 0
        self.hex_size = hex_size
        self._generate_from_board(board)
        self.harbors = HARBORS
        self._assign_harbors()

    def _generate_from_board(self, board):
        for tile in board.tiles:
            center_x, center_y = hex_to_pixel(tile.q, tile.r, self.hex_size)
            corners = self._get_hex_corners(center_x, center_y)
            corner_indices = []

            for x, y in corners:
                rounded = (round(x, 2), round(y, 2))  # Rounded to avoid float precision bugs
                if rounded not in self.coord_to_node:
                    self.coord_to_node[rounded] = self.next_node_id
                    self.graph.add_node(self.next_node_id, x=rounded[0], y=rounded[1], building=None, owner=None)
                    self.next_node_id += 1
                corner_indices.append(self.coord_to_node[rounded])

            # Connect corners of this tile in a cycle (each edge is a possible road)
            for i in range(6):
                a = corner_indices[i]
                b = corner_indices[(i + 1) % 6]
                if not self.graph.has_edge(a, b):
                    self.graph.add_edge(a, b, owner=None)

    def _get_hex_corners(self, cx, cy):
        """Return the 6 corner (x, y) positions for a flat-topped hex centered at (cx, cy)"""
        corners = []
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = np.radians(angle_deg)
            x = cx + self.hex_size * np.cos(angle_rad)
            y = cy + self.hex_size * np.sin(angle_rad)
            corners.append((x, y))
        return corners

    def build_settlement(self, node, player_id):
        if self.graph.nodes[node]['building'] is None:
            self.graph.nodes[node]['building'] = 'settlement'
            self.graph.nodes[node]['owner'] = player_id
            return True
        return False

    def build_road(self, a, b, player_id):
        if self.graph.has_edge(a, b) and self.graph[a][b]['owner'] is None:
            self.graph[a][b]['owner'] = player_id
            return True
        return False

    def get_available_settlement_spots(self):
        return [n for n, d in self.graph.nodes(data=True) if d['building'] is None]
    
    def _assign_harbors(self):
        for harbor in self.harbors:
            for node in harbor["nodes"]:
                if node in self.graph.nodes:
                    self.graph.nodes[node]["harbor"] = harbor["type"]


    


def render_board_with_graph(board, board_graph):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect('equal')
    ax.axis('off')

    # === Draw hex tiles ===
    for tile in board.tiles:
        x, y = hex_to_pixel(tile.q, tile.r)
        color = RESOURCE_COLORS.get(tile.resource, "#cccccc")
        label = "🌵" if tile.robber else (str(tile.number) if tile.number else "")
        draw_hex(ax, x, y, size=1, color=color, label=label)

    # === Draw intersection nodes ===
    for node_id, data in board_graph.graph.nodes(data=True):
        x, y = data['x'], data['y']
        ax.plot(x, y, 'o', color='black', markersize=5)
        ax.text(x, y + 0.2, str(node_id), ha='center', fontsize=6, color='blue')

        if "harbor" in data:
            ax.text(x, y - 0.2, f"{data['harbor']}", ha="center", fontsize=8, color="darkgreen")

    # === Draw road edges ===
    for a, b in board_graph.graph.edges:
        x1, y1 = board_graph.graph.nodes[a]['x'], board_graph.graph.nodes[a]['y']
        x2, y2 = board_graph.graph.nodes[b]['x'], board_graph.graph.nodes[b]['y']
        ax.plot([x1, x2], [y1, y2], color='gray', linewidth=1)

    plt.title("Catan Board with Intersections and Roads", fontsize=14)
    plt.show()

    if __name__ == "__main__":
        from catan.board import Board

        board = Board()
        graph = BoardGraph(board)
        print(graph.graph.nodes[0])
