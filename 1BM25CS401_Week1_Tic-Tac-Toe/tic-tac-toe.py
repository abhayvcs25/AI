
import random

board = ["1", "2", "3",
         "4", "5", "6",
         "7", "8", "9"]

def show_board():
    print(board[0], "|", board[1], "|", board[2])
    print("--+---+--")
    print(board[3], "|", board[4], "|", board[5])
    print("--+---+--")
    print(board[6], "|", board[7], "|", board[8])


def check_winner(symbol):
    wins = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]

    for a, b, c in wins:
        if board[a] == board[b] == board[c]:
            return True

    return False


for turn in range(9):

    show_board()

    # Player's turn
    position = int(input("Enter your position (1-9): ")) - 1

    while board[position] == "X" or board[position] == "O":
        position = int(input("Position occupied. Enter again: ")) - 1

    board[position] = "X"

    if check_winner("X"):
        show_board()
        print("You Win!")
        break

    if turn == 8:
        show_board()
        print("Draw!")
        break

    # AI's turn
    empty = []

    for i in range(9):
        if board[i] not in ["X", "O"]:
            empty.append(i)

    ai_position = random.choice(empty)
    board[ai_position] = "O"

    print("AI selected:", ai_position + 1)

    if check_winner("O"):
        show_board()
        print("AI Wins!")
        break