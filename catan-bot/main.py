from catan.board import Board
from catan.board_graph import BoardGraph, render_board_with_graph

if __name__ == "__main__":
    board = Board()
    graph = BoardGraph(board)
    render_board_with_graph(board, graph)