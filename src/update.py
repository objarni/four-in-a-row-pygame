from src.constants import DROP_DELAY_MS, RED, YELLOW, ROWS, EMPTY, COLUMNS, BOARD_LEFT, BOARD_RIGHT, DISC_DIAMETER
from src.messages import LeftMouseDownAt, Tick, ColumnWasClicked, MouseMovedTo, LeftMouseUpAt
from src.states import StartScreenState, GameState, GameOverState


def update(model, msg, audio_api):
    if isinstance(model, StartScreenState):
        if isinstance(msg, LeftMouseDownAt):
            audio_api.stop_music()
            return GameState()
        if isinstance(msg, Tick):
            if not model.music_playing:
                audio_api.play_music('music')
                model.music_playing = True
            model.time = msg.time
            return model
    if isinstance(model, GameState):
        if isinstance(msg, Tick):
            model.time = msg.time
            if model.mouse_down_time:
                if model.time > model.mouse_down_time + DROP_DELAY_MS:
                    model.mouse_down_time = None
                    model = update(model, ColumnWasClicked(convert_to_column(model.mouse_pos[0])), audio_api)
        if isinstance(msg, MouseMovedTo):
            model.mouse_pos = msg.pos
        if isinstance(msg, LeftMouseDownAt):
            if convert_to_column(msg.pos[0]) is not None:
                model.mouse_down = msg.pos
                model.mouse_down_time = model.time
        if isinstance(msg, LeftMouseUpAt):
            model.mouse_down_time = None
        if isinstance(msg, ColumnWasClicked):
            audio_api.play_sound('drop')
            model.board = place_brick(model.board, model.whos_turn_is_it, msg.column)
            model.whos_turn_is_it = (model.whos_turn_is_it + 1) % 2
            for color in [RED, YELLOW]:
                won = check_winning_state(model.board, color)
                if won:
                    return GameOverState(winner=color, board=model.board)
    if isinstance(model, GameOverState):
        if isinstance(msg, LeftMouseDownAt):
            return StartScreenState()

    return model


def place_brick(board, color, column):
    log(f"Placing brick color {print_color(color)} in column {column}")
    for i in range(ROWS):
        y = ROWS - i - 1
        if board[(column, y)] == EMPTY:
            board[(column, y)] = color
            break
    return board


def print_color(color):
    return 'red' if color == RED else 'yellow'


def check_winning_state(board, color):
    for (x, y) in positions_in_print_order():
        for dir in [(0, 1), (1, 0), (1, 1), (-1, 1)]:
            cells = extract(board, (x, y), dir)
            if all(cell == color for cell in cells):
                log(f"Found 4-in-a-row at {x, y} dir {dir}")
                return True
    return False


def extract(board, pos, dir):
    cells = []
    for i in range(4):
        p = (pos[0] + dir[0] * i, pos[1] + dir[1] * i)
        cells.append(board[p])
    return cells


def positions_in_print_order():
    for y in range(ROWS):
        for x in range(COLUMNS):
            yield (x, y)


def convert_to_column(x):
    if x < BOARD_LEFT:
        return None
    if x > BOARD_RIGHT:
        return None
    return (x - BOARD_LEFT) // DISC_DIAMETER


def log(msg):
    pass
    # print(msg)