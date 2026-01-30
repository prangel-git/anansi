from utils.src.greet import *
from utils.src.purse import *


def main():
    print(greet("world"))

    string_stream = "Peter Piper picked a peck of pickled peppers"
    my_purse = Purse()

    for _ in range(5):
        token_string = my_purse.str_to_tokens(string_stream)
        my_purse.token_pairing(token_string)

    token_string = my_purse.str_to_tokens(string_stream)
    expected_tokenization = [
        "P",
        "e",
        "t",
        "e",
        "r",
        " ",
        "P",
        "i",
        "per",
        " ",
        "pi",
        "ck",
        "ed",
        " ",
        "a",
        " ",
        "p",
        "e",
        "ck",
        " ",
        "o",
        "f",
        " ",
        "pi",
        "ck",
        "l",
        "ed",
        " ",
        "pe",
        "p",
        "per",
        "s",
    ]

    print(expected_tokenization)
    print(token_string)
    print(my_purse.tokens)


if __name__ == "__main__":
    main()
