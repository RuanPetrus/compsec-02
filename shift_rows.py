SBOX_MATRIX_SIZE = 256

State = list[int]

def shift_list(l: list[int], shift: int) -> list[int]:
    sz = len(l)
    return [l[(i + shift) % sz] for i in range(sz)]

def shiftrows(state: State) -> State:
    return [shift_list(state[i], i) for i in range(len(state))]

def main() -> None:
    state = [
        [ 1,  2,  3,  4],
        [ 5,  6,  7,  8],
        [ 9, 10, 11, 12],
        [13, 14, 15, 16]
    ]
    print(shiftrows(state))
	

if __name__ == "__main__":
    main()
