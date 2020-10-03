from approvaltests import verify

from src.four_in_a_row import (GameOverState, update, GameState, ColumnWasClicked, print_color,
                               EMPTY, RED, YELLOW, run_messages)
import src.four_in_a_row


def print_for_verify(model):
    state_string = model.__class__.__name__ + '\n'
    if isinstance(model, GameOverState):
        state_string += f'{print_color(model.winner).title()} won.\n'
    if isinstance(model, GameState):
        state_string += f'It is {model.whos_turn()}s turn.\n'
        symbols = {
            EMPTY: 'O',
            RED: 'R',
            YELLOW: 'Y'
        }
        for y in range(6):
            for x in range(7):
                pos = (x, y)
                board = model.board
                cell = board[pos]
                state_string += symbols[cell] + ' '
            state_string += '\n'
    return f'STATE:\n{state_string}\n\nLOG:\n{log}'


log = ''


def fake_log(s):
    global log
    log += s + '\n'


src.four_in_a_row.log = fake_log


def setup_test():
    global log
    log = ''


def test_first_placed_brick_is_red():
    model = GameState()
    model = update(model, ColumnWasClicked(0))
    verify(print_for_verify(model))


def test_placing_4_bricks_in_first_column():
    model = GameState()
    model = run_messages(model, [ColumnWasClicked(0)] * 4)
    verify(print_for_verify(model))


def test_letting_red_win():
    model = GameState()
    msgs = [ColumnWasClicked(0), ColumnWasClicked(1)] * 3 + [ColumnWasClicked(0)]
    model = run_messages(model, msgs)
    verify(print_for_verify(model))


def test_letting_red_win_horisontally():
    model = GameState()
    model = run_messages(model, [ColumnWasClicked(c) for c in [0, 5, 1, 5, 2, 5, 3]])
    verify(print_for_verify(model))
