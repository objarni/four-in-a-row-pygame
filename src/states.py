from collections import defaultdict, namedtuple

from src.constants import CENTER, RED, EMPTY


class StartScreenState(object):
    def __init__(self):
        self.time = 0
        self.music_playing = False


class GameState(object):
    def __init__(self):
        self.board = empty_board()
        self.whos_turn_is_it = RED
        self.mouse_pos = CENTER
        self.mouse_down_time = None
        self.time = None


def empty_board():
    return defaultdict(lambda: EMPTY)


GameOverState = namedtuple('GameOverState', 'winner board')
