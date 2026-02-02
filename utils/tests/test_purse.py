from utils.src.purse import *


def test_number_tokens():
    my_purse = Purse()
    assert my_purse.tokens is not None


def test_add_token():
    my_purse = Purse()
    my_purse.add_token("pe")
    assert my_purse.is_token("pe")


def test_str_to_tokens():
    string_stream = "Peter"
    my_purse = Purse()
    token_string = my_purse.str_to_tokens(string_stream)
    expected_outcome = ["P", "e", "t", "e", "r"]
    assert expected_outcome == token_string


def test_str_to_tokens_more_than_one_character():
    string_stream = "Peter"
    my_purse = Purse()
    my_purse.add_token("Pe")
    token_string = my_purse.str_to_tokens(string_stream)
    expected_outcome = ["Pe", "t", "e", "r"]
    assert expected_outcome == token_string


def test_word_to_tokens_piper():
    string_stream = "piper"
    my_purse = Purse()
    my_purse.add_token("pe")
    my_purse.add_token("per")
    token_string = my_purse.word_to_tokens(string_stream)
    expected_outcome = ["p", "i", "per"]
    assert expected_outcome == token_string


def test_str_to_tokens_one_character_token():
    string_stream = "A"
    my_purse = Purse()
    token_string = my_purse.str_to_tokens(string_stream)
    expected_outcome = ["A"]
    assert expected_outcome == token_string


def test_str_to_tokens_multiple_possible_tokens():
    string_stream = "ePeter"
    my_purse = Purse()
    my_purse.add_token("Pet")
    my_purse.add_token("eP")
    token_string = my_purse.str_to_tokens(string_stream)
    expected_outcome = ["eP", "e", "t", "e", "r"]
    assert expected_outcome == token_string


def test_token_pairings():
    string_stream = "Peter Piper picked a peck of pickled peppers"
    my_purse = Purse()
    token_string = my_purse.str_to_tokens(string_stream)
    token_pairing_count = my_purse.count_token_pairings(token_string)
    assert token_pairing_count["pe"] == 4


def test_byte_pair_encoding_one_step():
    string_stream = "Peter Piper picked a peck of pickled peppers"
    my_purse = Purse()
    token_string = my_purse.str_to_tokens(string_stream)
    my_purse.token_pairing(token_string)
    assert my_purse.is_token("pe")


def test_a_few_pair_encodings():
    string_stream = "Peter Piper picked a peck of pickled peppers"
    my_purse = Purse()

    for _ in range(6):
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
        "pick",
        "ed",
        " ",
        "a",
        " ",
        "pe",
        "ck",
        " ",
        "o",
        "f",
        " ",
        "pick",
        "l",
        "ed",
        " ",
        "pe",
        "p",
        "per",
        "s",
    ]

    assert expected_tokenization == token_string


def test_break_string():
    broken_string = break_string("Peter Parker")
    expected_break = ["Peter", " ", "Parker"]
    assert broken_string == expected_break


def test_break_string_just_spaces():
    broken_string = break_string("  ")
    expected_break = [" ", " "]
    assert broken_string == expected_break


def test_break_string_punctuation():
    broken_string = break_string("??..!! !🦑👻")
    expected_break = ["?", "?", ".", ".", "!", "!", " ", "!", "🦑", "👻"]
    assert broken_string == expected_break


def test_is_letter():
    assert is_letter("n")


def test_is_letter_not():
    assert not is_letter("👻")
