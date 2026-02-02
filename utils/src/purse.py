class Purse:
    def __init__(self) -> None:
        self.tokens = set()

    def add_token(self, token):
        self.tokens.add(token)

    def number_tokens(self) -> int:
        return len(self.tokens)

    def token_pairing(self, token_stream):
        counts = self.count_token_pairings(token_stream)
        max_count = max(counts, key=counts.get)
        self.add_token(max_count)

    def count_token_pairings(self, token_stream: list[str]) -> dict[str, int]:
        token_pairing_to_count = dict()
        for idx in range(len(token_stream) - 1):
            if is_letter(token_stream[idx][0]) and is_letter(token_stream[idx + 1][0]):
                current_token_pair = token_stream[idx] + token_stream[idx + 1]
                token_pairing_to_count[current_token_pair] = (
                    token_pairing_to_count.get(current_token_pair, 0) + 1
                )
        return token_pairing_to_count

    def is_token(self, coin):
        if len(coin) == 1:
            return True
        return coin in self.tokens

    def word_to_tokens(self, word):
        if not word:
            return []
        else:
            for k in range(len(word), 0, -1):
                token = word[:k]
                rest_of_string = word[k:]
                if self.is_token(word[:k]):
                    return [token] + self.word_to_tokens(rest_of_string)

        return [word[0]] + self.word_to_tokens(word[1:])

    def str_to_tokens(self, string):
        tokens = []
        for word in break_string(string):
            tokens += self.word_to_tokens(word)
        return tokens


def is_letter(character):
    return ("a" <= character and character <= "z") or (
        "A" <= character and character <= "Z"
    )


def break_string(string):

    if not string:
        return []

    if not is_letter(string[0]):
        return [string[0]] + break_string(string[1:])

    current_word = ""
    for character in string:
        if is_letter(character):
            current_word += character
        else:
            break

    return [current_word] + break_string(string[len(current_word) :])
