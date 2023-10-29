import numpy as np


def main() -> None:
    state = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 1],
    ], np.uint8)
    print(mix_cols(state))

if __name__ == "__main__":
    main()
