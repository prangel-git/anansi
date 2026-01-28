from utils.src.purse import *


def test_number_tokens():
    my_purse = Purse("AaBb c")
    assert my_purse.number_tokens() == 6


def test_is_token_return_true():
    my_purse = Purse("AaBb c")
    assert my_purse.is_token("c")


def test_is_token_return_false():
    my_purse = Purse("AaBb c")
    assert not my_purse.is_token("d")


def test_add_token():
    my_purse = Purse("")
    my_purse.add_token("pe")
    assert my_purse.is_token("pe")


def test_max_length():
    my_purse = Purse("")
    my_purse.add_token("pe")
    assert my_purse.token_max_len == 2


def test_str_to_tokens():
    string_stream = "Peter"
    my_purse = Purse(string_stream)
    token_string = my_purse.str_to_tokens(string_stream)
    expected_outcome = ["P", "e", "t", "e", "r"]
    assert expected_outcome == token_string


def test_str_to_tokens_more_than_one_character():
    string_stream = "Peter"
    my_purse = Purse(string_stream)
    my_purse.add_token("Pe")
    token_string = my_purse.str_to_tokens(string_stream)
    expected_outcome = ["Pe", "t", "e", "r"]
    assert expected_outcome == token_string


def test_str_to_tokens_multiple_possible_tokens():
    string_stream = "ePeter"
    my_purse = Purse(string_stream)
    my_purse.add_token("Pet")
    my_purse.add_token("eP")
    token_string = my_purse.str_to_tokens(string_stream)
    expected_outcome = ["eP", "e", "t", "e", "r"]
    assert expected_outcome == token_string


def test_token_pairings():
    string_stream = "Peter Piper picked a peck of pickled peppers"
    my_purse = Purse(string_stream)
    token_string = my_purse.str_to_tokens(string_stream)
    token_pairing_count = my_purse.count_token_pairings(token_string)
    assert token_pairing_count["pe"] == 4


def test_byte_pair_encoding_one_step():
    string_stream = "Peter Piper picked a peck of pickled peppers"
    my_purse = Purse(string_stream)
    token_string = my_purse.str_to_tokens(string_stream)
    my_purse.token_pairing(token_string)
    assert my_purse.is_token("pe")


def test_a_few_pair_encodings():
    string_stream = "Peter Piper picked a peck of pickled peppers"
    my_purse = Purse(string_stream)

    for _ in range(5):
        token_string = my_purse.str_to_tokens(string_stream)
        my_purse.token_pairing(token_string)

    token_string = my_purse.str_to_tokens(string_stream)

    assert ["per"] == token_string
