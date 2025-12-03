import pygame
import glm

from src.utils import mouse_pos
from src.settings import WINDOW_DIMS, DIMS


def draw(state, graphics):
    graphics.render_surface.fill((0, 0, 0))

    mpos = mouse_pos()

    grid_pos = glm.vec2(0, 0)
    grid_size = DIMS / 2
    draw_grid_and_nn(state, graphics, grid_pos, grid_size)

    # just draw a circle on the mouse
    pygame.draw.circle(graphics.render_surface, (0, 255, 0), mpos, 2)
    draw_grid_coords_under_mouse(state, graphics, grid_pos, grid_size, mpos)

    stretched_surface = pygame.transform.scale(graphics.render_surface, WINDOW_DIMS)
    graphics.window.blit(stretched_surface, (0, 0))
    pygame.display.update()


# should take in pos, and size
def draw_grid_and_nn(state, graphics, pos: glm.vec2, size: glm.vec2):
    draw_grid(state, graphics, pos, size)
    draw_neurons(state, graphics, pos, size)


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
        pygame.draw.line(
            graphics.render_surface,
            OUTPUT_HUB_COLOR,
            as_int_tuple(neuron_pos),
            as_int_tuple(output_hub_vec),
            1,
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
