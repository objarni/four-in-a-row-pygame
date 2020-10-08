from collections import defaultdict, namedtuple
import pygame

# CONSTANTS, Game Logic #
COLUMNS = 7
ROWS = 6
RED, YELLOW, EMPTY = range(3)

# CONSTANTS, Graphics #
WIDTH, HEIGHT = 1100, 800
DISC_DIAMETER = 90
DISC_RADIUS = DISC_DIAMETER // 2
BIG_TEXT = 45
MID_TEXT = 30
CENTER = (WIDTH // 2, HEIGHT // 2)
CENTER_X, CENTER_Y = CENTER
BOARD_WIDTH = DISC_DIAMETER * COLUMNS
BOARD_HEIGHT = DISC_DIAMETER * ROWS
BOARD_LEFT = (WIDTH - BOARD_WIDTH) // 2
BOARD_RIGHT = (WIDTH + BOARD_WIDTH) // 2


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
        self.board = empty_board()
        self.whos_turn_is_it = RED
        self.mouse_pos = CENTER
        self.mouse_down_time = None


def empty_board():
    return defaultdict(lambda: EMPTY)


GameOverState = namedtuple('GameOverState', 'winner board')


class StartScreenState(object):
    def __init__(self):
        self.time = 0


# MESSAGES #

LeftMouseDownAt = namedtuple('LeftMouseDownAt', 'pos')
LeftMouseUpAt = namedtuple('LeftMouseUpAt', 'pos')
ColumnWasClicked = namedtuple('ColumnWasClicked', 'column')
MouseMovedTo = namedtuple('MouseMovedTo', 'pos')
Tick = namedtuple('Tick', 'time')


# FUNCTIONS #

def update(model, msg):
    if isinstance(model, StartScreenState):
        if isinstance(msg, LeftMouseDownAt):
            return GameState()
        if isinstance(msg, Tick):
            model.time = msg.time
            return model
    if isinstance(model, GameState):
        if isinstance(msg, MouseMovedTo):
            model.mouse_pos = msg.pos
        if isinstance(msg, LeftMouseDownAt):
            return update(model, ColumnWasClicked(convert_to_column(msg.pos[0])))
        if isinstance(msg, ColumnWasClicked):
            model.board = place_brick(model.board, model.whos_turn_is_it, msg.column)
            model.whos_turn_is_it = (model.whos_turn_is_it + 1) % 2
            for color in [RED, YELLOW]:
                won = check_winning_state(model.board, color)
                if won:
                    return GameOverState(winner=color, board=model.board)
    if isinstance(model, GameOverState):
        if isinstance(msg, LeftMouseDownAt):
            return StartScreenState()

    return model


def place_brick(board, color, column):
    log(f"Placing brick color {print_color(color)} in column {column}")
    for i in range(ROWS):
        y = ROWS - i - 1
        if board[(column, y)] == EMPTY:
            board[(column, y)] = color
            log("Board state is now:")
            log(board_to_string(board))
            break
    return board


def board_to_string(board):
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


def print_color(color):
    return 'red' if color == RED else 'yellow'


def check_winning_state(board, color):
    for (x, y) in positions_in_print_order():
        for dir in [(0, 1), (1, 0), (1, 1), (-1, 1)]:
            cells = extract(board, (x, y), dir)
            if all(cell == color for cell in cells):
                log(f"Found 4-in-a-row at {x, y} dir {dir}")
                return True
    return False


def extract(board, pos, dir):
    cells = []
    for i in range(4):
        p = (pos[0] + dir[0] * i, pos[1] + dir[1] * i)
        cells.append(board[p])
    return cells


def positions_in_print_order():
    for y in range(ROWS):
        for x in range(COLUMNS):
            yield (x, y)


def view(model, api):
    clear_screen(api)
    if isinstance(model, StartScreenState):
        view_startscreenstate(api, model)
    if isinstance(model, GameState):
        view_gamestate(api, model)
    if isinstance(model, GameOverState):
        view_gameoverstate(api, model)


def view_startscreenstate(api, model):
    api.draw_image(CENTER, 'bg', (WIDTH, HEIGHT))
    edged_text(api, "FOUR-IN-A-ROW", CENTER, BIG_TEXT, Color.GREEN)
    edged_text(api, "Click left mouse button to play!",
               (CENTER_X, CENTER_Y + BIG_TEXT),
               BIG_TEXT,
               Color.YELLOW)
    for i in range(200):
        api.draw_disc((int(model.time / 2 + i ** 2 * 37) % WIDTH, int(model.time + i * 237) % HEIGHT), 1, Color.BLUE)
    for i in range(4):
        bigger_disc = int(DISC_DIAMETER * 0.75)
        api.draw_disc((40 + i * (DISC_DIAMETER + 5), 100), bigger_disc, Color.YELLOW)
        api.draw_disc((WIDTH - 40 - i * (DISC_DIAMETER + 5), HEIGHT - 100), bigger_disc, Color.RED)


def convert_to_column(x):
    if x < BOARD_LEFT:
        return None
    if x > BOARD_RIGHT:
        return None
    return (x - BOARD_LEFT) // DISC_DIAMETER


def frac(begin, end, current):
    return float(current) / (float(end) - float(begin))


assert frac(0, 10, 5) == 0.5
assert frac(0, 10, 0) == 0
assert frac(0, 10, 7.5) == 0.75


def view_gamestate(api, model):
    board = model.board
    draw_board(api, board)
    api.draw_text((WIDTH // 2, 20), f"{print_color(model.whos_turn_is_it).title()} to place disc", MID_TEXT,
                  Color.WHITE)
    api.draw_rectangle((BOARD_LEFT, CENTER_Y), (2, 100), Color.GREEN)
    api.draw_rectangle((BOARD_RIGHT, CENTER_Y), (2, 100), Color.GREEN)

    # Player making move?
    if model.mouse_down_time:
        column = convert_to_column(model.mouse_down)
        pos = (BOARD_LEFT + DISC_DIAMETER * column + DISC_RADIUS, CENTER_Y - BOARD_HEIGHT // 2 - DISC_RADIUS)
        api.draw_disc(pos, DISC_RADIUS, rgb_from_color(model.whos_turn_is_it))
        # draw holding indicator
        fraction = frac(begin=model.mouse_down_time, end=model.mouse_down_time + 1000,
                        current=model.time)  # from, to, current
        api.draw_disc(pos, DISC_RADIUS * fraction, Color.GREEN)
    else:
        column = convert_to_column(model.mouse_pos[0])
        if column is not None:
            pos = (BOARD_LEFT + DISC_DIAMETER * column + DISC_RADIUS, CENTER_Y - BOARD_HEIGHT // 2 - DISC_RADIUS)
            api.draw_disc(pos, DISC_RADIUS, rgb_from_color(model.whos_turn_is_it))
        else:
            api.draw_disc(model.mouse_pos, DISC_RADIUS, rgb_from_color(model.whos_turn_is_it))


def view_gameoverstate(api, model):
    draw_board(api, model.board, scale=1.0)

    edged_text(api,
               "GAME OVER",
               (CENTER_X, CENTER_Y - BIG_TEXT), BIG_TEXT,
               Color.WHITE)

    edged_text(api,
               f"{print_color(model.winner)} won!".upper(),
               ((CENTER_X), (CENTER_Y + BIG_TEXT)), BIG_TEXT,
               rgb_from_color(model.winner))


# PyGame drawing wrapper
class DrawingAPI:
    def __init__(self, screen):
        self.screen = screen
        self.font_name = pygame.font.match_font('arial')
        self.image_dict = {}

    def draw_rectangle(self, center, size, color):
        log(f"Drawing rectangle center {center} size {size} color {color}")
        r = pygame.Rect(0, 0, *size)
        r.center = center
        pygame.draw.rect(self.screen, color, r)

    def draw_disc(self, center, size, color):
        log(f'Drawing a disc center {center} size {size} color {color}')
        pygame.draw.circle(self.screen, color, center, size, size)

    def draw_text(self, center, text, size, color):
        log(f"Drawing text '{text}' at {center} color {color} size {size}")
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = center
        self.screen.blit(text_surface, text_rect)

    def draw_image(self, center, name, dimension):
        if (name, dimension) not in self.image_dict:
            self.image_dict[(name, dimension)] = self.load_and_scale(name, dimension)
        image = self.image_dict[(name, dimension)]
        pos = center[0] - WIDTH // 2, center[1] - HEIGHT // 2
        self.screen.blit(image, pos)

    def load_and_scale(self, name, dimension):
        p = f'res/{name}.png'
        image = pygame.image.load(p)
        return pygame.transform.scale(image, dimension)


def edged_text(api, txt, pos, size, color):
    (x, y) = pos
    api.draw_text(
        (x - 2, y - 2),
        txt,
        size,
        Color.WHITE
    )
    api.draw_text(
        (x + 2, y + 2),
        txt,
        size,
        Color.BLACK
    )
    api.draw_text(
        (x, y),
        txt,
        size,
        color
    )


def clear_screen(api):
    api.draw_rectangle(CENTER, (WIDTH, HEIGHT), Color.BLACK)


def draw_board(api, board, scale=1.0):
    api.draw_rectangle(CENTER, (DISC_DIAMETER * COLUMNS + 20, DISC_DIAMETER * ROWS + 20), Color.BLUE)
    for (x, y) in positions_in_print_order():
        value = board[(x, y)]
        color = Color.BLACK
        if value != EMPTY:
            color = rgb_from_color(value)
        x0 = int((WIDTH / 2 - COLUMNS * DISC_DIAMETER / 2 + x * DISC_DIAMETER + DISC_RADIUS))
        y0 = int((HEIGHT / 2 - ROWS * DISC_DIAMETER / 2 + y * DISC_DIAMETER + DISC_RADIUS))
        api.draw_disc((x0, y0), int(scale * DISC_RADIUS), color)


def rgb_from_color(color):
    return Color.RED if color == RED else Color.YELLOW


# MAIN PROGRAM #


def log(msg):
    pass
    # print(msg)


def print_model(model):
    state_string = model.__class__.__name__ + '\n'
    if isinstance(model, StartScreenState):
        state_string += f'{model.time=}'
    if isinstance(model, GameOverState):
        state_string += f'{print_color(model.winner).title()} won.\n'
    if isinstance(model, GameState):
        state_string += f'It is {print_color(model.whos_turn_is_it)}s turn.\n'
        state_string += f'The mouse is at {model.mouse_pos}.\n'
        state_string += board_to_string(model.board)
    return state_string


def mainloop(drawing_api):
    model = StartScreenState()
    view(model, drawing_api)
    pygame.display.update()
    clock = pygame.time.Clock()
    FPS = 60
    while True:
        old_model_repr = print_model(model)

        # A tick happens every time around the loop!
        model = update(model, Tick(pygame.time.get_ticks()))

        # Translate low level events to domain events
        while ev := pygame.event.poll():
            msg = None
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    msg = LeftMouseDownAt(ev.pos)
            if ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1:
                    msg = LeftMouseUpAt(ev.pos)
            if ev.type == pygame.MOUSEMOTION:
                msg = MouseMovedTo(ev.pos)
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_q:
                    return
            elif ev.type == pygame.QUIT:
                return

            if msg:
                model = update(model, msg)

        # pygame.time.wait(5)

        # Display current model, if any change found
        if old_model_repr != print_model(model):
            view(model, api)

        pygame.display.update()
        clock.tick(FPS)


def main():
    global api
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Four in a row")
    api = DrawingAPI(screen)
    mainloop(api)
    pygame.quit()


if __name__ == '__main__':
    main()
