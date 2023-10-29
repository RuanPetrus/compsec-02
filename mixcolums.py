import numpy as np

MIXCOLUMNS_MATRIX = np.array([
    [2, 3, 1, 1],
    [1, 2, 3, 1],
    [1, 1, 2, 3],
    [3, 1, 1, 2],
], np.uint8)

def mix_col(col):
    return np.dot(MIXCOLUMNS_MATRIX, col)

def mix_cols(state):
    return np.apply_along_axis(mix_col, axis=0, arr=state)

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
