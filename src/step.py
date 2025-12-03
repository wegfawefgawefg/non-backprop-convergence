import random
import glm

from src.brain import Input, Neuron, Output
from src.state import State, move_input, move_output
from src.settings import (
    GRID_SIZE,
    INPUT_MAX_DIST,
    OUTPUT_MAX_DIST,
    HUB_MAX_DIST,
    SIGNAL_SPEED,
    NEURON_SATISFACTION_RATIO,
    HUB_SATISFACTION_RATIO,
)


def step_state(state: State, dt: float) -> None:
    """Advance simulation time and bookkeeping."""
    state.step_count += 1
    state.time += dt
    move_neurons_this_frame = state.step_count % 8 == 0
    move_hubs_this_frame = state.step_count % 4 == 0

    for neuron in state.neurons:
        if move_neurons_this_frame:
            migrate_neuron(state, neuron)
        if move_hubs_this_frame:
            migrate_hub(state, neuron)
        for input in neuron.inputs:
            migrate_input(state, input)
        for output in neuron.outputs:
            migrate_output(state, output)

    update_neuron_activity(state.neurons, dt)


def clamp_charge(amount: float) -> float:
    return max(0.0, min(1.0, amount))


def maybe_start_signal(neuron: Neuron):
    if neuron.signal_active:
        return
    if neuron.charge >= 1.0:
        neuron.charge = 0.0
        neuron.signal_active = True
        neuron.signal_pos = 0.0


def signal_transfer_amount(input: Input, output: Output) -> float:
    return clamp_charge(1.0 * input.weight * output.weight)


def dispatch_signal(neuron: Neuron):
    for output in neuron.outputs:
        connected_input = output.connected_input
        if not connected_input:
            continue
        target_neuron = connected_input.parent_neuron
        if not target_neuron:
            continue

        transfer = signal_transfer_amount(connected_input, output)
        if transfer <= 0.0:
            continue

        target_neuron.charge = clamp_charge(target_neuron.charge + transfer)
        maybe_start_signal(target_neuron)


def update_neuron_activity(neurons, dt: float) -> None:
    for neuron in neurons:
        if neuron.signal_active:
            neuron.signal_pos += SIGNAL_SPEED * dt
            if neuron.signal_pos >= 1.0:
                neuron.signal_pos = 0.0
                neuron.signal_active = False
                dispatch_signal(neuron)
        else:
            neuron.charge += neuron.charge_rate * dt
            maybe_start_signal(neuron)


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
    upper = GRID_SIZE - 1
    return glm.ivec2(
        max(lower, min(upper, point.x)),
        max(lower, min(upper, point.y)),
    )


def clamp_to_taxicab_neighborhood(
    point: glm.ivec2, center: glm.ivec2 | None, max_dist: int
) -> glm.ivec2:
    """Clamp point to grid and within an L1 neighborhood of center."""
    clamped = clamp_to_grid(point)
    if center is None:
        return clamped

    dx = clamped.x - center.x
    dy = clamped.y - center.y
    while abs(dx) + abs(dy) > max_dist:
        if abs(dx) >= abs(dy) and dx != 0:
            dx -= 1 if dx > 0 else -1
        elif dy != 0:
            dy -= 1 if dy > 0 else -1
        else:
            break
    return clamp_to_grid(glm.ivec2(center.x + dx, center.y + dy))


def pull_outputs_toward_hub(state: State, neuron: Neuron):
    """Ensure outputs remain within their allowed radius when the hub moves."""
    hub_center = neuron.hub_pos
    if hub_center is None:
        return

    for output in neuron.outputs:
        new_pos = clamp_to_taxicab_neighborhood(
            glm.ivec2(output.pos.x, output.pos.y), hub_center, OUTPUT_MAX_DIST
        )
        if new_pos != output.pos:
            if output.connected_input:
                disconnect_input_output(output.connected_input, output)
            move_output(state, output, new_pos)
            attempt_connect_output(state, output)


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
        new_x = input.pos.x
        new_y = input.pos.y

        # check if input is too far in x direction
        x_dist = abs(input.pos.x - neuron.pos.x)
        if x_dist > INPUT_MAX_DIST:
            # shift the input by the x step direction
            new_x = input.pos.x + step.x
            moved_x = True
            # if the neron was connected before, it should be disconnected.
            if input.connected_output:
                disconnect_input_output(input, input.connected_output)

        # check if input is too far in y direction
        y_dist = abs(input.pos.y - neuron.pos.y)
        if y_dist > INPUT_MAX_DIST:
            # shift the input by the y step direction
            new_y = input.pos.y + step.y
            moved_y = True
            # if the neron was connected before, it should be disconnected.
            if input.connected_output:
                disconnect_input_output(input, input.connected_output)

        if moved_x or moved_y:
            target_pos = clamp_to_taxicab_neighborhood(
                glm.ivec2(new_x, new_y), neuron.pos, INPUT_MAX_DIST
            )
            move_input(state, input, target_pos)
            attempt_connect_input(state, input)

    # ensure hub stays within allowed distance after the neuron moves
    hub_pos = neuron.hub_pos
    clamped_hub = clamp_to_taxicab_neighborhood(
        glm.ivec2(hub_pos.x, hub_pos.y), neuron.pos, HUB_MAX_DIST
    )
    if clamped_hub != hub_pos:
        neuron.hub_pos = clamped_hub
        pull_outputs_toward_hub(state, neuron)


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
    parent_neuron = input.parent_neuron
    center = parent_neuron.pos if parent_neuron else None
    maybe_new_pos = clamp_to_taxicab_neighborhood(maybe_new_pos, center, INPUT_MAX_DIST)
    if maybe_new_pos == input.pos:
        return  # no movement

    # we do not have to check if we broke a connection since we dont migrate if connected
    move_input(state, input, maybe_new_pos)
    attempt_connect_input(state, input)


