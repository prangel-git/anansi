from utils.src.greet import *


def test_greet_with_name():
    assert greet("a_name") == "Hello a_name"
