class Purse:
    def __init__(self, text_stream) -> None:
        self.tokens = set(k for k in text_stream)
        self.token_max_len = 1

    def add_token(self, token):
        self.tokens.add(token)
        self.token_max_len = max(self.token_max_len, len(token))

    def number_tokens(self) -> int:
        return len(self.tokens)

    def token_pairing(self, token_stream):
        counts = self.count_token_pairings(token_stream)
        max_count = max(counts, key=counts.get)
        self.add_token(max_count)

    def count_token_pairings(self, token_stream: list[str]) -> dict[str, int]:
        token_pairing_to_count = dict()
        for idx in range(len(token_stream) - 1):
            current_token_pair = token_stream[idx] + token_stream[idx + 1]
            token_pairing_to_count[current_token_pair] = (
                token_pairing_to_count.get(current_token_pair, 0) + 1
            )
        return token_pairing_to_count

    def is_token(self, token):
        return token in self.tokens

    def str_to_tokens(self, string):
        if not string:
            return []
        else:
            max_possible_token = max(self.token_max_len, len(string))
            for k in range(max_possible_token, 0, -1):
                if string[:k] in self.tokens:
                    token = string[:k]
                    rest_of_string = string[k:]
                    output = [token]
                    return output + self.str_to_tokens(rest_of_string)

        raise Exception("The string contains a non-token")
