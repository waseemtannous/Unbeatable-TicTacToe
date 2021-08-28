from tkinter import Tk, Button, messagebox

X_PLAYER_MIN, O_PLAYER_MAX = 'x', 'o'
board = [[' ' for _ in range(3)] for _ in range(3)]
buttons = None


# get the next move using minimax algorithm with alpha-beta pruning
def minimax(currentState, alpha, beta, player):
    if checkFullBoard(currentState):
        return None, evaluate(currentState)

    nextPLayer = O_PLAYER_MAX if player == X_PLAYER_MIN else X_PLAYER_MIN

    edgeVal = float('-inf') if player == O_PLAYER_MAX else float('inf')
    nextState = None
    children = getAllChildrenStates(currentState, player)
    for child in children:
        evaluation = evaluate(child)

        # check if this player can win in one move
        if evaluation > 0 and player == O_PLAYER_MAX:
            return child, evaluation
        if evaluation < 0 and player == X_PLAYER_MIN:
            return child, evaluation

        _, val = minimax(child, alpha, beta, nextPLayer)
        if player == O_PLAYER_MAX:
            if val > edgeVal:
                edgeVal = val
                nextState = child
            alpha = max(alpha, val)
        else:
            if val < edgeVal:
                edgeVal = val
                nextState = child
            beta = min(beta, val)
        if beta < alpha:
            break
    return nextState, edgeVal


#############################################################################

# OLD IMPLEMENTATION. EASIER TO UNDERSTAND BUT CONTAINS DUPLICATE CODE
#
# def minimax(currentState, alpha, beta, player):
#     if checkFullBoard(currentState):
#         return None, evaluate(currentState)
#     if player == O_PLAYER_MAX:
#         maxVal = float('-inf')
#         nextState = None
#         children = getAllChildrenStates(currentState, player)
#         for child in children:
#             evaluation = evaluate(child)
#
#             # check if this player can win in one move
#             if evaluation > 0:
#                 return child, evaluation
#
#             _, val = minimax(child, alpha, beta, X_PLAYER_MIN)
#             if val > maxVal:
#                 maxVal = val
#                 nextState = child
#             alpha = max(alpha, val)
#             if beta <= alpha:
#                 break
#         return nextState, maxVal
#
#     if player == X_PLAYER_MIN:
#         minVal = float('inf')
#         nextState = None
#         children = getAllChildrenStates(currentState, player)
#         for child in children:
#             evaluation = evaluate(child)
#
#             # check if this player can win in one move
#             if evaluation < 0:
#                 return child, evaluation
#
#             _, val = minimax(child, alpha, beta, O_PLAYER_MAX)
#             if val < minVal:
#                 minVal = val
#                 nextState = child
#             beta = min(beta, val)
#             if beta <= alpha:
#                 break
#         return nextState, minVal
#
#
#############################################################################

# returns all available moves for the player
def getAllChildrenStates(state, player):
    children = []
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i][j] == ' ':
                child = [row[:] for row in state]
                child[i][j] = player
                children.append(child)
    return children


# check if the board is full
def checkFullBoard(state):
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i][j] == ' ':
                return False
    return True


# evaluates the current game state
def evaluate(state):
    retVal = 0

    # check columns
    for col in range(3):
        if state[0][col] == state[1][col] == state[2][col] == X_PLAYER_MIN:
            retVal = -1
        elif state[0][col] == state[1][col] == state[2][col] == O_PLAYER_MAX:
            retVal = 1

    # check rows
    for row in range(3):
        if state[row][0] == state[row][1] == state[row][2] == X_PLAYER_MIN:
            retVal = -1
        elif state[row][0] == state[row][1] == state[row][2] == O_PLAYER_MAX:
            retVal = 1

    # check diagonals
    if state[0][0] == state[1][1] == state[2][2] == X_PLAYER_MIN:
        retVal = -1
    elif state[0][0] == state[1][1] == state[2][2] == O_PLAYER_MAX:
        retVal = 1

    if state[2][0] == state[1][1] == state[0][2] == X_PLAYER_MIN:
        retVal = -1
    elif state[2][0] == state[1][1] == state[0][2] == O_PLAYER_MAX:
        retVal = 1

    emptyCounter = 1
    for i in range(len(state)):
        for j in range(len(state)):
            if state[i][j] == ' ':
                emptyCounter += 1

    return retVal * emptyCounter


