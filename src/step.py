import random
import glm

from src.brain import Neuron
from src.state import State, move_input, move_output


def step_state(state: State, dt: float) -> None:
    """Advance simulation time and bookkeeping."""
    state.step_count += 1
    state.time += dt

    for neuron in state.neurons:
        migrate_neuron(state, neuron)
        for input in neuron.inputs:
            migrate_input(state, input)
        for output in neuron.outputs:
            migrate_output(state, output)

    update_neuron_activity(state.neurons, dt)


def update_neuron_activity(neurons, dt: float) -> None:
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


# return an ivec2 of -1, 0, or +1 added to x and y of pos
def random_step() -> glm.ivec2:
    delta_x = random.randint(-1, 1)
    delta_y = random.randint(-1, 1)
    return glm.ivec2(delta_x, delta_y)


# return a nearby position within 1 unit in x and y, unclamped
def nearby(pos: glm.ivec2) -> glm.ivec2:
    delta = random_step()
    return glm.ivec2(pos.x + delta.x, pos.y + delta.y)


def roam(pos: glm.ivec2) -> glm.ivec2:
    new_pos = nearby(pos)

    # Clamp to grid
    lower = 0
    upper = State.GRID_SIZE - 1
    clamped_pos = glm.ivec2(
        max(lower, min(upper, new_pos.x)),
        max(lower, min(upper, new_pos.y)),
    )
    return clamped_pos


def clamp_to_grid(point: glm.ivec2) -> glm.ivec2:
    lower = 0
    upper = State.GRID_SIZE - 1
    return glm.ivec2(
        max(lower, min(upper, point.x)),
        max(lower, min(upper, point.y)),
    )


# migrate neuron
"""
migrate neuron will check if the neuron is currently satisfied
if it is satisfied, do nothing
if not satisfied, move the neuron randomly in x and y by up to 1 unit, so -1, 0, or +1 in each direction
clamp the neuron position to be within the grid
"""


def migrate_neuron(state: State, neuron: Neuron):
    if neuron.satisfied:
        return

    step = random_step()
    if step.x == 0 and step.y == 0:
        return  # no movement

    maybe_new_pos = glm.ivec2(neuron.pos.x + step.x, neuron.pos.y + step.y)
    maybe_new_pos = clamp_to_grid(maybe_new_pos)
    if maybe_new_pos == neuron.pos:
        return  # no movement

    neuron.pos = maybe_new_pos

    # check if inputs are too far from neuron / new york distance
    for input in neuron.inputs:
        moved_x = False
        moved_y = False

        # check if input is too far in x direction
        x_dist = abs(input.pos.x - neuron.pos.x)
        if x_dist > neuron.input_max_dist:
            # shift the input by the x step direction
            new_x = input.pos.x + step.x
            moved_x = True
            # if the neron was connected before, it should be disconnected.
            if input.connected_output:
                connected_output = input.connected_output
                connected_output.connected_input = None
                input.connected_output = None

        # check if input is too far in y direction
        y_dist = abs(input.pos.y - neuron.pos.y)
        if y_dist > neuron.input_max_dist:
            # shift the input by the y step direction
            new_y = input.pos.y + step.y
            moved_y = True
            # if the neron was connected before, it should be disconnected.
            if input.connected_output:
                connected_output = input.connected_output
                connected_output.connected_input = None
                input.connected_output = None

        if moved_x:
            input.pos.x = new_x
        if moved_y:
            input.pos.y = new_y
        if moved_x or moved_y:
            # replace the neuron in the input lookup
            move_input(state, input, glm.ivec2(input.pos.x, input.pos.y))

    # check if hub is now too far from neuron
    hub_pos = neuron.hub_pos
    hub_step = glm.ivec2(0, 0)

    hub_moved_x = False
    hub_x_dist = abs(hub_pos.x - neuron.pos.x)
    if hub_x_dist > neuron.hub_max_dist:
        hub_step.x = step.x
        hub_moved_x = True

    hub_moved_y = False
    hub_y_dist = abs(hub_pos.y - neuron.pos.y)
    if hub_y_dist > neuron.hub_max_dist:
        hub_step.y = step.y
        hub_moved_y = True

    if hub_moved_x or hub_moved_y:
        new_hub_pos = glm.ivec2(hub_pos.x + hub_step.x, hub_pos.y + hub_step.y)
        neuron.hub_pos = new_hub_pos

        # check if outputs have now moved beyond max distance from hub in both dimensions
        for output in neuron.outputs:
            output_moved_x = False
            output_x_dist = abs(output.pos.x - neuron.hub_pos.x)
            if output_x_dist > neuron.output_max_dist:
                new_x = output.pos.x + hub_step.x
                output_moved_x = True
                # if the output was connected before, it should be disconnected.
                if output.connected_input:
                    connected_input = output.connected_input
                    connected_input.connected_output = None
                    output.connected_input = None

            output_moved_y = False
            output_y_dist = abs(output.pos.y - neuron.hub_pos.y)
            if output_y_dist > neuron.output_max_dist:
                new_y = output.pos.y + hub_step.y
                output_moved_y = True
                # if the output was connected before, it should be disconnected.
                if output.connected_input:
                    connected_input = output.connected_input
                    connected_input.connected_output = None
                    output.connected_input = None

            if output_moved_x:
                output.pos.x = new_x
            if output_moved_y:
                output.pos.y = new_y

            if output_moved_x or output_moved_y:
                # replace the output in the output lookup
                move_output(state, output, glm.ivec2(output.pos.x, output.pos.y))


def migrate_input(state: State, input):
    """
    just like migrate neuron, except satisfied status is just whether the input is connected to an output
    """

    if input.connected_output:
        return

    step = random_step()
    if step.x == 0 and step.y == 0:
        return  # no movement

    maybe_new_pos = glm.ivec2(input.pos.x + step.x, input.pos.y + step.y)
    maybe_new_pos = clamp_to_grid(maybe_new_pos)
    if maybe_new_pos == input.pos:
        return  # no movement

    input.pos = maybe_new_pos
    # we do not have to check if we broke a connection since we dont migrate if connected
    move_input(state, input, glm.ivec2(input.pos.x, input.pos.y))


def migrate_output(state: State, output):
    """
    just like migrate neuron, except satisfied status is just whether the output is connected to an input
    """

    if output.connected_input:
        return

    step = random_step()
    if step.x == 0 and step.y == 0:
        return  # no movement

    maybe_new_pos = glm.ivec2(output.pos.x + step.x, output.pos.y + step.y)
    maybe_new_pos = clamp_to_grid(maybe_new_pos)
    if maybe_new_pos == output.pos:
        return  # no movement

    output.pos = maybe_new_pos
    # we do not have to check if we broke a connection since we dont migrate if connected
    move_output(state, output, glm.ivec2(output.pos.x, output.pos.y))
