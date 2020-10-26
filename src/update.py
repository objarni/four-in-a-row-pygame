from src.constants import DROP_DELAY_MS, RED, YELLOW, ROWS, EMPTY, COLUMNS, BOARD_LEFT, BOARD_RIGHT, DISC_DIAMETER
from src.messages import LeftMouseDownAt, Tick, ColumnWasClicked, MouseMovedTo, LeftMouseUpAt
from src.states import StartScreenState, GameState, GameOverState


def update(model, msg, audio_api):
    begin = lambda *args: args[-1]
    def assign(o, a, v):
        o.__setattr__(a, v)

    case_of = {
        (StartScreenState, LeftMouseDownAt): lambda: begin(
                audio_api.stop_music(),
                GameState()),
        (StartScreenState, Tick): lambda: begin(
                (assign(model, 'time', msg.time)),
                (audio_api.play_music('music') if not model.music_playing else None),
                (assign(model, 'music_playing', True)),
                model)
    }

    # if isinstance(model, StartScreenState):
    #     if isinstance(msg, LeftMouseDownAt):
    #         audio_api.stop_music()
    #         return GameState()
    #     if isinstance(msg, Tick):
    #         if not model.music_playing:
    #             audio_api.play_music('music')
    #             model.music_playing = True
    #         model.time = msg.time
    #         return model


    for condition in case_of:
        stateClass, msgClass = condition
        if isinstance(model, stateClass) and isinstance(msg, msgClass):
            return case_of[condition]()

    if isinstance(model, GameState):
        return update_gamestate(model, msg, audio_api)
    if isinstance(model, GameOverState):
        if isinstance(msg, LeftMouseDownAt):
            return StartScreenState()

    return model


def update_gamestate(gamestate, msg, audio_api):
    if isinstance(msg, Tick):
        gamestate.time = msg.time
        if (
            gamestate.mouse_down_time
            and gamestate.time > gamestate.mouse_down_time + DROP_DELAY_MS
        ):
            gamestate.mouse_down_time = None
            gamestate = update(gamestate, ColumnWasClicked(convert_to_column(gamestate.mouse_pos[0])), audio_api)
    if isinstance(msg, MouseMovedTo):
        gamestate.mouse_pos = msg.pos
    if (
        isinstance(msg, LeftMouseDownAt)
        and convert_to_column(msg.pos[0]) is not None
    ):
        gamestate.mouse_down = msg.pos
        gamestate.mouse_down_time = gamestate.time
    if isinstance(msg, LeftMouseUpAt):
        gamestate.mouse_down_time = None
    if isinstance(msg, ColumnWasClicked):
        if gamestate.board[(msg.column, 0)] != EMPTY:
            audio_api.play_sound('blocked')
        else:
            audio_api.play_sound('drop')
            gamestate.juice = 10
            gamestate.board = place_brick(gamestate.board, gamestate.whos_turn_is_it, msg.column)
            gamestate.whos_turn_is_it = (gamestate.whos_turn_is_it + 1) % 2
            for color in [RED, YELLOW]:
                won = check_winning_state(gamestate.board, color)
                if won:
                    gamestate = GameOverState(winner=color, board=gamestate.board)
    return gamestate


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
                log(f"Found 4-in-a-row at {x, y} direction {dir}")
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