# everytime the player clicks a button, this function is activated
def buttonClick(button, i, j):
    global board
    if not button["text"] == " ":
        return
    button["text"] = X_PLAYER_MIN
    board[i][j] = X_PLAYER_MIN
    if checkFullBoard(board):
        if checkEndCondition(board):
            reset()
            return
    if checkEndCondition(board):
        reset()
        return
    nextBoard, _ = minimax(currentState=board, alpha=float('-inf'), beta=float('inf'), player=O_PLAYER_MAX)
    if not nextBoard:
        if checkEndCondition(board):
            reset()
            return
    board = nextBoard
    drawBoard()
    if checkEndCondition(board):
        reset()


# draws the board on the screen
def drawBoard():
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == O_PLAYER_MAX:
                button = buttons[(3 * i) + j]
                button["text"] = "o"
            if board[i][j] == X_PLAYER_MIN:
                button = buttons[(3 * i) + j]
                button["text"] = "x"


# this functions resets the board to its empty state
def reset():
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    for button in buttons:
        button["text"] = " "


def checkEndCondition(state):
    value = evaluate(state)
    retVal = False
    if value == 0 and checkFullBoard(state):
        messagebox.showinfo(message='TIE !!')
        retVal = True
    elif value > 0:
        messagebox.showinfo(message='YOU LOST !!')
        retVal = True
    elif value < 0:
        messagebox.showinfo(message='YOU WON !!')
        retVal = True
    return retVal


if __name__ == '__main__':
    root = Tk()
    root.title('Unbeatable Tic Tac Toe')
    root.geometry('560x555')
    root.resizable(height=False, width=False)

    # buttons attributes
    font = ("Helvetica", 20)
    height = 5
    width = 11

    button1 = Button(root, text=" ", font=font, height=height, width=width, fg="#bbbbbb", bg="#2b2b2b", borderwidth=4,
                     command=lambda: buttonClick(button1, 0, 0))
    button2 = Button(root, text=" ", font=font, height=height, width=width, fg="#bbbbbb", bg="#2b2b2b", borderwidth=4,
                     command=lambda: buttonClick(button2, 0, 1))
    button3 = Button(root, text=" ", font=font, height=height, width=width, fg="#bbbbbb", bg="#2b2b2b", borderwidth=4,
                     command=lambda: buttonClick(button3, 0, 2))
    button4 = Button(root, text=" ", font=font, height=height, width=width, fg="#bbbbbb", bg="#2b2b2b", borderwidth=4,
                     command=lambda: buttonClick(button4, 1, 0))
    button5 = Button(root, text=" ", font=font, height=height, width=width, fg="#bbbbbb", bg="#2b2b2b", borderwidth=4,
                     command=lambda: buttonClick(button5, 1, 1))
    button6 = Button(root, text=" ", font=font, height=height, width=width, fg="#bbbbbb", bg="#2b2b2b", borderwidth=4,
                     command=lambda: buttonClick(button6, 1, 2))
    button7 = Button(root, text=" ", font=font, height=height, width=width, fg="#bbbbbb", bg="#2b2b2b", borderwidth=4,
                     command=lambda: buttonClick(button7, 2, 0))
    button8 = Button(root, text=" ", font=font, height=height, width=width, fg="#bbbbbb", bg="#2b2b2b", borderwidth=4,
                     command=lambda: buttonClick(button8, 2, 1))
    button9 = Button(root, text=" ", font=font, height=height, width=width, fg="#bbbbbb", bg="#2b2b2b", borderwidth=4,
                     command=lambda: buttonClick(button9, 2, 2))

    buttons = [button1, button2, button3, button4, button5, button6, button7, button8, button9]

    button1.grid(row=0, column=0)
    button2.grid(row=0, column=1)
    button3.grid(row=0, column=2)
    button4.grid(row=1, column=0)
    button5.grid(row=1, column=1)
    button6.grid(row=1, column=2)
    button7.grid(row=2, column=0)
    button8.grid(row=2, column=1)
    button9.grid(row=2, column=2)

    root.mainloop()
