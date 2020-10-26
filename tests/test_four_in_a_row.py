import os

import pygame
import pytest
from approvaltests import verify

import src.constants
import src.four_in_a_row
import src.states
import src.update
from src.messages import LeftMouseDownAt, ColumnWasClicked, MouseMovedTo
from src.states import GameState, GameOverState, StartScreenState
from tests.fakes import simulate
from tests.printers import print_rgb, print_scenario, ScenarioLogger


@pytest.fixture
def log():
    logger = ScenarioLogger()
    src.update.log = logger
    return logger


def setup_function():
    pygame.init()


def test_print_rgb():
    assert print_rgb(0, 0, 0) == '.'
    assert print_rgb(200, 0, 0) == 'R'
    assert print_rgb(0, 200, 0) == 'G'
    assert print_rgb(0, 0, 200) == 'B'
    assert print_rgb(200, 200, 0) == 'Y'
    assert print_rgb(200, 200, 200) == 'W'


def test_first_placed_brick_is_red(log):
    player_moves = [ColumnWasClicked(0)]
    result = simulate(GameState(), player_moves, log)
    verify(print_scenario(player_moves, result, log))


def test_placing_4_bricks_in_first_column(log):
    model = GameState()
    player_moves = [ColumnWasClicked(0)] * 4
    result = simulate(model, player_moves, log)
    verify(print_scenario(player_moves, result, log))


def test_placing_too_many_bricks_in_first_column(log):
    model = GameState()
    player_moves = [ColumnWasClicked(0)] * 8
    result = simulate(model, player_moves, log)
    verify(print_scenario(player_moves, result, log))


def test_letting_red_win(log):
    model = GameState()
    player_moves = [ColumnWasClicked(0), ColumnWasClicked(1)] * 3 + [ColumnWasClicked(0)]
    result = simulate(model, player_moves, log)
    verify(print_scenario(player_moves, result, log))


def test_letting_red_win_horisontally(log):
    model = GameState()
    player_moves = [ColumnWasClicked(c) for c in [0, 5, 1, 5, 2, 5, 3]]
    result = simulate(model, player_moves, log)
    verify(print_scenario(player_moves, result, log))


def test_letting_yellow_win_horisontally(log):
    model = GameState()
    player_moves = [ColumnWasClicked(c) for c in [0, 1, 0, 2, 0, 3, 1, 4]]
    result = simulate(model, player_moves, log)
    verify(print_scenario(player_moves, result, log))


def test_slash_red_win(log):
    model = GameState()
    player_moves = [ColumnWasClicked(c) for c in [0, 1, 1, 2, 2, 3, 2, 3, 3, 5, 3]]
    result = simulate(model, player_moves, log)
    verify(print_scenario(player_moves, result, log))


def test_backslash_yellow_win(log):
    model = GameState()
    player_moves = [ColumnWasClicked(c) for c in [0, 6, 5, 5, 4, 4, 3, 4, 5, 3, 0, 3, 0, 3]]
    result = simulate(model, player_moves, log)
    verify(print_scenario(player_moves, result, log))


def test_startscreen(log):
    model = StartScreenState()
    ticks = [src.messages.Tick(ms) for ms in range(3)]
    result = simulate(model, ticks, log)
    verify(print_scenario(ticks, result, log))


def test_clicking_in_game_over_state(log):
    model = GameOverState(winner=src.constants.RED, board=src.states.empty_board())
    mouse_events = [LeftMouseDownAt((1, 1))]
    result = simulate(model, mouse_events, log)
    verify(print_scenario(mouse_events, result, log))


def test_startscreen_to_game_transition(log):
    model = StartScreenState()
    mouse_events = [LeftMouseDownAt((1, 1))]
    result = simulate(model, mouse_events, log)
    verify(print_scenario(mouse_events, result, log))


def test_mouse_movement_over_game_screen(log):
    model = GameState()
    mouse_events = [MouseMovedTo((x, x)) for x in range(0, 500, 10)]
    result = simulate(model, mouse_events, log)
    verify(print_scenario(mouse_events, result, log))
