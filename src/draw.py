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
    draw_grid_coords_under_mouse(graphics, grid_pos, grid_size, mpos)

    stretched_surface = pygame.transform.scale(graphics.render_surface, WINDOW_DIMS)
    graphics.window.blit(stretched_surface, (0, 0))
    pygame.display.update()


# should take in pos, and size
def draw_grid_and_nn(state, graphics, pos: glm.vec2, size: glm.vec2):
    draw_grid(state, graphics, pos, size)
    draw_neurons(state, graphics, pos, size)


def draw_grid_coords_under_mouse(
    graphics, grid_pos: glm.vec2, grid_size: glm.vec2, pos: glm.vec2
):
    mouse = mouse_pos()
    col = "-"
    row = "-"
    if (
        mouse.x >= grid_pos.x
        and mouse.x < grid_pos.x + grid_size.x
        and mouse.y >= grid_pos.y
        and mouse.y < grid_pos.y + grid_size.y
    ):
        col = int((mouse.x - grid_pos.x) / 10)
        row = int((mouse.y - grid_pos.y) / 10)

    # draw the text in the top right corner
    font = pygame.font.Font(None, 16)
    text = font.render(f"({col}, {row})", True, (255, 255, 255))
    # put it at pos
    graphics.render_surface.blit(text, (pos.x, pos.y))


def draw_grid(state, graphics, pos: glm.vec2, size: glm.vec2):
    GRID_COLOR = (50, 50, 50)
    GRID_WIDTH = 1

    # draw the grid lines
    for x in range(int(pos.x), int(pos.x + size.x) + 1, 10):
        pygame.draw.line(
            graphics.render_surface,
            GRID_COLOR,
            (x, pos.y),
            (x, pos.y + size.y),
            GRID_WIDTH,
        )
    for y in range(int(pos.y), int(pos.y + size.y) + 1, 10):
        pygame.draw.line(
            graphics.render_surface,
            GRID_COLOR,
            (pos.x, y),
            (pos.x + size.x, y),
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

    for neuron in state.neurons:
        neuron_pos = glm.vec2(
            pos.x + neuron.position[0] * 10 + 5, pos.y + neuron.position[1] * 10 + 5
        )

        # draw inputs
        for input_pos in neuron.inputs:
            input_vec = glm.vec2(
                pos.x + input_pos[0] * 10 + 5, pos.y + input_pos[1] * 10 + 5
            )
            pygame.draw.line(
                graphics.render_surface,
                INPUT_COLOR,
                neuron_pos.to_tuple(),
                input_vec.to_tuple(),
                1,
            )

        # draw output hub
        output_hub_vec = glm.vec2(
            pos.x + neuron.output_hub_pos[0] * 10 + 5,
            pos.y + neuron.output_hub_pos[1] * 10 + 5,
        )
        pygame.draw.line(
            graphics.render_surface,
            OUTPUT_HUB_COLOR,
            neuron_pos.to_tuple(),
            output_hub_vec.to_tuple(),
            1,
        )

        # draw outputs
        for output_pos in neuron.outputs:
            output_vec = glm.vec2(
                pos.x + output_pos[0] * 10 + 5, pos.y + output_pos[1] * 10 + 5
            )
            pygame.draw.line(
                graphics.render_surface,
                OUTPUT_COLOR,
                output_hub_vec.to_tuple(),
                output_vec.to_tuple(),
                1,
            )

        # draw neuron position
        pygame.draw.circle(
            graphics.render_surface,
            NEURON_COLOR,
            neuron_pos.to_tuple(),
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
