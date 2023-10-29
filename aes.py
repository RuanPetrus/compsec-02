import sys
import numpy as np
from keyschedule import getkeys, get_words, get_num

State = any
SBOX_MATRIX_SIZE = 256

MIXCOLUMNS_MATRIX = np.array([
    [2, 3, 1, 1],
    [1, 2, 3, 1],
    [1, 1, 2, 3],
    [3, 1, 1, 2],
])

# citar codigo
def mix_col(r):
    a = [0]*4
    b = [0]*4
    for c in range(4):
        a[c]=r[c]
        h = r[c]>>7
        b[c] = (r[c] << 1) % 256
        b[c] ^= (h * 0x1B) % 256
    r[0] = b[0] ^ a[3] ^ a[2] ^ b[1] ^ a[1] 
    r[1] = b[1] ^ a[0] ^ a[3] ^ b[2] ^ a[2] 
    r[2] = b[2] ^ a[1] ^ a[0] ^ b[3] ^ a[3] 
    r[3] = b[3] ^ a[2] ^ a[1] ^ b[0] ^ a[0] 
    return r


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

def subbyte(state: State, sbox):
    for i in range(4):
        for j in range(4):
            state[i][j] = sbox[state[i][j]]

def shiftrows(state: State) -> State:
    for i in range(4):
        state[i] = np.roll(state[i], -i)

def add_round_key(state: State, keys : list[int]):
    state = state.T
    for i in range(4):
        state[i] = np.array(get_words(get_num(state[i]) ^ keys[i]))

def print_state(state):
    result = 0
    for i in range(4):
        result <<= 32
        result |= int(get_num((state.T)[i]))
    print(hex(result))


def aes(text: int, cypher_key: int, rounds:int) -> int:
    values = get_words(text, 128, 8)

    state = np.array(values, dtype=np.uint8).reshape((4, 4)).T
    sbox, isbox = generate_aes_sbox()
    keys = getkeys(cypher_key, rounds+1, sbox)

    add_round_key(state, keys[0:4])

    
    for r in range(1, rounds):
        subbyte(state, sbox)
        shiftrows(state)
        mix_cols(state)
        add_round_key(state, keys[4*r:4*(r+1)])

    subbyte(state, sbox)
    shiftrows(state)
    add_round_key(state, keys[4*rounds:4*(rounds+1)])
    print_state(state)


def main() -> None:
    aes( 0x00112233445566778899aabbccddeeff,
         0x000102030405060708090a0b0c0d0e0f,
         10
        )

    

if __name__ == "__main__":
    main()
