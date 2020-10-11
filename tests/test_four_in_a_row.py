import pygame
from approvaltests import verify

import src.constants
import src.four_in_a_row
import src.states
import src.update
from src.constants import EMPTY, RED, YELLOW, ROWS, COLUMNS
from src.constants import (WIDTH, HEIGHT)
from src.messages import LeftMouseDownAt, ColumnWasClicked, MouseMovedTo
from src.states import GameState, GameOverState, StartScreenState
from src.update import print_color


class FakeDrawingAPI:
    def __init__(self):
        self.surface = pygame.Surface(src.constants.SCREENDIM)
        self.real_api = src.four_in_a_row.DrawingAPI(self.surface, '../res')

    def draw_rectangle(self, center, size, color):
        self.real_api.draw_rectangle(center, size, color)

    def draw_disc(self, center, size, color):
        self.real_api.draw_disc(center, size, color)

    def draw_text(self, center, text, size, color):
        self.real_api.draw_text(center, text, size, color)

    def draw_image(self, center, name, dimension):
        self.real_api.draw_image(center, name, dimension)

class FakeAudioAPI:
    def play_music(self, name):
        global log
        log += f"Starting music {name}.\n"

    def stop_music(self):
        global log
        log += f"Stopping music playback.\n"


def rgb_int2tuple(rgb):
    return (rgb // 256 // 256 % 256, rgb // 256 % 256, rgb % 256)


def project_rgb(r, g, b):
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


assert project_rgb(0, 0, 0) == '.'
assert project_rgb(200, 0, 0) == 'R'
assert project_rgb(0, 200, 0) == 'G'
assert project_rgb(0, 0, 200) == 'B'
assert project_rgb(200, 200, 0) == 'Y'
assert project_rgb(200, 200, 200) == 'W'


def project(model_and_surface):
    (model, surface) = model_and_surface
    ascii_art = project_surface(surface)
    state_string = project_model(model)
    return f'''\
FINAL STATE:
{state_string}

FINAL SCREEN:
{ascii_art}

SIMULATION LOG:
{log}'''


def project_model(model):
    state_string = model.__class__.__name__ + '\n'
    if isinstance(model, StartScreenState):
        state_string += f'{model.time=}\n'
        state_string += f'{model.music_playing=}\n'
    if isinstance(model, GameOverState):
        state_string += f'{print_color(model.winner).title()} won.\n'
    if isinstance(model, GameState):
        state_string += f'It is {print_color(model.whos_turn_is_it)}s turn.\n'
        state_string += f'{model.time=}\n'
        state_string += f'The mouse is at {model.mouse_pos}.\n'
        state_string += f'{model.mouse_down_time=}\n'
        state_string += project_board(model.board)
    return state_string


def project_surface(surface):
    ascii_art_width = 79
    ascii_art_height = int(ascii_art_width // (WIDTH / HEIGHT))
    smaller = pygame.transform.scale(surface, (ascii_art_width, ascii_art_height))
    ascii_art = ''
    for y in range(smaller.get_height()):
        for x in range(smaller.get_width()):
            color = smaller.get_at_mapped((x, y))
            (r, g, b) = rgb_int2tuple(color)
            ascii_color = project_rgb(r, g, b)
            ascii_art += ascii_color
        ascii_art += '\n'
    return ascii_art


def project_board(board):
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


log = ''


def fake_log(s):
    global log
    log += f"LOG: {s}\n"


src.update.log = fake_log


def setup_function():
    global log
    pygame.init()
    log = ''


def simulate(model, messages):
    global log
    # Mimics behaviour of main event loop in four_in_a_row
    fake_drawing = FakeDrawingAPI()
    fake_audio = FakeAudioAPI()
    log += f"[SIMULATION STARTING]\n"
    log += f"===Model state===\n"
    log += f"{project_model(model)}\n\n\n"
    for msg in messages:
        log += f"[SIMULATING MSG={msg}]\n\n"
        model = src.update.update(model, msg, fake_audio)
        log += f"===Model state===\n"
        log += f"{project_model(model)}\n\n\n"
    log += f"[SIMULATION ENDED]"

    src.view.view(model, fake_drawing)
    return (model, fake_drawing.surface)


def test_first_placed_brick_is_red():
    result = simulate(GameState(), [ColumnWasClicked(0)])
    verify(project(result))


def test_placing_4_bricks_in_first_column():
    model = GameState()
    result = simulate(model, [ColumnWasClicked(0)] * 4)
    verify(project(result))


def test_letting_red_win():
    model = GameState()
    msgs = [ColumnWasClicked(0), ColumnWasClicked(1)] * 3 + [ColumnWasClicked(0)]
    result = simulate(model, msgs)
    verify(project(result))


def test_letting_red_win_horisontally():
    model = GameState()
    result = simulate(model, [ColumnWasClicked(c) for c in [0, 5, 1, 5, 2, 5, 3]])
    verify(project(result))


def test_letting_yellow_win_horisontally():
    model = GameState()
    result = simulate(model, [ColumnWasClicked(c) for c in [0, 1, 0, 2, 0, 3, 1, 4]])
    verify(project(result))


def test_slash_red_win():
    model = GameState()
    result = simulate(model, [ColumnWasClicked(c) for c in [
        0, 1,
        1, 2,
        2, 3,
        2, 3,
        3, 5,
        3]])
    verify(project(result))


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
    verify(project(result))


def test_startscreen():
    model = StartScreenState()
    result = simulate(model, [src.messages.Tick(ms) for ms in range(3)])
    verify(project(result))


def test_clicking_in_game_over_state():
    model = GameOverState(winner=src.constants.RED, board=src.states.empty_board())
    result = simulate(model, [LeftMouseDownAt((1, 1))])
    verify(project(result))


def test_startscreen_to_game_transition():
    model = StartScreenState()
    result = simulate(model, [LeftMouseDownAt((1, 1))])
    verify(project(result))


def test_mouse_movement_over_game_screen():
    model = GameState()
    result = simulate(model, [MouseMovedTo((x, x)) for x in range(0, 500, 10)])
    verify(project(result))
