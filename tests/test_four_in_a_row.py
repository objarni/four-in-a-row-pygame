from approvaltests import verify

from src.four_in_a_row import (GameOverState,GameState, StartScreenState,
                               update, view, ColumnWasClicked, run_messages,
                               LeftMouseClickAt, MouseMovedTo,
                                print_model)
import src.four_in_a_row


class FakeDrawingApi:
    def draw_rectangle(self, center, size, color):
        src.four_in_a_row.log(f"Drawing rectangle center {center} size {size} color {color}")

    def draw_disc(self, center, size, color):
        src.four_in_a_row.log(f'Drawing a disc center {center} size {size} color {color}')

    def draw_text(self, center, text, size, color):
        src.four_in_a_row.log(f"Drawing text '{text}' at {center} color {color} size {size}")


def print_for_verify(model):
    state_string = print_model(model)
    fake_view_model(model)
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


def test_letting_yellow_win_horisontally():
    model = GameState()
    model = run_messages(model, [ColumnWasClicked(c) for c in [0, 1, 0, 2, 0, 3, 1, 4]])
    verify(print_for_verify(model))


def test_slash_red_win():
    model = GameState()
    model = run_messages(model, [ColumnWasClicked(c) for c in [
        0, 1,
        1, 2,
        2, 3,
        2, 3,
        3, 5,
        3]])
    verify(print_for_verify(model))


def test_backslash_yellow_win():
    model = GameState()
    model = run_messages(model, [ColumnWasClicked(c) for c in [
        0, 6,
        5, 5,
        4, 4,
        3, 4,
        5, 3,
        0, 3,
        0, 3]])
    verify(print_for_verify(model))


def test_startscreen():
    model = StartScreenState()
    verify(print_for_verify(model))


def test_startscreen_to_game_transition():
    model = StartScreenState()
    model = run_messages(model, [LeftMouseClickAt((1, 1))])
    verify(print_for_verify(model))


def test_mouse_movement_over_game_screen():
    model = GameState()
    model = run_messages(model, [MouseMovedTo((x, x)) for x in range(0, 500, 10)])
    verify(print_for_verify(model))
