from collections import defaultdict
import pygame

# CONSTANTS #
DISC_SIZE = 90
RED, YELLOW, EMPTY = range(3)
WIDTH, HEIGHT = 1100, 600
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


class StartScreenState(object):
    pass


# MESSAGES #

class LeftMouseClickAt(object):
    def __init__(self, pos):
        self.pos = pos


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
            won = check_winning_state(model.board, YELLOW)
            if won:
                return GameOverState(winner=YELLOW)
    if isinstance(model, StartScreenState):
        if isinstance(msg, LeftMouseClickAt):
            return GameState()

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
    for y in range(6):
        for x in range(7):
            pos = (x, y)
            cell = board[pos]
            board_string += symbols[cell] + ' '
        board_string += '\n'
    return board_string


def print_color(color):
    return 'red' if color == RED else 'yellow'


def check_winning_state(board, color):
    for (x, y) in all_positions():
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


def all_positions():
    for y in range(ROWS):
        for x in range(COLUMNS):
            yield (x, y)


# PyGame drawing wrapper
class DrawingAPI:
    def __init__(self, screen):
        self.screen = screen
        self.font_name = pygame.font.match_font('arial')

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


def view(model, api):
    if isinstance(model, GameState):
        api.draw_rectangle(CENTER, (WIDTH, HEIGHT), Color.BLACK)
        api.draw_rectangle(CENTER, (DISC_SIZE * COLUMNS + 20, DISC_SIZE * ROWS + 20), Color.BLUE)
        for (x, y) in all_positions():
            value = model.board[(x, y)]
            color = Color.BLACK
            if value != EMPTY:
                color = rgb_from_color(value)
            x0 = int(WIDTH / 2 - COLUMNS * DISC_SIZE / 2 + x * DISC_SIZE + DISC_SIZE // 2)
            y0 = int(HEIGHT / 2 - ROWS * DISC_SIZE / 2 + y * DISC_SIZE + DISC_SIZE // 2)
            pos = (x0, y0)
            api.draw_disc(pos, DISC_SIZE // 2, color)
        api.draw_text((WIDTH // 2, 20), f"{model.whos_turn().title()} to place disc", 30, Color.WHITE)
    if isinstance(model, GameOverState):
        api.draw_rectangle(CENTER, (WIDTH, HEIGHT), Color.BLUE)
        api.draw_text((CENTER[0], CENTER[1] - 45), f"GAME OVER", 45, Color.WHITE)
        api.draw_text((CENTER[0], CENTER[1] + 45),
                      f"{print_color(model.winner)} won!".upper(),
                      45,
                      rgb_from_color(model.winner)
                      )
    if isinstance(model, StartScreenState):
        api.draw_rectangle(CENTER, (WIDTH, HEIGHT), Color.GREEN)
        api.draw_text((CENTER[0], CENTER[1] - 45), "FOUR-IN-A-ROW", 45, Color.WHITE)
        api.draw_text((CENTER[0], CENTER[1] + 45), "Click left mouse button to play!", 45, Color.WHITE)


def rgb_from_color(color):
    return Color.RED if color == RED else Color.YELLOW


# MAIN PROGRAM #


def log(msg):
    print(msg)


def print_model(model):
    state_string = model.__class__.__name__ + '\n'
    if isinstance(model, StartScreenState):
        pass
    if isinstance(model, GameOverState):
        state_string += f'{print_color(model.winner).title()} won.\n'
    if isinstance(model, GameState):
        state_string += f'It is {model.whos_turn()}s turn.\n'
        state_string += board_to_string(model.board)
    return state_string


def mainloop(drawing_api):
    model = StartScreenState()
    i = 0
    view(model, drawing_api)
    while True:
        # Translate low level events to domain events
        msgs = []
        ev = pygame.event.poll()
        if ev.type == pygame.MOUSEBUTTONDOWN:
            print(f"Got click {ev}")
            pos = ev.pos
            button = ev.button
            if button == 1:
                msgs.append(LeftMouseClickAt(pos))
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                msgs.append(ColumnWasClicked(i % 2))
                i += 1
            elif ev.key == pygame.K_q:
                break
        elif ev.type == pygame.QUIT:
            break

        # Handle events to update state
        old_model_repr = print_model(model)
        model = run_messages(model, msgs)

        # Display current model
        if old_model_repr != print_model(model):
            view(model, api)

        pygame.display.update()


def run_messages(model, msgs):
    for msg in msgs:
        model = update(model, msg)
    return model


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Four in a row")
    api = DrawingAPI(screen)
    mainloop(api)
    pygame.quit()
