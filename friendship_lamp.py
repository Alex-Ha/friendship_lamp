from data.pixel_art_matrices import valorant as valorant_matrix, aram as aram_matrix, peped as peped_matrices
from board import Board

def main():
    board = Board()

    board.display_art(aram_matrix)
    board.display_scrolling_art(valorant_matrix)
    board.display_animation(peped_matrices)

if __name__ == "__main__":
    main()