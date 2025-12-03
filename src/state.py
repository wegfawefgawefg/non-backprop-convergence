import random
from typing import Tuple

import glm
import numpy as np
import pygame

from src.brain import Input, Neuron, Output


class State:
    def __init__(self):
        self.step_count = 0
        self.time = 0.0

        self.neurons = []
        self.env = None
        self.loss = 0.0
        self.target_distribution = None
        self.target_distribution_surface: pygame.Surface | None = None

        self.input_pos_lookup: dict[Tuple[int, int], list[Input]] = {}
        self.output_pos_lookup: dict[Tuple[int, int], list[Output]] = {}


# make non method versions
def move_input(state: State, input: Input, new_pos: glm.ivec2):
    old_key = (input.pos.x, input.pos.y)
    new_key = (new_pos.x, new_pos.y)

    if old_key in state.input_pos_lookup:
        state.input_pos_lookup[old_key].remove(input)
        if not state.input_pos_lookup[old_key]:
            del state.input_pos_lookup[old_key]

    input.pos = new_pos

    if new_key not in state.input_pos_lookup:
        state.input_pos_lookup[new_key] = []
    state.input_pos_lookup[new_key].append(input)


def move_output(state: State, output: Output, new_pos: glm.ivec2):
    old_key = (output.pos.x, output.pos.y)
    new_key = (new_pos.x, new_pos.y)

    if old_key in state.output_pos_lookup:
        state.output_pos_lookup[old_key].remove(output)
        if not state.output_pos_lookup[old_key]:
            del state.output_pos_lookup[old_key]

    output.x = new_pos.x
    output.y = new_pos.y

    if new_key not in state.output_pos_lookup:
        state.output_pos_lookup[new_key] = []
    state.output_pos_lookup[new_key].append(output)
