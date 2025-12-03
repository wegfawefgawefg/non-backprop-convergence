import glm
import numpy as np
import pygame

from src.graphics import Graphics
from src.state import State


def distribution_surface_from_density(density: np.ndarray) -> pygame.Surface:
    normalized = (density * 255).astype(np.uint8)
    grayscale = normalized.T  # pygame expects width x height
    rgb = np.repeat(grayscale[:, :, None], 3, axis=2)
    surface = pygame.surfarray.make_surface(rgb)
    return surface.convert()


def init_target_distribution(
    state: State,
    graphics: Graphics,
    size: glm.ivec2,
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
    graphics.target_distribution_surface = distribution_surface_from_density(density)
