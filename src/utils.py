import pygame
import glm

from src.settings import DIMS, WINDOW_DIMS
from src.settings import GRID_SIZE


def mouse_pos():
    return glm.vec2(pygame.mouse.get_pos()) / WINDOW_DIMS * DIMS


def clamp_to_grid(point: glm.ivec2) -> glm.ivec2:
    lower = 0
    upper = GRID_SIZE - 1
    return glm.ivec2(
        max(lower, min(upper, point.x)),
        max(lower, min(upper, point.y)),
    )
