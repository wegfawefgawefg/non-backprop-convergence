import random

import glm

from src.utils import clamp_to_grid
from src.settings import (
    NUM_NEURONS,
    GRID_SIZE,
    NEURON_CHARGE_RATE,
    INPUT_MAX_DIST,
    HUB_MAX_DIST,
    OUTPUT_MAX_DIST,
    NUM_INPUTS,
    NUM_OUTPUTS,
)


class Input:
    NEXT_ID = 0

    def __init__(self) -> None:
        self.id = Input.NEXT_ID
        Input.NEXT_ID += 1

        self.pos: glm.ivec2 = None
        self.weight: float = 0.0

        self.parent_neuron = None

        self.connected_output = None


class Output:
    NEXT_ID = 0

    def __init__(self) -> None:
        self.id = Output.NEXT_ID
        Output.NEXT_ID += 1

        self.pos: glm.ivec2 = None
        self.weight: float = 0.0

        self.parent_neuron = None

        self.connected_input = None


class Neuron:
    """
    Neurons have heads and hubs.
    Heads have inputs.
    Hubs have outputs.
    """

    NEXT_ID = 0

    def __init__(self) -> None:
        self.id = Neuron.NEXT_ID
        Neuron.NEXT_ID += 1

        self.satisfied = False
        self.hub_satisfied = False

        self.pos: glm.ivec2 = None
        self.charge: float = None
        self.fire_threshold: float = None
        self.decay_rate: float = None

        # self.num_inputs: int = 4
        # self.input_max_dist: int = 4
        self.inputs: list[Input] = []

        # self.hub_max_dist: int = 16
        self.hub_pos: glm.ivec2 = None

        # self.num_outputs: int = 4
        # self.output_max_dist: int = 4
        self.outputs: list[Output] = []


def init_brain(state):
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
        neuron.pos = clamp_to_grid(
            glm.ivec2(
                random.randint(0, GRID_SIZE - 1),
                random.randint(0, GRID_SIZE - 1),
            )
        )

        # create inputs
        for _ in range(NUM_INPUTS):
            input_pos = glm.ivec2(
                neuron.pos.x + random.randint(-INPUT_MAX_DIST, INPUT_MAX_DIST),
                neuron.pos.y + random.randint(-INPUT_MAX_DIST, INPUT_MAX_DIST),
            )
            input_pos = clamp_to_grid(
                input_pos,
            )
            new_input = Input()
            new_input.pos = input_pos
            new_input.weight = random.uniform(-1.0, 1.0)
            new_input.parent_neuron = neuron
            neuron.inputs.append(new_input)
            # add to state lookup
            key = (input_pos.x, input_pos.y)
            if key not in state.input_pos_lookup:
                state.input_pos_lookup[key] = []
            state.input_pos_lookup[key].append(new_input)

        # create output hub
        output_hub_pos = glm.ivec2(
            neuron.pos.x + random.randint(-HUB_MAX_DIST, HUB_MAX_DIST),
            neuron.pos.y + random.randint(-HUB_MAX_DIST, HUB_MAX_DIST),
        )
        neuron.hub_pos = clamp_to_grid(
            output_hub_pos,
        )

        # create outputs
        for _ in range(NUM_OUTPUTS):
            output_pos = glm.ivec2(
                output_hub_pos.x + random.randint(-OUTPUT_MAX_DIST, OUTPUT_MAX_DIST),
                output_hub_pos.y + random.randint(-OUTPUT_MAX_DIST, OUTPUT_MAX_DIST),
            )
            output_pos = clamp_to_grid(
                output_pos,
            )
            new_output = Output()
            new_output.pos = output_pos
            new_output.weight = random.uniform(-1.0, 1.0)
            new_output.parent_neuron = neuron
            neuron.outputs.append(new_output)
            key = (output_pos.x, output_pos.y)
            if key not in state.output_pos_lookup:
                state.output_pos_lookup[key] = []
            state.output_pos_lookup[key].append(new_output)

        neuron.charge = random.random()
        neuron.charge_rate = NEURON_CHARGE_RATE
        neuron.signal_pos = 0.0
        neuron.signal_active = False

        state.neurons.append(neuron)
