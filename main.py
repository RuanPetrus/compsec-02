SBOX_MATRIX_SIZE = 256

State = list[int]

def cap_8bit(x: int) -> int:
    mask8bit = (1 << 8) - 1
    return x & mask8bit

def rotl_8bit(x: int, shift: int) -> int:
    x = cap_8bit(x)
    return cap_8bit((x << shift) | (x >> (8 - shift)))

def generate_aes_sbox() -> tuple[list[int], list[int]]:
    sbox = [0] * SBOX_MATRIX_SIZE
    p = 1
    q = 1

    while(True):
        p = cap_8bit(p ^ (p << 1) ^ (0x1B if (p & 0x80) else 0))

        q ^= q << 1
        q ^= q << 2
        q ^= q << 4
        q ^= (0x09 if (q & 0x80) else 0)
        q = cap_8bit(q)
        
        xformed = cap_8bit((q ^ rotl_8bit(q, 1) 
                              ^ rotl_8bit(q, 2) 
                              ^ rotl_8bit(q, 3) 
                              ^ rotl_8bit(q, 4)))
        sbox[p] = xformed ^ 0x63
        if p == 1:
            break

    sbox[0] = 0x63

    inverse_sbox = [0] * SBOX_MATRIX_SIZE
    for x in range(SBOX_MATRIX_SIZE):
        inverse_sbox[sbox[x]] = x

    return sbox, inverse_sbox


def print_sbox(sbox: list[int]) -> None:
    print("SBOX:")
    for i in range(16):
        for j in range(16):
            print(hex(sbox[i*16 + j]), end=" ")
        print()

def subbyte(state: State) -> list[int]:
    return [sbox[x] for x in state]


def main() -> None:
    sbox, inverse_sbox = generate_aes_sbox()
    print_sbox(inverse_sbox)


if __name__ == "__main__":
    main()
