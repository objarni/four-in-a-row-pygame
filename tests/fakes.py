import pygame

import src.constants
import src.four_in_a_row
import src.update
from src.printers import print_model


class FakeDrawingAPI:
    def __init__(self, log):
        self.log = log
        self.surface = pygame.Surface(src.constants.SCREENDIM)
        self.real_api = src.four_in_a_row.DrawingAPI(self.surface, '../res')

    def draw_rectangle(self, center, size, color):
        self.real_api.draw_rectangle(center, size, color)

    def draw_disc(self, center, size, color):
        self.real_api.draw_disc(center, size, color)

    def draw_text(self, center, text, color):
        self.real_api.draw_text(center, text, color)

    def draw_image(self, center, name, dimension):
        self.real_api.draw_image(center, name, dimension)


class FakeAudioAPI:
    def __init__(self, log):
        self.log = log

    def play_music(self, name):
        self.log += f"Starting music {name}.\n"

    def stop_music(self):
        self.log += f"Stopping music playback.\n"

    def play_sound(self, name):
        self.log += f"Playing sound {name}.\n"


def simulate_main_event_loop(model, messages, log):
    # Mimics behaviour of main event loop in four_in_a_row
    fake_drawing = FakeDrawingAPI(log)
    fake_audio = FakeAudioAPI(log)
    log += f"[SIMULATION STARTING]\n"
    log += f"===Model state===\n"
    log += f"{print_model(model)}\n\n\n"
    for msg in messages:
        log += f"[SIMULATING MSG={msg}]\n\n"
        model = src.update.update(model, msg, fake_audio)
        log += f"===Model state===\n"
        log += f"{print_model(model)}\n\n\n"
    log += f"[SIMULATION ENDED]"

    src.view.view(model, fake_drawing)
    return (model, fake_drawing.surface)