import pygame

from src.messages import LeftMouseDownAt, LeftMouseUpAt, MouseMovedTo, Tick
from src.states import StartScreenState
from src.constants import WIDTH, HEIGHT, FPS

from src.update import update
from src.view import view

# PyGame drawing wrapper
from tests.test_four_in_a_row import project_model


class DrawingAPI:
    def __init__(self, screen, resource_path):
        self.screen = screen
        self.font_name = pygame.font.match_font('arial')
        self.image_dict = {}
        self.resource_path = resource_path

    def draw_rectangle(self, center, size, color):
        r = pygame.Rect(0, 0, *size)
        r.center = center
        pygame.draw.rect(self.screen, color, r)

    def draw_disc(self, center, size, color):
        pygame.draw.circle(self.screen, color, center, size, size)

    def draw_text(self, center, text, size, color):
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
        p = f'{self.resource_path}/{name}.png'
        image = pygame.image.load(p)
        return pygame.transform.scale(image, dimension)


# MAIN PROGRAM #


def mainloop(drawing_api):
    model = StartScreenState()
    view(model, drawing_api)
    pygame.display.update()
    clock = pygame.time.Clock()
    while True:
        old_model_repr = project_model(model)

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

        # Display current model, if any change found
        if old_model_repr != project_model(model):
            view(model, api)

        pygame.display.update()
        clock.tick(FPS)


def main():
    global api
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Four in a row")
    api = DrawingAPI(screen, 'res')
    mainloop(api)
    pygame.quit()


if __name__ == '__main__':
    main()

#     pygame.mixer.music.stop()
#     pygame.mixer.init()
#     pygame.mixer.music.load('res/music.ogg')
#     pygame.mixer.music.play()
# TODO: approval tested music playback
# TODO: all states as named tuples instead of classes and initial_GameState function
# TODO: refactor to many states instead of 'mixed in' states
# TODO: sfx
# TODO: little man easter egg
