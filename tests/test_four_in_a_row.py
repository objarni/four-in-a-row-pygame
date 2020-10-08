from collections import defaultdict

from approvaltests import verify

from src.four_in_a_row import (GameOverState, GameState, StartScreenState,
                               update, view, ColumnWasClicked,
                               LeftMouseDownAt, MouseMovedTo,
                               print_model)
import src.four_in_a_row


class FakeDrawingApi:
    def draw_rectangle(self, center, size, color):
        src.four_in_a_row.log(f"Drawing rectangle center {center} size {size} color {color}")

    def draw_disc(self, center, size, color):
        src.four_in_a_row.log(f'Drawing a disc center {center} size {size} color {color}')

    def draw_text(self, center, text, size, color):
        src.four_in_a_row.log(f"Drawing text '{text}' at {center} color {color} size {size}")

    def draw_image(self, center, name, dimension):
        src.four_in_a_row.log(f"Drawing image '{name}' at {center} dimension {dimension}")


def print_state_and_log(model):
    state_string = print_model(model)
    return f'STATE:\n{state_string}\n\nLOG:\n{log}'


def fake_view_model(model):
    fake_drawing_api = FakeDrawingApi()
    view(model, fake_drawing_api)


log = ''


def fake_log(s):
    global log
    log += s + '\n'


src.four_in_a_row.log = fake_log


def setup_function():
    global log
    log = ''


def simulate(model, messages):
    # Mimics behaviour of main event loop in four_in_a_row
    fake_api = FakeDrawingApi()
    view(model, fake_api)
    for msg in messages:
        # Handle events to update state
        old_model_repr = print_model(model)
        model = update(model, msg)

        # Display current model, if any change found
        if old_model_repr != print_model(model):
            fake_log("[STATE CHANGE, VIEWING]")
            view(model, fake_api)

    return model


def test_first_placed_brick_is_red():
    model = simulate(GameState(), [LeftMouseDownAt((300, 500))])
    verify(print_state_and_log(model))


def test_placing_4_bricks_in_first_column():
    model = GameState()
    model = simulate(model, [ColumnWasClicked(0)] * 4)
    verify(print_state_and_log(model))


def test_letting_red_win():
    model = GameState()
    msgs = [ColumnWasClicked(0), ColumnWasClicked(1)] * 3 + [ColumnWasClicked(0)]
    model = simulate(model, msgs)
    verify(print_state_and_log(model))


def test_letting_red_win_horisontally():
    model = GameState()
    model = simulate(model, [ColumnWasClicked(c) for c in [0, 5, 1, 5, 2, 5, 3]])
    verify(print_state_and_log(model))


def test_letting_yellow_win_horisontally():
    model = GameState()
    model = simulate(model, [ColumnWasClicked(c) for c in [0, 1, 0, 2, 0, 3, 1, 4]])
    verify(print_state_and_log(model))


def test_slash_red_win():
    model = GameState()
    model = simulate(model, [ColumnWasClicked(c) for c in [
        0, 1,
        1, 2,
        2, 3,
        2, 3,
        3, 5,
        3]])
    verify(print_state_and_log(model))


def test_backslash_yellow_win():
    model = GameState()
    model = simulate(model, [ColumnWasClicked(c) for c in [
        0, 6,
        5, 5,
        4, 4,
        3, 4,
        5, 3,
        0, 3,
        0, 3]])
    verify(print_state_and_log(model))


def test_startscreen():
    model = StartScreenState()
    verify(print_state_and_log(model))


def test_clicking_in_game_over_state():
    model = GameOverState(winner=src.four_in_a_row.RED, board=src.four_in_a_row.empty_board())
    model = simulate(model, [LeftMouseDownAt((1, 1))])
    verify(print_state_and_log(model))


def test_startscreen_to_game_transition():
    model = StartScreenState()
    model = simulate(model, [LeftMouseDownAt((1, 1))])
    verify(print_state_and_log(model))


def test_mouse_movement_over_game_screen():
    model = GameState()
    model = simulate(model, [MouseMovedTo((x, x)) for x in range(0, 500, 10)])
    verify(print_state_and_log(model))
