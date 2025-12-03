import random
from typing import Tuple

import numpy as np
import pygame

from src.brain import Neuron


class State:
    GRID_SIZE = 16
    NEURON_CHARGE_RATE = 0.2  # charge per second
    SIGNAL_SPEED = 4.0  # normalized units per second

    def __init__(self):
        self.step_count = 0
        self.time = 0.0

        self.neurons = []
        self.env = None
        self.loss = 0.0
        self.target_distribution = None
        self.target_distribution_surface: pygame.Surface | None = None


def clamp_to_grid(point: tuple[int, int]) -> tuple[int, int]:
    lower = 0
    upper = State.GRID_SIZE - 1
    return (
        max(lower, min(upper, point[0])),
        max(lower, min(upper, point[1])),
    )


def init_brain(state):
    NUM_NEURONS = 4
    INPUT_MAX_DIST = 4
    OUTPUT_HUB_MAX_DIST = 16
    OUTPUT_MAX_DIST = 4

    NUM_INPUTS = 4
    NUM_OUTPUTS = 4

    """
    neuron pos is on grid
    positions are integer pairs, x, y

    inputs are placed randomly around neuron with max distance constraint
    output hub is placed randomly around neuron with max distance constraint
    outputs are placed randomly around output hub with max distance constraint

    dont worry about setting other settings for now lets just get the positions good
    """

    for _ in range(NUM_NEURONS):
        neuron = Neuron()
        neuron.position = clamp_to_grid(
            (
                random.randint(0, State.GRID_SIZE - 1),
                random.randint(0, State.GRID_SIZE - 1),
            )
        )

        # create inputs
        for _ in range(NUM_INPUTS):
            input_pos = (
                neuron.position[0] + random.randint(-INPUT_MAX_DIST, INPUT_MAX_DIST),
                neuron.position[1] + random.randint(-INPUT_MAX_DIST, INPUT_MAX_DIST),
            )
            neuron.inputs.append(clamp_to_grid(input_pos))

        # create output hub
        output_hub_pos = (
            neuron.position[0]
            + random.randint(-OUTPUT_HUB_MAX_DIST, OUTPUT_HUB_MAX_DIST),
            neuron.position[1]
            + random.randint(-OUTPUT_HUB_MAX_DIST, OUTPUT_HUB_MAX_DIST),
        )
        neuron.output_hub_pos = clamp_to_grid(output_hub_pos)

        # create outputs
        for _ in range(NUM_OUTPUTS):
            output_pos = (
                output_hub_pos[0] + random.randint(-OUTPUT_MAX_DIST, OUTPUT_MAX_DIST),
                output_hub_pos[1] + random.randint(-OUTPUT_MAX_DIST, OUTPUT_MAX_DIST),
            )
            neuron.outputs.append(clamp_to_grid(output_pos))

        neuron.charge = random.random()
        neuron.charge_rate = State.NEURON_CHARGE_RATE
        neuron.signal_pos = 0.0
        neuron.signal_active = False

        state.neurons.append(neuron)


def init_target_distribution(
    state,
    size: Tuple[int, int],
    seed: int = 7,
    nodes: int = 2,
) -> None:
    """
    Initialize a deterministic 2-D Gaussian mixture distribution and pre-render
    it to a surface for fast blitting.
    """

    width, height = size
    rng = np.random.default_rng(seed)
    centers = rng.uniform(0.2, 0.8, size=(nodes, 2))
    stds = rng.uniform(0.05, 0.15, size=nodes)

    xs = np.linspace(0.0, 1.0, width)
    ys = np.linspace(0.0, 1.0, height)
    grid_x, grid_y = np.meshgrid(xs, ys)

    density = np.zeros((height, width), dtype=np.float32)
    for center, std in zip(centers, stds, strict=False):
        dx = grid_x - center[0]
        dy = grid_y - center[1]
        gaussian = np.exp(-(dx**2 + dy**2) / (2.0 * std**2))
        density += gaussian

    if np.max(density) > 0:
        density /= np.max(density)

    state.target_distribution = density
    state.target_distribution_surface = _distribution_surface_from_density(density)


def _distribution_surface_from_density(density: np.ndarray) -> pygame.Surface:
    normalized = (density * 255).astype(np.uint8)
    grayscale = normalized.T  # pygame expects width x height
    rgb = np.repeat(grayscale[:, :, None], 3, axis=2)
    surface = pygame.surfarray.make_surface(rgb)
    return surface.convert()


def step_state(state, dt: float) -> None:
    """Advance simulation time and bookkeeping."""
    state.step_count += 1
    state.time += dt
    _update_neuron_activity(state.neurons, dt)


def _update_neuron_activity(neurons, dt: float) -> None:
    for neuron in neurons:
        if neuron.signal_active:
            neuron.signal_pos += State.SIGNAL_SPEED * dt
            if neuron.signal_pos >= 1.0:
                neuron.signal_pos = 0.0
                neuron.signal_active = False
        else:
            neuron.charge += neuron.charge_rate * dt
            if neuron.charge >= 1.0:
                neuron.charge = 0.0
                neuron.signal_active = True
                neuron.signal_pos = 0.0
