from src.constants import (CENTER, WIDTH, HEIGHT, Color, CENTER_X, CENTER_Y, DISC_DIAMETER, \
                           BOARD_LEFT, BOARD_RIGHT, DISC_RADIUS, BOARD_HEIGHT, DROP_DELAY_MS, COLUMNS, ROWS, EMPTY, RED)
from src.states import StartScreenState, GameState, GameOverState
from src.update import convert_to_column, positions_in_print_order, int_to_color_name


def view(model, drawing_api):
    clear_screen(drawing_api)
    if isinstance(model, StartScreenState):
        view_startscreenstate(model, drawing_api)
    if isinstance(model, GameState):
        view_gamestate(drawing_api, model)
    if isinstance(model, GameOverState):
        view_gameoverstate(drawing_api, model)


def view_startscreenstate(model, api):
    api.draw_image(CENTER, 'background', (WIDTH, HEIGHT))
    edged_text(api, "FOUR-IN-A-ROW", CENTER, Color.GREEN)
    edged_text(api, "Click left mouse button to play!",
               (CENTER_X, CENTER_Y + 30),
               Color.YELLOW)
    for i in range(200):
        api.draw_disc((int(model.time / 2 + i ** 2 * 37) % WIDTH, int(model.time + i * 237) % HEIGHT), 1, Color.BLUE)
    for i in range(4):
        bigger_disc = int(DISC_DIAMETER * 0.75)
        api.draw_disc((40 + i * (DISC_DIAMETER + 5), 100), bigger_disc, Color.YELLOW)
        api.draw_disc((WIDTH - 40 - i * (DISC_DIAMETER + 5), HEIGHT - 100), bigger_disc, Color.RED)


def frac(begin, end, current):
    return (float(current) - float(begin)) / (float(end) - float(begin))


assert frac(10, 20, 15) == 0.5
assert frac(10, 20, 10) == 0
assert frac(10, 20, 17.5) == 0.75


def view_gamestate(api, model):
    board = model.board
    draw_board(api, board)
    api.draw_text((WIDTH // 2, 20), f"{int_to_color_name(model.whos_turn_is_it).title()} to place disc", Color.WHITE)
    api.draw_rectangle((BOARD_LEFT, CENTER_Y), (2, 100), Color.GREEN)
    api.draw_rectangle((BOARD_RIGHT, CENTER_Y), (2, 100), Color.GREEN)

    # Player making move?
    if model.mouse_down_time:
        column = convert_to_column(model.mouse_down[0])
        pos = (BOARD_LEFT + DISC_DIAMETER * column + DISC_RADIUS, CENTER_Y - BOARD_HEIGHT // 2 - DISC_RADIUS)
        api.draw_disc(pos, DISC_RADIUS, rgb_from_color(model.whos_turn_is_it))
        # draw holding indicator
        fraction = frac(begin=model.mouse_down_time, end=model.mouse_down_time + DROP_DELAY_MS,
                        current=model.time)  # from, to, current
        api.draw_disc(pos, int(DISC_RADIUS * fraction), Color.GREEN)
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
               (CENTER_X, CENTER_Y - 30),
               Color.WHITE)

    edged_text(api,
               f"{int_to_color_name(model.winner)} won!".upper(),
               ((CENTER_X), (CENTER_Y + 30)),
               rgb_from_color(model.winner))


def edged_text(api, txt, pos, color):
    (x, y) = pos
    api.draw_text(
        (x - 2, y - 2),
        txt,
        Color.WHITE
    )
    api.draw_text(
        (x + 2, y + 2),
        txt,
        Color.BLACK
    )
    api.draw_text(
        (x, y),
        txt,
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
