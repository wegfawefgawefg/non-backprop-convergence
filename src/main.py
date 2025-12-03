import pygame
import glm

from src.graphics import Graphics
from src.state import State
from src.brain import init_brain
from src.data import init_target_distribution
from src.step import step_state
from src.utils import mouse_pos
from src.settings import DIMS, SQUARE_SIZE_HEIGHT_FRAC
from src.draw import draw
from src.settings import SIMULATION_FPS, SIM_DT, RENDER_FPS, RENDER_INTERVAL


pygame.init()


def main():
    state = State()
    graphics = Graphics()

    square_px = int(DIMS.y * SQUARE_SIZE_HEIGHT_FRAC)
    dist_size = (square_px, square_px)
    init_target_distribution(state, graphics, size=dist_size, seed=7, nodes=2)
    init_brain(state)

    running = True
    accumulator = 0.0
    last_time = pygame.time.get_ticks() / 1000.0
    last_render_time = 0.0
    displayed_fps = 0.0
    sim_rate = SIMULATION_FPS
    sim_measure_start = last_time
    sim_steps = 0

    while running:
        current_time = pygame.time.get_ticks() / 1000.0
        frame_time = current_time - last_time
        last_time = current_time
        accumulator += frame_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN
                and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q)
            ):
                running = False

        while accumulator >= SIM_DT:
            step_state(state, SIM_DT)
            accumulator -= SIM_DT
            sim_steps += 1

        if current_time - sim_measure_start >= 0.5:
            elapsed = current_time - sim_measure_start
            if elapsed > 0:
                sim_rate = sim_steps / elapsed
            sim_steps = 0
            sim_measure_start = current_time

        if current_time - last_render_time >= RENDER_INTERVAL:
            graphics.clock.tick()
            displayed_fps = graphics.clock.get_fps()
            draw(
                state,
                graphics,
                fps=displayed_fps,
                fps_target=RENDER_FPS,
                sim_rate=sim_rate,
                sim_target=SIMULATION_FPS,
            )
            last_render_time = current_time

    pygame.quit()


if __name__ == "__main__":
    main()
