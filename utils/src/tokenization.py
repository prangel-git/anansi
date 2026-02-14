"""Byte Pair Encoding tokenizer."""


class BPETokenizer:
    """
    A Byte Pair Encoding tokenizer that learns and applies token merges.

    Only consecutive letters are grouped together into tokens. Non-letter
    characters (spaces, punctuation, emoji) remain as individual tokens
    and are never merged with letter tokens.
    """

    def __init__(self) -> None:
        """Initialize the tokenizer with no learned tokens."""
        self.tokens = set()

    def add_token(self, token: str) -> None:
        """Add a learned token to the tokenizer."""
        self.tokens.add(token)

    def is_token(self, token: str) -> bool:
        """
        Check if a token is known.

        Single characters are always considered valid tokens.
        Multi-character tokens must be in the learned tokens set.
        """
        if len(token) == 1:
            return True
        return token in self.tokens

    def learn_from_text(self, text: str, iterations: int = 1) -> None:
        """
        Learn tokens using BPE algorithm.

        Args:
            text: The text to learn from
            iterations: Number of BPE iterations to perform
        """
        for _ in range(iterations):
            # Tokenize current text with known tokens
            tokenized = self.tokenize(text)

            # Find most common pairing among letter sequences
            pair_counts = self._count_letter_pairings(tokenized)

            if not pair_counts:
                break

            # Learn the most common pairing
            most_common = max(pair_counts, key=pair_counts.get)  # type: ignore
            self.add_token(most_common)

    def tokenize(self, text: str) -> list[str]:
        """
        Tokenize text into a list of tokens.

        Letters are grouped into word segments, then each segment
        is tokenized using learned tokens. Non-letter characters
        become individual tokens.
        """
        tokens = []
        for segment in self._break_into_segments(text):
            tokens.extend(self._tokenize_segment(segment))
        return tokens

    def _break_into_segments(self, text: str) -> list[str]:
        """
        Break text into segments of letters and non-letters.

        E.g., "hello, world" -> ["hello", ",", " ", "world"]
        """
        if not text:
            return []

        segments = []
        current_segment = ""

        for char in text:
            is_letter = self._is_letter(char)
            is_current_letter = current_segment and self._is_letter(current_segment[0])

            if current_segment and is_letter != is_current_letter:
                # Type changed, save current segment and start new one
                segments.append(current_segment)
                current_segment = char
            else:
                current_segment += char

        if current_segment:
            segments.append(current_segment)

        return segments

    def _tokenize_segment(self, segment: str) -> list[str]:
        """
        Tokenize a single segment (either all letters or all non-letters).

        For letter segments, use learned tokens with greedy matching.
        For non-letter segments, split into individual characters.
        """
        if not segment:
            return []

        # Non-letter segments: each character is its own token
        if not self._is_letter(segment[0]):
            return list(segment)

        # Letter segments: use greedy tokenization with learned tokens
        return self._tokenize_word(segment)

    def _tokenize_word(self, word: str) -> list[str]:
        """
        Tokenize a word (all letters) greedily using known tokens.

        Always try to match the longest known token first.
        """
        if not word:
            return []

        # Try longest-first matching
        for length in range(len(word), 0, -1):
            token = word[:length]
            if self.is_token(token):
                rest = word[length:]
                return [token] + self._tokenize_word(rest)

        # This shouldn't happen if is_token works correctly
        return [word[0]] + self._tokenize_word(word[1:])

    def _count_letter_pairings(self, token_stream: list[str]) -> dict[str, int]:
        """
        Count adjacent pairings of tokens that are both letters.

        Only counts pairs where both tokens are purely alphabetic.
        This prevents creating tokens like " e" or "p!".
        """
        pairings = {}

        for idx in range(len(token_stream) - 1):
            current = token_stream[idx]
            next_token = token_stream[idx + 1]

            # Only count pairings where both are letter tokens
            if self._is_letter_token(current) and self._is_letter_token(next_token):
                pairing = current + next_token
                pairings[pairing] = pairings.get(pairing, 0) + 1

        return pairings

    def _is_letter_token(self, token: str) -> bool:
        """Check if a token contains only letters."""
        return len(token) > 0 and all(self._is_letter(char) for char in token)

    @staticmethod
    def _is_letter(char: str) -> bool:
        """Check if a character is a letter."""
        return char.isalpha()
