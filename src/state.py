import random

from src.brain import Neuron


class State:
    GRID_SIZE = 16

    def __init__(self):
        self.step_count = 0
        self.time = 0.0

        self.neurons = []
        self.env = None
        self.loss = 0.0


def init_brain(state):
    NUM_NEURONS = 8
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
        neuron.position = (
            random.randint(0, State.GRID_SIZE - 1),
            random.randint(0, State.GRID_SIZE - 1),
        )

        # create inputs
        for _ in range(NUM_INPUTS):
            input_pos = (
                neuron.position[0] + random.randint(-INPUT_MAX_DIST, INPUT_MAX_DIST),
                neuron.position[1] + random.randint(-INPUT_MAX_DIST, INPUT_MAX_DIST),
            )
            neuron.inputs.append(input_pos)

        # create output hub
        output_hub_pos = (
            neuron.position[0]
            + random.randint(-OUTPUT_HUB_MAX_DIST, OUTPUT_HUB_MAX_DIST),
            neuron.position[1]
            + random.randint(-OUTPUT_HUB_MAX_DIST, OUTPUT_HUB_MAX_DIST),
        )
        neuron.output_hub_pos = output_hub_pos

        # create outputs
        for _ in range(NUM_OUTPUTS):
            output_pos = (
                output_hub_pos[0] + random.randint(-OUTPUT_MAX_DIST, OUTPUT_MAX_DIST),
                output_hub_pos[1] + random.randint(-OUTPUT_MAX_DIST, OUTPUT_MAX_DIST),
            )
            neuron.outputs.append(output_pos)

        state.neurons.append(neuron)
