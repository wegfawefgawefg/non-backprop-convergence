# objects are in int positions on a grid


class Pos:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y


class Inputs:
    def __init__(self) -> None:
        self.pos: Pos = None
        self.weight: float = None


class Outputs:
    def __init__(self) -> None:
        self.pos: Pos = None
        self.weight: float = None


class Neuron:
    def __init__(self) -> None:
        self.pos: Pos = None
        self.charge: float = None
        self.fire_threshold: float = None
        self.decay_rate: float = None

        self.num_inputs = 4
        self.input_max_dist = 4
        self.inputs = []

        self.num_outputs = 4
        self.output_hub_max_dist = 16
        self.output_hub_pos: Pos = None
        self.outputs = []


def main():
    print("bla")


if __name__ == "__main__":
    main()
