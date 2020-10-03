from collections import defaultdict

# CONSTANTS #
DISC_SIZE = 130
RED, YELLOW, EMPTY = range(3)
WIDTH, HEIGHT = 1200, 1200
CENTER = (WIDTH // 2, HEIGHT // 2)
COLUMNS = 7
ROWS = 6


class Color:
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
    log(f"Placing brick color {print_color(color)}")
    for i in range(ROWS):
        y = ROWS - i - 1
        log(f"checking {column, y}")
        if board[(column, y)] == EMPTY:
            board[(column, y)] = color
            break
    return board


def print_color(color):
    return 'red' if color == RED else 'yellow'


def check_winning_state(board, color):
    for (x, y) in all_positions():
        for dir in [(0, 1), (1, 0), (1, 1)]:
            cells = extract(board, (x, y), dir)
            if all(cell == color for cell in cells):
                return True
    return False


def extract(board, pos, dir):
    cells = []
    for i in range(4):
        p = (pos[0] + dir[0] * i, pos[1] + dir[1] * i)
        cells.append(board[p])
    return cells


def all_positions():
    for y in range(ROWS):
        for x in range(COLUMNS):
            yield (x, y)


def view(model, screen):
    if isinstance(model, GameState):
        screen.fill(Color.BLACK)
        r = pygame.Rect(0, 0, DISC_SIZE * COLUMNS + 20, DISC_SIZE * ROWS + 20)
        r.center = CENTER
        pygame.draw.rect(screen, Color.BLUE, r)
        for (x, y) in all_positions():
            value = model.board[(x, y)]
            color = Color.BLACK
            if value != EMPTY:
                color = Color.RED if value == RED else Color.YELLOW
            draw_disc(color, screen, x, y)

    draw_text(screen, f"{model.whos_turn().title()} to place disc", 30, WIDTH // 2, 0)
    # draw_text(screen, "or [Q] To Quit", 30, WIDTH / 2, (HEIGHT / 2) + 40)


def draw_disc(color, screen, x, y):
    x0 = int(WIDTH / 2 - COLUMNS * DISC_SIZE / 2 + x * DISC_SIZE + DISC_SIZE // 2)
    y0 = int(HEIGHT / 2 - ROWS * DISC_SIZE / 2 + y * DISC_SIZE + DISC_SIZE // 2)
    pos = (x0, y0)
    pygame.draw.circle(screen, color, pos, DISC_SIZE // 2, DISC_SIZE // 2)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, Color.WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


# MAIN PROGRAM #

import pygame


def log(msg):
    print(msg)


def mainloop(screen):
    model = GameState()
    i = 0
    while True:
        # Translate low level events to domain events
        msgs = []
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                msgs.append(ColumnWasClicked(i))
                i += 1
            elif ev.key == pygame.K_q:
                break
        elif ev.type == pygame.QUIT:
            break

        # Handle events to update state
        model = run_messages(model, msgs)

        # Display current model
        view(model, screen)

        pygame.display.update()


def run_messages(model, msgs):
    for msg in msgs:
        model = update(model, msg)
    return model


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Four in a row")
    clock = pygame.time.Clock()
    font_name = pygame.font.match_font('arial')
    mainloop(screen)
    pygame.quit()
