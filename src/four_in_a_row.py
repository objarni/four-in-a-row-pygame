from collections import defaultdict


RED, YELLOW, EMPTY = range(3)


def print_color(color):
    return 'red' if color == RED else 'yellow'


class GameOverState(object):
    def __init__(self, winner):
        self.winner = winner


def extract(board, pos, dir):
    cells = []
    for i in range(4):
        p = (pos[0] + dir[0] * i, pos[1] + dir[1] * i)
        cells.append(board[p])
    return cells


def check_winning_state(board, color):
    for y in range(6):
        for x in range(7):
            for dir in [(0, 1), (1, 0), (1, 1)]:
                cells = extract(board, (x, y), dir)
                if all(cell == color for cell in cells):
                    return True
    return False


def update(model, msg):
    if isinstance(model, GameState):
        if isinstance(msg, ColumnWasClicked):
            column = msg.column
            model.board = place_brick(model.board, model.whos_turn_is_it, column)
            model.whos_turn_is_it = (model.whos_turn_is_it + 1) % 2
            won = check_winning_state(model.board, RED)
            if won:
                return GameOverState(winner=RED)

    return model


def place_brick(board, color, column):
    for y in range(6, -1, -1):
        if board[(column, y)] == EMPTY:
            board[(column, y)] = color
            break
    return board


class GameState(object):
    def __init__(self):
        self.board = defaultdict(lambda: EMPTY)
        self.whos_turn_is_it = RED

    def whos_turn(self):
        return print_color(self.whos_turn_is_it)


class ColumnWasClicked(object):
    def __init__(self, column):
        self.column = column
