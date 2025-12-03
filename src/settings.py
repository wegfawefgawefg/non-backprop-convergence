import glm

# sim
SIMULATION_FPS = 60.0  # 480.0
SIM_DT = 1.0 / SIMULATION_FPS

# rendering
RENDER_FPS = 60.0
RENDER_INTERVAL = 1.0 / RENDER_FPS

WINDOW_DIMS = glm.vec2(1600, 800)
DIMS = WINDOW_DIMS / 2

# layout
LEFT_PADDING_FRAC_X = 0.02
TOP_PADDING_FRAC_Y = 0.04
SQUARE_SIZE_HEIGHT_FRAC = 0.4
VERTICAL_GAP_FRAC_Y = 0.04

# brain
GRID_SIZE = 8
NEURON_CHARGE_RATE = 0.2  # charge per second
SIGNAL_SPEED = 4.0  # normalized units per second
NUM_NEURONS = 2
INPUT_MAX_DIST = 2
HUB_MAX_DIST = 4
OUTPUT_MAX_DIST = 2

NUM_INPUTS = 4
NUM_OUTPUTS = 4

NEURON_SATISFACTION_RATIO = (
    0.5  # what fraction of inputs must be connected for the neuron to not move
)
HUB_SATISFACTION_RATIO = (
    0.5  # what fraction of outputs must be connected for the hub to not move
)
