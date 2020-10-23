import pygame

from src.messages import LeftMouseDownAt, LeftMouseUpAt, MouseMovedTo, Tick
from src.states import StartScreenState, GameOverState, GameState
from src.constants import WIDTH, HEIGHT, FPS, EMPTY, RED, YELLOW, ROWS, COLUMNS

from src.update import update, print_color
from src.view import view


def main():
    global api
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Four in a row")
    resource_folder = 'res'
    drawing_api = DrawingAPI(screen, resource_folder)
    audio_api = AudioAPI(resource_folder)
    mainloop(drawing_api, audio_api)
    pygame.quit()


def mainloop(drawing_api, audio_api):
    model = StartScreenState()
    view(model, drawing_api)
    pygame.display.update()
    clock = pygame.time.Clock()
    while True:
        old_model_repr = project_model(model)

        # A tick happens every time around the loop!
        model = update(model, Tick(pygame.time.get_ticks()), audio_api)

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
                model = update(model, msg, audio_api)

        # Display current model, if any change found
        if old_model_repr != project_model(model):
            view(model, drawing_api)

        pygame.display.update()
        clock.tick(FPS)


class DrawingAPI:
    def __init__(self, screen, resource_path):
        self.screen = screen
        self.image_dict = {}
        self.resource_path = resource_path
        self.font = pygame.font.Font(f'{self.resource_path}/font.ttf', 30)

    def draw_rectangle(self, center, size, color):
        r = pygame.Rect(0, 0, *size)
        r.center = center
        pygame.draw.rect(self.screen, color, r)

    def draw_disc(self, center, size, color):
        pygame.draw.circle(self.screen, color, center, size, size)

    def draw_text(self, center, text, color):
        text_surface = self.font.render(text, True, color)
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
        p = f'{self.resource_path}/{name}.png'
        image = pygame.image.load(p)
        return pygame.transform.scale(image, dimension)


class AudioAPI:
    def __init__(self, resource_path):
        self.resource_path = resource_path
        self.sound = {}

    def play_music(self, name):
        p = f'{self.resource_path}/{name}.ogg'
        pygame.mixer.music.load(p)
        pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_sound(self, name):
        if name not in self.sound:
            p = f'{self.resource_path}/{name}.wav'
            self.sound[name] = pygame.mixer.Sound(p)
        self.sound[name].play()


if __name__ == '__main__':
    main()

# TODO: all states as named tuples instead of classes and initial_GameState function
# TODO: refactor to many states instead of 'mixed in' states
# TODO: little man easter egg
# TODO: remove old_model_repr logic (animations on every screen so was premature optimization after all, but fun exp!)
# TODO: ALSA blocks mixer init. Can it be solved without resorting to 'catch exception / null audio api'?
# TODO: idea to reduce missing updating projectors with new state:
#         investigate using nametuple string representation in projectors
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