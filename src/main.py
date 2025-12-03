import pygame
import glm

from src.graphics import Graphics
from src.state import State, init_brain
from src.utils import mouse_pos
from src.settings import DIMS
from src.draw import draw

pygame.init()


def main():
    state = State()
    graphics = Graphics()

    init_brain(state)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN
                and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)
            ):
                running = False

        # step_nn(state)
        # eval(state)
        draw(state, graphics)

    pygame.quit()


if __name__ == "__main__":
    main()
