import pygame
import glm

from src.settings import DIMS, WINDOW_DIMS


def mouse_pos():
    return glm.vec2(pygame.mouse.get_pos()) / WINDOW_DIMS * DIMS
