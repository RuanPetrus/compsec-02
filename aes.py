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

IMIXCOLUMNS_MATRIX = np.array([
    [0x0e, 0x0b, 0x0d, 0x09],
    [0x09, 0x0e, 0x0b, 0x0d],
    [0x0d, 0x09, 0x0e, 0x0b],
    [0x0b, 0x0d, 0x09, 0x0e],
])

def xtime(a, n):
    if n == 0: return a
    a = xtime(a,n-1)

    msb = a >> 7
    result = (a << 1) % 256
    if msb == 1:
        result ^= 0x1B
    return result

def mul(a,b):
    result=0
    for i in range(8):
        if a & 1 == 1: 
            result ^= xtime(b, i)
        a >>= 1
    return result

def mul_mat_vec(mat, vec):
    result = [0,0,0,0]

    for i in range(4):
        for j in range(4):
            result[i] ^= mul(mat[i][j], vec[j])
    return result

def mix_col(r, mat):
    return mul_mat_vec(mat, r)
 
def mix_cols(state, mat):
    state=state.T
    for i in range(4):
        state[i] = np.array(mix_col(state[i], mat))


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

def ishiftrows(state: State) -> State:
    for i in range(4):
        state[i] = np.roll(state[i], i)

def add_round_key(state: State, keys : list[int]):
    state = state.T
    for i in range(4):
        state[i] = np.array(get_words(get_num(state[i]) ^ keys[i]))


def state_num(state) -> int:
    result = 0
    for i in range(4):
        result <<= 32
        result |= int(get_num((state.T)[i]))
    return result

def print_state(state):
    print(hex(state_num(state)))


def aes_encrypt(text: int, cypher_key: int, rounds:int) -> int:
    values = get_words(text, 128, 8)

    state = np.array(values, dtype=np.uint8).reshape((4, 4)).T
    sbox, isbox = generate_aes_sbox()
    keys = getkeys(cypher_key, rounds+1, sbox)

    add_round_key(state, keys[0:4])

    
    for r in range(1, rounds):
        subbyte(state, sbox)
        shiftrows(state)
        mix_cols(state, MIXCOLUMNS_MATRIX)
        add_round_key(state, keys[4*r:4*(r+1)])

    subbyte(state, sbox)
    shiftrows(state)
    add_round_key(state, keys[4*rounds:4*(rounds+1)])
    return state_num(state)

def aes_decrypt(text: int, cypher_key: int, rounds:int) -> int:
    values = get_words(text, 128, 8)

    state = np.array(values, dtype=np.uint8).reshape((4, 4)).T
    sbox, isbox = generate_aes_sbox()
    keys = getkeys(cypher_key, rounds+1, sbox)

    add_round_key(state, keys[rounds*4:(rounds+1)*4])

    for r in range(rounds-1, 0, -1):
        ishiftrows(state)
        subbyte(state, isbox)
        add_round_key(state, keys[4*r:4*(r+1)])
        mix_cols(state, IMIXCOLUMNS_MATRIX)

    ishiftrows(state)
    subbyte(state, isbox)
    add_round_key(state, keys[0:4])
    return state_num(state)

def encrypt_array(data : bytearray, key, rounds=10) -> int:
    blocks = []
    ctr = 0xf0f1f2f3f4f5f6f7f8f9fafbfcfdfeff
    for i in range(len(data)//16):
        blocks.append(get_num(data[16*i:16*(i+1)])) 

    outs = [aes_encrypt(ctr+i, key, rounds) for i in range(len(blocks))]
    cyphers = [blocks[i] ^ outs[i] for i in range(len(blocks))]
    result = []
    for num in cyphers:
        nums = get_words(num, 128, 8)
        for byte in nums: result.append(byte)
    
    if len(data) % 16 != 0:
        last = data[16 * (len(data) // 16):]
        last_len = len(last)
        last = get_num(last)
        last_out = aes_encrypt(ctr+len(blocks), key, rounds)
        last_cypher = last^(last_out >> (16-last_len))
        last_num = get_words(last_cypher, last_len*8, 8)
        for byte in last_num: result.append(byte)

    return bytearray(result)

def main() -> None:
    x = encrypt_array(bytearray([123]*16), 12)
    y = encrypt_array(x, 12)
    print(y)

    

if __name__ == "__main__":
    main()
