from utils.src.greet import *
from utils.src.purse import *


def main():
    print(greet("world"))
    string_stream = "Peter Piper picked a peck of pickled peppers"
    my_purse = Purse(string_stream)

    for _ in range(5):
        token_string = my_purse.str_to_tokens(string_stream)
        my_purse.token_pairing(token_string)

    token_string = my_purse.str_to_tokens(string_stream)
    print(token_string)


if __name__ == "__main__":
    main()
