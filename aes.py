import sys
import numpy as np

State = any

def aes(text: int, cypher_key: int) -> int:
    values = []
    h = hex(text)
    for i in range(16):
        pos = 2 + i * 2
        value = int(h[pos: pos+2], 16)
        values.append(value)

    state = np.array(values, dtype=np.uint8).reshape((4, 4))
    print(state)

def main() -> None:
    aes(int("f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff", 16), 21)
    

if __name__ == "__main__":
    main()
