import aes
import sys
from keyschedule import get_num, get_words

def usage() -> None:
    print("python3 main.py <command>")
    print()
    print("command:")
    print("     encrypt_aes   <password> <rounds>")
    print("     decrypt_aes   <password> <rounds>")
    print("     encrypt_ctr   <password> <rounds>")
    print("     decrypt_ctr   <password> <rounds>")
    print()
    print("Examples:")
    print("cat example_aes.txt | python3 main.py encrypt_aes 10123 10 | python3 main.py decrypt_aes 10123 10")
    print("cat example_ctr.txt | python3 main.py encrypt_ctr 10123 10 | python3 main.py decrypt_ctr 10123 10")
    print()

def next_arg(args: list[str]) -> str:
    if len(args) == 0:
        usage()
        exit(1)
    argument = args[0]
    args.pop(0)
    return argument

def read_from_stdin() -> str:
    text = open(0).read()
    return text

def print_to_stdout(*a) -> None:
    print(*a, file=sys.stdout, end="")

def main() -> None:
    args = sys.argv
    program = next_arg(args)
    command = next_arg(args)
    text = read_from_stdin()

    if command == "encrypt_aes":
        password = int(next_arg(args))
        rounds = int(next_arg(args))
        if (len(text) != 16):
            print("Error: text needs to be 16 bytes")
            usage()
            exit(1)

        text_int = get_num([ord(c) for c in text])
        result_int = aes.aes_encrypt(text_int, password, rounds)
        result = "".join(chr(x) for x in get_words(result_int, 128, 8))
        print_to_stdout(result)

    elif command == "decrypt_aes":
        password = int(next_arg(args))
        rounds = int(next_arg(args))
        if (len(text) != 16):
            print("Error: text needs to be 16 bytes")
            usage()
            exit(1)

        text_int = get_num([ord(c) for c in text])
        result_int = aes.aes_decrypt(text_int, password, rounds)
        result = "".join(chr(x) for x in get_words(result_int, 128, 8))
        print_to_stdout(result)

    elif command == "encrypt_ctr":
        password = int(next_arg(args))
        rounds = int(next_arg(args))

        text_bytes = bytearray(ord(c) for c in text)
        result_bytes = aes.ctr_encrypt(text_bytes, password, rounds)
        result = "".join(chr(int(x)) for x in result_bytes)
        print_to_stdout(result)

    elif command == "decrypt_ctr":
        password = int(next_arg(args))
        rounds = int(next_arg(args))

        text_bytes = bytearray(ord(c) for c in text)
        result_bytes = aes.ctr_encrypt(text_bytes, password, rounds)
        result = "".join(chr(int(x)) for x in result_bytes)
        print_to_stdout(result)

    else:
        usage()
        exit(1)

if __name__ == "__main__":
    main()
