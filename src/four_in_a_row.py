from collections import defaultdict

# CONSTANTS #
DISC_SIZE = 80
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
    print(f"Placing brick color {color}")
    for i in range(6):
        y = 5 - i
        print(f"checking {column, y}")
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


def view(model, screen):
    if isinstance(model, GameState):
        screen.fill(Color.BLACK)
        for y in range(6):
            for x in range(7):
                value = model.board[(x, y)]
                if value != EMPTY:
                    color = Color.RED if value == RED else Color.YELLOW
                    x0 = int(WIDTH/2 - 7 * DISC_SIZE/2 + x * DISC_SIZE)
                    y0 = int(HEIGHT/2 - 6 * DISC_SIZE/2 + y * DISC_SIZE)
                    pos = (x0, y0)
                    pygame.draw.circle(screen, color, pos, DISC_SIZE//2, DISC_SIZE//2)

    draw_text(screen, "Press [ENTER] To Begin", 30, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "or [Q] To Quit", 30, WIDTH / 2, (HEIGHT / 2) + 40)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, Color.WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# MAIN PROGRAM #

import pygame


def mainloop(screen):
    model = GameState()
    msgs = []
    while True:
        # Translate low level events to domain events
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                msgs.append(ColumnWasClicked(0))
            elif ev.key == pygame.K_q:
                break
        elif ev.type == pygame.QUIT:
            break

        # Handle events updating state
        while len(msgs) > 0:
            msg = msgs.pop(0)
            model = update(model, msg)

        # Display current model
        view(model, screen)

        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Four in a row")
    clock = pygame.time.Clock()
    font_name = pygame.font.match_font('arial')
    mainloop(screen)
    pygame.quit()
