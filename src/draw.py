import pygame
import glm

from src.utils import mouse_pos
from src.settings import (
    WINDOW_DIMS,
    DIMS,
    LEFT_PADDING_FRAC_X,
    TOP_PADDING_FRAC_Y,
    SQUARE_SIZE_HEIGHT_FRAC,
    VERTICAL_GAP_FRAC_Y,
)


def draw(
    state,
    graphics,
    fps: float = 0.0,
    fps_target: float = 0.0,
    sim_rate: float = 0.0,
    sim_target: float = 0.0,
):
    graphics.render_surface.fill((0, 0, 0))

    mpos = mouse_pos()

    left_pad = DIMS.x * LEFT_PADDING_FRAC_X
    top_pad = DIMS.y * TOP_PADDING_FRAC_Y
    square_size = DIMS.y * SQUARE_SIZE_HEIGHT_FRAC

    grid_pos = glm.vec2(left_pad, top_pad)
    grid_size = glm.vec2(square_size, square_size)
    draw_grid_and_nn(state, graphics, grid_pos, grid_size)

    # just draw a circle on the mouse
    pygame.draw.circle(graphics.render_surface, (0, 255, 0), mpos, 2)
    draw_grid_coords_under_mouse(state, graphics, grid_pos, grid_size, mpos)

    dist_top = grid_pos.y + grid_size.y + DIMS.y * VERTICAL_GAP_FRAC_Y
    dist_pos = glm.vec2(left_pad, dist_top)
    dist_size = glm.vec2(square_size, square_size)
    draw_target_distribution(state, graphics, dist_pos, dist_size)

    draw_perf_stats(graphics, fps, fps_target, sim_rate, sim_target)

    # lets put it on the right 40% of the screen, from top to bottom
    stats_pos = glm.vec2(DIMS.x * 0.6, 0)
    stats_size = glm.vec2(DIMS.x * 0.4, DIMS.y)
    draw_stats(state, graphics, stats_pos, stats_size)

    stretched_surface = pygame.transform.scale(graphics.render_surface, WINDOW_DIMS)
    graphics.window.blit(stretched_surface, (0, 0))
    pygame.display.update()


# should take in pos, and size
def draw_grid_and_nn(state, graphics, pos: glm.vec2, size: glm.vec2):
    draw_grid(state, graphics, pos, size)
    draw_neurons(state, graphics, pos, size)


def draw_stats(state, graphics, pos, size):
    # for now just a box
    BOX_COLOR = (30, 30, 30)
    pygame.draw.rect(
        graphics.render_surface,
        BOX_COLOR,
        (int(round(pos.x)), int(round(pos.y)), int(round(size.x)), int(round(size.y))),
    )


def draw_target_distribution(state, graphics, pos: glm.vec2, size: glm.vec2):
    surface = state.target_distribution_surface
    if surface is None:
        return

    dest_rect = pygame.Rect(
        int(round(pos.x)),
        int(round(pos.y)),
        int(round(size.x)),
        int(round(size.y)),
    )

    blit_surface = surface
    if surface.get_size() != (dest_rect.width, dest_rect.height):
        blit_surface = pygame.transform.smoothscale(surface, dest_rect.size)

    graphics.render_surface.blit(blit_surface, dest_rect.topleft)
    pygame.draw.rect(graphics.render_surface, (80, 80, 80), dest_rect, 1)


def draw_grid_coords_under_mouse(
    state,
    graphics,
    grid_pos: glm.vec2,
    grid_size: glm.vec2,
    pos: glm.vec2,
):
    mouse = mouse_pos()
    col = "-"
    row = "-"
    cell = glm.vec2(
        grid_size.x / state.GRID_SIZE if state.GRID_SIZE else 0,
        grid_size.y / state.GRID_SIZE if state.GRID_SIZE else 0,
    )

    within_x = grid_pos.x <= mouse.x < grid_pos.x + grid_size.x
    within_y = grid_pos.y <= mouse.y < grid_pos.y + grid_size.y
    if within_x and within_y and cell.x and cell.y:
        col = int((mouse.x - grid_pos.x) / cell.x)
        row = int((mouse.y - grid_pos.y) / cell.y)

    # draw the text in the top right corner
    font = pygame.font.Font(None, 16)
    text = font.render(f"({col}, {row})", True, (255, 255, 255))
    # put it at pos
    graphics.render_surface.blit(text, (pos.x, pos.y))


