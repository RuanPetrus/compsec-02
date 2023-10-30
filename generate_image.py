from PIL import Image
import numpy as np
import io
import aes

TEST_IMAGE_PATH = "mario.png"
OUTPUT_PATH = "enc_mario13.png"
PASSWORD = 1234
ROUNDS = 13

def get_image_data(image_path: str) -> tuple[bytearray, int, int]:
    im = Image.open(TEST_IMAGE_PATH).convert("RGB")
    w, h = im.size
    pixels = im.load()
    data = bytearray([
        d
        for j in range(h)
        for i in range(w)
        for d in pixels[(i, j)]
    ])
    return data, h, w

def image_array_from_bytearray(data: bytearray, height: int, width: int):
    return np.array([
        int(data[i])
        for i in range(len(data))
    ], dtype=np.uint8).reshape((height, width, 3))

def main():
    data, h, w = get_image_data(TEST_IMAGE_PATH)
    print(len(data))
    encrypted_data = aes.ctr_encrypt(data, PASSWORD, ROUNDS)
    # encrypted_data = data
    m = image_array_from_bytearray(encrypted_data, h, w)
    img = Image.fromarray(m, mode="RGB")
    img.save(OUTPUT_PATH)


if __name__ == "__main__":
    main()
