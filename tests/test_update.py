from approvaltests import verify

from src.four_in_a_row import (GameOverState, update, GameState, ColumnWasClicked, print_color,
                               EMPTY, RED, YELLOW)


def print_model(model):
    state = model.__class__.__name__ + '\n'
    if isinstance(model, GameOverState):
        state += f'{print_color(model.winner).title()} won.\n'
    if isinstance(model, GameState):
        state += f'It is {model.whos_turn()}s turn.\n'
        symbols = {
            EMPTY: 'O',
            RED: 'R',
            YELLOW: 'Y'
        }
        for y in range(7):
            for x in range(6):
                pos = (x, y)
                board = model.board
                cell = board[pos]
                state += symbols[cell] + ' '
            state += '\n'
    return state


def test_first_placed_brick_is_red():
    model = GameState()
    model = update(model, ColumnWasClicked(0))
    state = print_model(model)
    verify(state)


def test_placing_4_bricks_in_first_column():
    model = GameState()
    model = update(model, ColumnWasClicked(0))
    model = update(model, ColumnWasClicked(0))
    model = update(model, ColumnWasClicked(0))
    model = update(model, ColumnWasClicked(0))
    state = print_model(model)
    verify(state)


def test_letting_red_win():
    model = GameState()
    model = update(model, ColumnWasClicked(0))  # red
    model = update(model, ColumnWasClicked(1))  # yellow
    model = update(model, ColumnWasClicked(0))  # red
    model = update(model, ColumnWasClicked(1))  # yellow
    model = update(model, ColumnWasClicked(0))  # red
    model = update(model, ColumnWasClicked(1))  # yellow
    model = update(model, ColumnWasClicked(0))  # red
    state = print_model(model)
    verify(state)


def test_letting_red_win_horisontally():
    model = GameState()
    model = update(model, ColumnWasClicked(0))  # red
    model = update(model, ColumnWasClicked(5))  # yellow
    model = update(model, ColumnWasClicked(1))  # red
    model = update(model, ColumnWasClicked(5))  # yellow
    model = update(model, ColumnWasClicked(2))  # red
    model = update(model, ColumnWasClicked(5))  # yellow
    model = update(model, ColumnWasClicked(3))  # red
    state = print_model(model)
    verify(state)
