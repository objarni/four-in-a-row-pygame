from collections import defaultdict

# CONSTANTS #
RED, YELLOW, EMPTY = range(3)
WIDTH, HEIGHT = 1024, 768


class Color:
    WIDTH = 480
    HEIGHT = 600
    FPS = 60
    POWERUP_TIME = 5000
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)


# STATES #

class GameState(object):
    def __init__(self):
        self.board = defaultdict(lambda: EMPTY)
        self.whos_turn_is_it = RED

    def whos_turn(self):
        return print_color(self.whos_turn_is_it)


class GameOverState(object):
    def __init__(self, winner):
        self.winner = winner


# MESSAGES #

class ColumnWasClicked(object):
    def __init__(self, column):
        self.column = column


# FUNCTIONS #

def update(model, msg):
    if isinstance(model, GameState):
        if isinstance(msg, ColumnWasClicked):
            column = msg.column
            model.board = place_brick(model.board, model.whos_turn_is_it, column)
            model.whos_turn_is_it = (model.whos_turn_is_it + 1) % 2
            won = check_winning_state(model.board, RED)
            if won:
                return GameOverState(winner=RED)

    return model


def place_brick(board, color, column):
    for y in range(6, -1, -1):
        if board[(column, y)] == EMPTY:
            board[(column, y)] = color
            break
    return board


def print_color(color):
    return 'red' if color == RED else 'yellow'


def extract(board, pos, dir):
    cells = []
    for i in range(4):
        p = (pos[0] + dir[0] * i, pos[1] + dir[1] * i)
        cells.append(board[p])
    return cells


def check_winning_state(board, color):
    for y in range(6):
        for x in range(7):
            for dir in [(0, 1), (1, 0), (1, 1)]:
                cells = extract(board, (x, y), dir)
                if all(cell == color for cell in cells):
                    return True
    return False


# MAIN PROGRAM #

import pygame


def main_menu():
    pygame.display.update()

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break
            elif ev.key == pygame.K_q:
                pygame.quit()
                quit()
        elif ev.type == pygame.QUIT:
            pygame.quit()
            quit()
        else:
            draw_text(screen, "Press [ENTER] To Begin", 30, WIDTH / 2, HEIGHT / 2)
            draw_text(screen, "or [Q] To Quit", 30, WIDTH / 2, (HEIGHT / 2) + 40)
            pygame.display.update()

    # pygame.mixer.music.stop()
    # ready = pygame.mixer.Sound(path.join(sound_folder, 'getready.ogg'))
    # ready.play()
    screen.fill(Color.BLACK)
    draw_text(screen, "GET READY!", 40, WIDTH / 2, HEIGHT / 2)
    pygame.display.update()


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, Color.WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


if __name__ == '__main__':
    pygame.init()
    # pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Four in a row")
    clock = pygame.time.Clock()
    font_name = pygame.font.match_font('arial')
    main_menu()
    pygame.quit()
