# objects are in int positions on a grid

import random

import glm
from src.state import State
from src.state import clamp_to_grid


class Input:
    NEXT_ID = 0

    def __init__(self) -> None:
        self.id = Input.NEXT_ID
        Input.NEXT_ID += 1

        self.pos: glm.ivec2 = None
        self.weight: float = None

        self.parent_neuron = None

        self.connected_output = None


class Output:
    NEXT_ID = 0

    def __init__(self) -> None:
        self.id = Output.NEXT_ID
        Output.NEXT_ID += 1

        self.pos: glm.ivec2 = None
        self.weight: float = None

        self.parent_neuron = None
        self.parent_hub = None

        self.connected_input = None


class Neuron:
    """
    Neurons have heads and hubs.
    Heads have inputs.
    Hubs have outputs.
    """

    NUM_NEURONS = 4
    INPUT_MAX_DIST = 4
    OUTPUT_HUB_MAX_DIST = 16
    OUTPUT_MAX_DIST = 4

    NUM_INPUTS = 4
    NUM_OUTPUTS = 4

    NEXT_ID = 0

    def __init__(self) -> None:
        self.id = Neuron.NEXT_ID
        Neuron.NEXT_ID += 1

        self.pos: glm.ivec2 = None
        self.charge: float = None
        self.fire_threshold: float = None
        self.decay_rate: float = None

        self.num_inputs: int = 4
        self.input_max_dist: int = 4
        self.inputs: list[Input] = []

        self.hub_max_dist: int = 16
        self.hub_pos: glm.ivec2 = None

        self.num_outputs: int = 4
        self.output_max_dist: int = 4
        self.outputs: list[Output] = []


def init_brain(state: State):
    """
    neuron pos is on grid
    positions are integer pairs, x, y

    inputs are placed randomly around neuron with max distance constraint
    output hub is placed randomly around neuron with max distance constraint
    outputs are placed randomly around output hub with max distance constraint

    dont worry about setting other settings for now lets just get the positions good
    """

    for _ in range(Neuron.NUM_NEURONS):
        neuron = Neuron()
        neuron.pos = clamp_to_grid(
            (
                random.randint(0, State.GRID_SIZE - 1),
                random.randint(0, State.GRID_SIZE - 1),
            )
        )

        # create inputs
        for _ in range(Neuron.NUM_INPUTS):
            input_pos = glm.ivec2(
                neuron.pos.x
                + random.randint(-Neuron.INPUT_MAX_DIST, Neuron.INPUT_MAX_DIST),
                neuron.pos.y
                + random.randint(-Neuron.INPUT_MAX_DIST, Neuron.INPUT_MAX_DIST),
            )
            neuron.inputs.append(clamp_to_grid(input_pos))

        # create output hub
        output_hub_pos = glm.ivec2(
            neuron.pos.x
            + random.randint(-Neuron.OUTPUT_HUB_MAX_DIST, Neuron.OUTPUT_HUB_MAX_DIST),
            neuron.pos.y
            + random.randint(-Neuron.OUTPUT_HUB_MAX_DIST, Neuron.OUTPUT_HUB_MAX_DIST),
        )
        neuron.hub_pos = clamp_to_grid(output_hub_pos)

        # create outputs
        for _ in range(Neuron.NUM_OUTPUTS):
            output_pos = glm.ivec2(
                output_hub_pos.x
                + random.randint(-Neuron.OUTPUT_MAX_DIST, Neuron.OUTPUT_MAX_DIST),
                output_hub_pos.y
                + random.randint(-Neuron.OUTPUT_MAX_DIST, Neuron.OUTPUT_MAX_DIST),
            )
            neuron.outputs.append(clamp_to_grid(output_pos))

        neuron.charge = random.random()
        neuron.charge_rate = State.NEURON_CHARGE_RATE
        neuron.signal_pos = 0.0
        neuron.signal_active = False

        state.neurons.append(neuron)
