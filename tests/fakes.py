import pygame

import src.constants
import src.four_in_a_row


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