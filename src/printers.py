from src.constants import EMPTY, RED, YELLOW, ROWS, COLUMNS
from src.states import StartScreenState, GameOverState, GameState
from src.update import int_to_color_name


def print_model(model):
    state_string = model.__class__.__name__ + '\n'
    if isinstance(model, StartScreenState):
        state_string += f'{model.time=}\n'
        state_string += f'{model.music_playing=}\n'
    if isinstance(model, GameOverState):
        state_string += print_board(model.board)
        state_string += f'\n{int_to_color_name(model.winner).title()} won.\n'
    if isinstance(model, GameState):
        state_string += f'It is {int_to_color_name(model.whos_turn_is_it)}s turn.\n'
        state_string += f'{model.time=}\n'
        state_string += f'The mouse is at {model.mouse_pos}.\n'
        state_string += f'{model.mouse_down_time=}\n'
        state_string += print_board(model.board)
    return state_string


def print_board(board):
    board_string = ''
    symbols = {
        EMPTY: 'O',
        RED: 'R',
        YELLOW: 'Y'
    }
    board_string += "0 1 2 3 4 5 6\n"
    board_string += "-------------\n"
    for y in range(ROWS):
        board_string += ' '.join(symbols[board[(x, y)]] for x in range(COLUMNS)) + '\n'
    return board_string