def draw_perf_stats(graphics, fps, fps_target, sim_rate, sim_target):
    def fmt_line(label, current, target):
        percent = 0.0
        if target:
            percent = (current / target) * 100.0
        return f"{label}: {current:6.1f} / {target:6.1f} ({percent:5.1f}%)"

    lines = [
        fmt_line("SIM", sim_rate, sim_target),
        fmt_line("FPS", fps, fps_target),
    ]

    y = 2
    for line in lines:
        text_surface = graphics.font.render(line, True, (255, 255, 255))
        graphics.render_surface.blit(text_surface, (2, y))
        y += text_surface.get_height() + 2


def draw_grid(state, graphics, pos: glm.vec2, size: glm.vec2):
    GRID_COLOR = (50, 50, 50)
    GRID_WIDTH = 1
    cell_x = size.x / state.GRID_SIZE
    cell_y = size.y / state.GRID_SIZE

    for i in range(state.GRID_SIZE + 1):
        x = int(round(pos.x + i * cell_x))
        pygame.draw.line(
            graphics.render_surface,
            GRID_COLOR,
            (x, int(round(pos.y))),
            (x, int(round(pos.y + size.y))),
            GRID_WIDTH,
        )
    for j in range(state.GRID_SIZE + 1):
        y = int(round(pos.y + j * cell_y))
        pygame.draw.line(
            graphics.render_surface,
            GRID_COLOR,
            (int(round(pos.x)), y),
            (int(round(pos.x + size.x)), y),
            GRID_WIDTH,
        )


def draw_neurons(state, graphics, pos: glm.vec2, size: glm.vec2):
    """
    draw neuron position as a blue circle
    draw neuron inputs as blue lines out from neuron position
    draw output hub as line from neuron position to output hub position
    draw outputs as lines from output hub position to output positions
    """

    NEURON_COLOR = (0, 0, 255)
    NEURON_RADIUS = 2

    INPUT_COLOR = (0, 0, 200)
    OUTPUT_HUB_COLOR = (0, 200, 0)
    OUTPUT_COLOR = (200, 0, 0)
    SIGNAL_COLOR = (100, 255, 100)

    cell = glm.vec2(size.x / state.GRID_SIZE, size.y / state.GRID_SIZE)

    def to_surface_center(grid_point):
        return glm.vec2(
            pos.x + (grid_point[0] + 0.5) * cell.x,
            pos.y + (grid_point[1] + 0.5) * cell.y,
        )

    def as_int_tuple(vec: glm.vec2) -> tuple[int, int]:
        return int(round(vec.x)), int(round(vec.y))

    for neuron in state.neurons:
        neuron_pos = to_surface_center(neuron.position)

        # draw inputs
        for input_pos in neuron.inputs:
            input_vec = to_surface_center(input_pos)
            pygame.draw.line(
                graphics.render_surface,
                INPUT_COLOR,
                as_int_tuple(neuron_pos),
                as_int_tuple(input_vec),
                1,
            )

        # draw output hub
        output_hub_vec = to_surface_center(neuron.output_hub_pos)
        neuron_screen = as_int_tuple(neuron_pos)
        hub_screen = as_int_tuple(output_hub_vec)
        pygame.draw.line(
            graphics.render_surface,
            OUTPUT_HUB_COLOR,
            neuron_screen,
            hub_screen,
            1,
        )

        if neuron.signal_active and neuron.signal_pos > 0.0:
            progress = min(1.0, neuron.signal_pos)
            signal_point = neuron_pos + (output_hub_vec - neuron_pos) * progress
            pygame.draw.line(
                graphics.render_surface,
                SIGNAL_COLOR,
                neuron_screen,
                as_int_tuple(signal_point),
                2,
            )

        # draw outputs
        for output_pos in neuron.outputs:
            output_vec = to_surface_center(output_pos)
            pygame.draw.line(
                graphics.render_surface,
                OUTPUT_COLOR,
                as_int_tuple(output_hub_vec),
                as_int_tuple(output_vec),
                1,
            )

        # draw neuron position
        pygame.draw.circle(
            graphics.render_surface,
            NEURON_COLOR,
            as_int_tuple(neuron_pos),
            NEURON_RADIUS,
        )


def draw_demo(surface):
    angle = pygame.time.get_ticks() / 1000

    rect_size = glm.vec2(16, 16)
    center = DIMS / 2
    rect_pos = center - rect_size / 2 + glm.vec2(32, 32)

    for i in range(3):
        rot = glm.rotate(glm.vec2(0.0, 1.0), angle + i * 90)
        rect_pos_rotated = rot @ (rect_pos - center) + rect_pos
        pygame.draw.rect(
            surface, (255, 0, 0), (rect_pos_rotated.to_tuple(), rect_size.to_tuple())
        )

    pygame.draw.circle(surface, (0, 255, 0), mouse_pos(), 10)
