import os

import pygame

import src
from src.constants import WIDTH, HEIGHT
from src.messages import ColumnWasClicked
from src.printers import print_model


def rgb_int2tuple(rgb):
    return (rgb // 256 // 256 % 256, rgb // 256 % 256, rgb % 256)


def print_rgb(r, g, b):
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


def print_scenario_description(events):
    log = ""
    test_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0][5:]
    log += test_name
    log += '\n'
    if not events:
        return
    sample_event = events[0]
    if isinstance(sample_event, ColumnWasClicked):
        log += print_player_moves(events)
    else:
        log += "events:\n"
        for event in events:
            log += f"{event}\n"
    return log


def print_player_moves(player_moves):
    log = ""
    log += f"Player moves:\n"
    players = ["RED", "YELLOW"]
    for i, move in enumerate(player_moves):
        current_player = players[i % len(players)]
        log += f"  {current_player}: {move.column}"
        if i % len(players) == 1:
            log += "\n"

    return log


def print_scenario(player_moves, model_and_surface, log):
    (model, surface) = model_and_surface
    ascii_art = print_surface(surface)
    state_string = print_model(model)
    return f'''\
SCENARIO:
{print_scenario_description(player_moves)}

FINAL STATE:
{state_string}

FINAL SCREEN:
{ascii_art}

SIMULATION LOG:
{log}
'''


def print_surface(surface):
    ascii_art_width = 79
    ascii_art_height = int(ascii_art_width // (WIDTH / HEIGHT))
    smaller = pygame.transform.scale(surface, (ascii_art_width, ascii_art_height))
    ascii_art = ''
    for y in range(smaller.get_height()):
        for x in range(smaller.get_width()):
            color = smaller.get_at_mapped((x, y))
            (r, g, b) = rgb_int2tuple(color)
            ascii_color = print_rgb(r, g, b)
            ascii_art += ascii_color
        ascii_art += '\n'
    return ascii_art


class ScenarioLogger:
    def __init__(self):
        self.log = ""

    def append_log(self, msg):
        self.log += f"LOG: {msg}\n"

    def __add__(self, other):
        self.log += str(other)
        return self

    def __call__(self, msg):
        self.append_log(msg)

    def __str__(self):
        return self.log