from collections import defaultdict

import pygame
from approvaltests import verify

from src.four_in_a_row import (GameOverState, GameState, StartScreenState,
                               update, view, ColumnWasClicked,
                               LeftMouseDownAt, MouseMovedTo,
                               print_model, WIDTH, HEIGHT)
import src.four_in_a_row


class FakeDrawingApi:
    def __init__(self):
        self.surface = pygame.Surface(src.four_in_a_row.SCREENDIM)
        self.real_api = src.four_in_a_row.DrawingAPI(self.surface, '../res')

    def draw_rectangle(self, center, size, color):
        self.real_api.draw_rectangle(center, size, color)

    def draw_disc(self, center, size, color):
        self.real_api.draw_disc(center, size, color)

    def draw_text(self, center, text, size, color):
        self.real_api.draw_text(center, text, size, color)

    def draw_image(self, center, name, dimension):
        self.real_api.draw_image(center, name, dimension)


def rgb_int2tuple(rgbint):
    return (rgbint // 256 // 256 % 256, rgbint // 256 % 256, rgbint % 256)


def rgb_to_ascii(r, g, b):
    if sum([r, g, b]) < 10:
        return '.'
    if b < r > g and r > 100:
        return 'R'
    if r < g > b and g > 100:
        return 'G'
    if r < b > g and b > 100:
        return 'B'
    if r > 100 and g > 100 and b < 100:
        return 'Y'
    return 'W'


assert rgb_to_ascii(0, 0, 0) == '.'
assert rgb_to_ascii(200, 0, 0) == 'R'
assert rgb_to_ascii(0, 200, 0) == 'G'
assert rgb_to_ascii(0, 0, 200) == 'B'
assert rgb_to_ascii(200, 200, 0) == 'Y'
assert rgb_to_ascii(200, 200, 200) == 'W'


def print_result(model_and_surface):
    (model, surface) = model_and_surface
    ascii_art_width = 79
    ascii_art_height = int(ascii_art_width // (WIDTH / HEIGHT))
    smaller = pygame.transform.scale(surface, (ascii_art_width, ascii_art_height))
    ascii_art = ''
    for y in range(smaller.get_height()):
        for x in range(smaller.get_width()):
            color = smaller.get_at_mapped((x, y))
            (r, g, b) = rgb_int2tuple(color)
            ascii_color = rgb_to_ascii(r, g, b)
            ascii_art += ascii_color
        ascii_art += '\n'
    state_string = print_model(model)
    return f'''\
FINAL STATE:
{state_string}

FINAL SCREEN:
{ascii_art}

SIMULATION LOG:
{log}'''


log = ''


def fake_log(s):
    global log
    log += f"LOG: {s}\n"


src.four_in_a_row.log = fake_log


def setup_function():
    global log
    log = ''
    pygame.init()


def simulate(model, messages):
    global log
    # Mimics behaviour of main event loop in four_in_a_row
    fake_api = FakeDrawingApi()
    log += f"[SIMULATION STARTING]\n"
    log += f"===Model state===\n"
    log += f"{print_model(model)}\n\n\n"
    for msg in messages:
        log += f"[SIMULATING MSG={msg}]\n\n"
        model = update(model, msg)
        log += f"===Model state===\n"
        log += f"{print_model(model)}\n\n\n"
    log += f"[SIMULATION ENDED]"

    view(model, fake_api)
    return (model, fake_api.surface)


def test_first_placed_brick_is_red():
    result = simulate(GameState(), [ColumnWasClicked(0)])
    verify(print_result(result))


def test_placing_4_bricks_in_first_column():
    model = GameState()
    result = simulate(model, [ColumnWasClicked(0)] * 4)
    verify(print_result(result))


def test_letting_red_win():
    model = GameState()
    msgs = [ColumnWasClicked(0), ColumnWasClicked(1)] * 3 + [ColumnWasClicked(0)]
    result = simulate(model, msgs)
    verify(print_result(result))


def test_letting_red_win_horisontally():
    model = GameState()
    result = simulate(model, [ColumnWasClicked(c) for c in [0, 5, 1, 5, 2, 5, 3]])
    verify(print_result(result))


def test_letting_yellow_win_horisontally():
    model = GameState()
    result = simulate(model, [ColumnWasClicked(c) for c in [0, 1, 0, 2, 0, 3, 1, 4]])
    verify(print_result(result))


def test_slash_red_win():
    model = GameState()
    result = simulate(model, [ColumnWasClicked(c) for c in [
        0, 1,
        1, 2,
        2, 3,
        2, 3,
        3, 5,
        3]])
    verify(print_result(result))


def test_backslash_yellow_win():
    model = GameState()
    result = simulate(model, [ColumnWasClicked(c) for c in [
        0, 6,
        5, 5,
        4, 4,
        3, 4,
        5, 3,
        0, 3,
        0, 3]])
    verify(print_result(result))


def test_startscreen():
    model = StartScreenState()
    result = simulate(model, [])
    verify(print_result(result))


def test_clicking_in_game_over_state():
    print("HESAN")
    import os
    print(os.getcwd())
    model = GameOverState(winner=src.four_in_a_row.RED, board=src.four_in_a_row.empty_board())
    result = simulate(model, [LeftMouseDownAt((1, 1))])
    verify(print_result(result))


def test_startscreen_to_game_transition():
    model = StartScreenState()
    result = simulate(model, [LeftMouseDownAt((1, 1))])
    verify(print_result(result))


def test_mouse_movement_over_game_screen():
    model = GameState()
    result = simulate(model, [MouseMovedTo((x, x)) for x in range(0, 500, 10)])
    verify(print_result(result))