def migrate_hub(state: State, neuron: Neuron):
    """Randomly walk hubs while keeping them near their neuron."""
    if neuron.hub_satisfied:
        return

    step = random_step()
    if step.x == 0 and step.y == 0:
        return

    maybe_new_pos = glm.ivec2(neuron.hub_pos.x + step.x, neuron.hub_pos.y + step.y)
    maybe_new_pos = clamp_to_taxicab_neighborhood(
        maybe_new_pos, neuron.pos, HUB_MAX_DIST
    )

    if maybe_new_pos == neuron.hub_pos:
        return

    neuron.hub_pos = maybe_new_pos
    pull_outputs_toward_hub(state, neuron)


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
    parent_neuron = output.parent_neuron
    hub_center = parent_neuron.hub_pos if parent_neuron else None
    maybe_new_pos = clamp_to_taxicab_neighborhood(
        maybe_new_pos, hub_center, OUTPUT_MAX_DIST
    )
    if maybe_new_pos == output.pos:
        return  # no movement

    # we do not have to check if we broke a connection since we dont migrate if connected
    move_output(state, output, maybe_new_pos)
    attempt_connect_output(state, output)


def set_neuron_satisfaction(neuron: Neuron):
    """Set the satisfied status of the neuron based on its connections."""

    connected_inputs = sum(1 for input in neuron.inputs if input.connected_output)
    total_inputs = len(neuron.inputs)
    neuron.satisfied = (
        connected_inputs / total_inputs >= NEURON_SATISFACTION_RATIO
        if total_inputs > 0
        else True
    )


def set_hub_satisfaction(neuron: Neuron):
    """Set the satisfied status of the neuron hub based on its connections."""

    connected_outputs = sum(1 for output in neuron.outputs if output.connected_input)
    total_outputs = len(neuron.outputs)
    neuron.hub_satisfied = (
        connected_outputs / total_outputs >= HUB_SATISFACTION_RATIO
        if total_outputs > 0
        else True
    )


def connect_input_output(input: Input, output: Output):
    """Connect the given input and output and update satisfaction."""
    if input.connected_output or output.connected_input:
        return
    if input.parent_neuron is output.parent_neuron:
        return

    input.connected_output = output
    output.connected_input = input

    if input.parent_neuron:
        set_neuron_satisfaction(input.parent_neuron)
    if output.parent_neuron:
        set_hub_satisfaction(output.parent_neuron)


def disconnect_input_output(input: Input | None, output: Output | None):
    """Disconnect the given input/output pair and update satisfaction."""
    if not input or not output:
        return

    if input.connected_output is output:
        input.connected_output = None
    if output.connected_input is input:
        output.connected_input = None

    if input.parent_neuron:
        set_neuron_satisfaction(input.parent_neuron)
    if output.parent_neuron:
        set_hub_satisfaction(output.parent_neuron)


def attempt_connect_input(state: State, input: Input):
    """Connect the input to an available output at its current location."""
    if input.connected_output:
        return

    key = (input.pos.x, input.pos.y)
    candidates = state.output_pos_lookup.get(key)
    if not candidates:
        return

    for output in candidates:
        if not output.connected_input:
            connect_input_output(input, output)
            break


def attempt_connect_output(state: State, output: Output):
    """Connect the output to an available input at its current location."""
    if output.connected_input:
        return

    key = (output.pos.x, output.pos.y)
    candidates = state.input_pos_lookup.get(key)
    if not candidates:
        return

    for input in candidates:
        if not input.connected_output:
            connect_input_output(input, output)
            break
