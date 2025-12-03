import pygame

from src.settings import WINDOW_DIMS, DIMS


class Graphics:
    def __init__(self):
        self.window = pygame.display.set_mode(WINDOW_DIMS.to_tuple())
        self.render_surface = pygame.Surface(DIMS.to_tuple())
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 18)
