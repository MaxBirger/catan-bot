import random

class Tile:
    def __init__(self, resource, number=None, q=0, r=0):
        self.resource = resource
        self.number = number
        self.q = q
        self.r = r
        self.robber = (resource == 'desert')

    def coords(self):
        return (self.q, self.r)

class Board:
    def __init__(self, layout=None):
        self.tiles = []
        if layout:
            self._load_custom_layout(layout)
        else:
            self._generate_default_axial_board()

    def _generate_default_axial_board(self):
        axial_coords = [
            (0, 0),
            (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1),
            (2, -2), (2, -1), (2, 0),
            (1, 1), (0, 2), (-1, 2),
            (-2, 2), (-2, 1), (-2, 0),
            (-1, -1), (0, -2), (1, -2)
        ]

        resources = (
            ['brick'] * 3 + ['lumber'] * 4 + ['grain'] * 4 +
            ['wool'] * 4 + ['ore'] * 3 + ['desert']
        )
        numbers = [2, 3, 3, 4, 4, 5, 5, 6, 6,
                8, 8, 9, 9, 10, 10, 11, 11, 12]

        random.shuffle(resources)
        random.shuffle(numbers)

        for (q, r) in axial_coords:
            resource = resources.pop()
            number = None if resource == 'desert' else numbers.pop()
            self.tiles.append(Tile(resource, number, q, r))

    def get_tile_at(self, q, r):
        for tile in self.tiles:
            if tile.q == q and tile.r == r:
                return tile
        return None


import matplotlib.pyplot as plt
import numpy as np

# Mapping resource to color
RESOURCE_COLORS = {
    "brick": "#B22222",
    "lumber": "#228B22",
    "grain": "#DAA520",
    "wool": "#7CFC00",
    "ore": "#708090",
    "desert": "#F5DEB3"
}

def hex_to_pixel(q, r, size=1):
    x = size * (3/2 * q)
    y = size * (np.sqrt(3) * (r + q / 2))
    return x, y

def draw_hex(ax, x, y, size, color, label=None):
    """Draw a single hexagon"""
    angles = np.linspace(0, 2 * np.pi, 7)
    xs = x + size * np.cos(angles)
    ys = y + size * np.sin(angles)
    ax.fill(xs, ys, color=color, edgecolor="black")
    if label is not None:
        ax.text(x, y, label, ha='center', va='center', fontsize=10, weight='bold')


def render_board(board):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_aspect('equal')
    ax.axis('off')

    for tile in board.tiles:
        x, y = hex_to_pixel(tile.q, tile.r)
        color = RESOURCE_COLORS.get(tile.resource, "#cccccc")
        label = "🌵" if tile.robber else (str(tile.number) if tile.number else "")
        draw_hex(ax, x, y, size=1, color=color, label=label)

    plt.title("Catan Board", fontsize=14)
    plt.show(block=True)