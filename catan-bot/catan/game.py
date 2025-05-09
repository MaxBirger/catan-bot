from catan.board import Board
from catan.player import Player
import random

class Game:
    def __init__(self, num_players=4):
        self.players = [Player(i) for i in range(num_players)]
        self.board = Board()
        self.current_turn = 0
        self.robber_tile = self._find_desert()

    def _find_desert(self):
        for idx, tile in enumerate(self.board.tiles):
            if tile.resource == 'desert':
                tile.robber = True
                return idx

    def roll_dice(self):
        return random.randint(1, 6) + random.randint(1, 6)

    def next_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)

    def get_current_player(self):
        return self.players[self.current_turn]