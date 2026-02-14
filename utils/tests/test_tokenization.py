"""Tests for the BPE tokenizer."""
from utils.src.tokenization import BPETokenizer


class TestBPETokenizerBasics:
    """Test basic tokenizer functionality."""

    def test_init(self):
        """Tokenizer initializes with empty token set."""
        tokenizer = BPETokenizer()
        assert tokenizer.tokens == set()

    def test_add_token(self):
        """Can add tokens to the tokenizer."""
        tokenizer = BPETokenizer()
        tokenizer.add_token("th")
        assert "th" in tokenizer.tokens

    def test_is_token_single_char(self):
        """Single characters are always valid tokens."""
        tokenizer = BPETokenizer()
        assert tokenizer.is_token("a")
        assert tokenizer.is_token("Z")
        assert tokenizer.is_token(" ")
        assert tokenizer.is_token("!")

    def test_is_token_multi_char_learned(self):
        """Multi-char tokens must be learned."""
        tokenizer = BPETokenizer()
        assert not tokenizer.is_token("th")
        tokenizer.add_token("th")
        assert tokenizer.is_token("th")

    def test_is_token_multi_char_not_learned(self):
        """Unknown multi-char tokens return False."""
        tokenizer = BPETokenizer()
        assert not tokenizer.is_token("xyz")


class TestBreakIntoSegments:
    """Test the segment breaking logic."""

    def test_break_simple_word(self):
        """Break simple word into one segment."""
        tokenizer = BPETokenizer()
        segments = tokenizer._break_into_segments("hello")
        assert segments == ["hello"]

    def test_break_word_with_space(self):
        """Break word and space into separate segments."""
        tokenizer = BPETokenizer()
        segments = tokenizer._break_into_segments("hello world")
        assert segments == ["hello", " ", "world"]

    def test_break_word_with_punctuation(self):
        """Break word and punctuation into separate segments."""
        tokenizer = BPETokenizer()
        segments = tokenizer._break_into_segments("hello,")
        assert segments == ["hello", ","]

    def test_break_multiple_spaces(self):
        """Multiple spaces are grouped into one segment."""
        tokenizer = BPETokenizer()
        segments = tokenizer._break_into_segments("a  b")
        assert segments == ["a", "  ", "b"]

    def test_break_complex_string(self):
        """Break complex string with mixed content."""
        tokenizer = BPETokenizer()
        segments = tokenizer._break_into_segments("hi! how?")
        assert segments == ["hi", "! ", "how", "?"]

    def test_break_emoji(self):
        """Emoji are separate segments."""
        tokenizer = BPETokenizer()
        segments = tokenizer._break_into_segments("hello🦑world")
        assert segments == ["hello", "🦑", "world"]

    def test_break_empty_string(self):
        """Empty string returns empty list."""
        tokenizer = BPETokenizer()
        assert tokenizer._break_into_segments("") == []


class TestTokenizeSegment:
    """Test tokenization of individual segments."""

    def test_tokenize_letter_segment_no_tokens(self):
        """Letter segment splits into characters with no learned tokens."""
        tokenizer = BPETokenizer()
        result = tokenizer._tokenize_segment("hello")
        assert result == ["h", "e", "l", "l", "o"]

    def test_tokenize_letter_segment_with_token(self):
        """Letter segment uses learned tokens."""
        tokenizer = BPETokenizer()
        tokenizer.add_token("he")
        result = tokenizer._tokenize_segment("hello")
        assert result == ["he", "l", "l", "o"]

    def test_tokenize_letter_segment_multiple_tokens(self):
        """Letter segment uses multiple learned tokens."""
        tokenizer = BPETokenizer()
        tokenizer.add_token("he")
        tokenizer.add_token("ll")
        result = tokenizer._tokenize_segment("hello")
        assert result == ["he", "ll", "o"]

    def test_tokenize_nonletter_segment(self):
        """Non-letter segment splits into individual characters."""
        tokenizer = BPETokenizer()
        result = tokenizer._tokenize_segment("!!??")
        assert result == ["!", "!", "?", "?"]

    def test_tokenize_space_segment(self):
        """Space segment splits into individual spaces."""
        tokenizer = BPETokenizer()
        result = tokenizer._tokenize_segment("   ")
        assert result == [" ", " ", " "]

    def test_tokenize_empty_segment(self):
        """Empty segment returns empty list."""
        tokenizer = BPETokenizer()
        assert tokenizer._tokenize_segment("") == []


class TestTokenize:
    """Test full tokenization."""

    def test_tokenize_single_word(self):
        """Tokenize a single word."""
        tokenizer = BPETokenizer()
        tokens = tokenizer.tokenize("hello")
        assert tokens == ["h", "e", "l", "l", "o"]

    def test_tokenize_sentence(self):
        """Tokenize a sentence."""
        tokenizer = BPETokenizer()
        tokens = tokenizer.tokenize("hi there")
        assert tokens == ["h", "i", " ", "t", "h", "e", "r", "e"]

    def test_tokenize_with_punctuation(self):
        """Tokenize respects punctuation boundaries."""
        tokenizer = BPETokenizer()
        tokens = tokenizer.tokenize("hello!")
        assert tokens == ["h", "e", "l", "l", "o", "!"]

    def test_tokenize_with_learned_tokens(self):
        """Tokenize uses learned tokens."""
        tokenizer = BPETokenizer()
        tokenizer.add_token("he")
        tokenizer.add_token("ll")
        tokens = tokenizer.tokenize("hello")
        assert tokens == ["he", "ll", "o"]

    def test_tokenize_mixed_content(self):
        """Tokenize complex text with mixed content."""
        tokenizer = BPETokenizer()
        tokenizer.add_token("th")
        tokens = tokenizer.tokenize("th: ok!")
        assert tokens == ["th", ":", " ", "o", "k", "!"]

    def test_tokenize_never_mixes_letters_nonletters(self):
        """Learned tokens never contain both letters and non-letters."""
        tokenizer = BPETokenizer()
        # Add a token that would span letter/non-letter boundary
        # (this shouldn't happen naturally, but ensure it can't cause issues)
        tokenizer.add_token("o ")
        tokens = tokenizer.tokenize("hello world")
        # The space breaks the segments, so "o " is never created
        assert " " in tokens  # Space is always its own token


class TestCountLetterPairings:
    """Test the pairing count logic."""

    def test_count_basic_pairing(self):
        """Count simple letter pairings."""
        tokenizer = BPETokenizer()
        tokens = ["h", "e", "l", "l", "o"]
        counts = tokenizer._count_letter_pairings(tokens)
        assert counts == {"he": 1, "el": 1, "ll": 1, "lo": 1}

    def test_count_repeated_pairing(self):
        """Count repeated pairings."""
        tokenizer = BPETokenizer()
        tokens = ["p", "e", "p", "p", "e", "r"]
        counts = tokenizer._count_letter_pairings(tokens)
        assert counts["pe"] == 2
        assert counts["pp"] == 1
        assert counts["er"] == 1

    def test_count_ignores_nonletter_pairings(self):
        """Don't count pairings with non-letter tokens."""
        tokenizer = BPETokenizer()
        tokens = ["h", "i", " ", "t", "h", "e", "r", "e"]
        counts = tokenizer._count_letter_pairings(tokens)
        # " t" should not be counted
        assert " t" not in counts
        # "i " should not be counted
        assert "i " not in counts
        # But letter-only pairings should be
        assert "hi" in counts
        assert "th" in counts

    def test_count_no_pairings(self):
        """Return empty dict when no letter pairings."""
        tokenizer = BPETokenizer()
        tokens = ["!", "@", " "]
        counts = tokenizer._count_letter_pairings(tokens)
        assert counts == {}

    def test_count_mixed_content(self):
        """Count only letter pairings in mixed content."""
        tokenizer = BPETokenizer()
        tokens = ["t", "h", ":", " ", "o", "k", "!"]
        counts = tokenizer._count_letter_pairings(tokens)
        assert "th" in counts
        assert "ok" in counts
        assert "h:" not in counts
        assert ": " not in counts
        assert "k!" not in counts


class TestLearnFromText:
    """Test the learning process."""

    def test_learn_one_iteration(self):
        """Learn one iteration discovers a pairing."""
        tokenizer = BPETokenizer()
        tokenizer.learn_from_text("hello", iterations=1)
        # Should learn one of the most common pairings
        # From "h,e,l,l,o" all pairings appear once, so any could be learned
        assert len(tokenizer.tokens) == 1
        learned_token = list(tokenizer.tokens)[0]
        assert learned_token in ["he", "el", "ll", "lo"]

    def test_learn_multiple_iterations(self):
        """Learn multiple iterations."""
        tokenizer = BPETokenizer()
        tokenizer.learn_from_text("hello world", iterations=3)
        # Should learn multiple tokens
        assert len(tokenizer.tokens) >= 1

    def test_learn_recognizes_learned_tokens(self):
        """Subsequent iterations use previously learned tokens."""
        tokenizer = BPETokenizer()
        tokenizer.learn_from_text("peter piper", iterations=2)
        # After learning, tokenization should be different
        tokens_iter2 = tokenizer.tokenize("peter piper")
        # Verify some tokens were learned (not all single chars)
        multi_char_tokens = [t for t in tokens_iter2 if len(t) > 1]
        assert len(multi_char_tokens) > 0

    def test_learn_respects_letter_boundaries(self):
        """Learning never creates tokens that cross letter/non-letter boundaries."""
        tokenizer = BPETokenizer()
        tokenizer.learn_from_text("hello, world!", iterations=5)
        # All tokens should be either all-letter or all-non-letter
        for token in tokenizer.tokens:
            is_letter = all(c.isalpha() for c in token)
            is_nonletter = all(not c.isalpha() for c in token)
            assert is_letter or is_nonletter, f"Token '{token}' mixes letters and non-letters"

    def test_learn_no_pairings_stops_gracefully(self):
        """Learning stops gracefully when no more pairings found."""
        tokenizer = BPETokenizer()
        # Single character - no pairings possible
        tokenizer.learn_from_text("a", iterations=10)
        # Should not crash
        assert len(tokenizer.tokens) == 0


class TestRealWorldExample:
    """Test with realistic text."""

    def test_learn_and_tokenize_sentence(self):
        """Full workflow: learn from text, then tokenize it."""
        tokenizer = BPETokenizer()
        text = "Peter Piper picked a peck of pickled peppers"
        
        tokenizer.learn_from_text(text, iterations=6)
        tokens = tokenizer.tokenize(text)
        
        # Should have learned some common patterns
        assert len(tokenizer.tokens) > 0
        # Should be able to tokenize the text
        assert len(tokens) > 0
        # All tokens should be reconstitutable
        reconstructed = "".join(tokens)
        assert reconstructed == text

    def test_learned_tokens_improve_compression(self):
        """Learned tokens reduce the total token count."""
        text = "Peter Piper picked a peck of pickled peppers"
        
        tokenizer1 = BPETokenizer()
        tokens1 = tokenizer1.tokenize(text)
        count1 = len(tokens1)
        
        tokenizer2 = BPETokenizer()
        tokenizer2.learn_from_text(text, iterations=6)
        tokens2 = tokenizer2.tokenize(text)
        count2 = len(tokens2)
        
        # Learned tokens should reduce count
        assert count2 < count1

    def test_consistency_across_runs(self):
        """Tokenization is consistent."""
        tokenizer = BPETokenizer()
        tokenizer.learn_from_text("hello world", iterations=2)
        
        tokens1 = tokenizer.tokenize("hello world")
        tokens2 = tokenizer.tokenize("hello world")
        
        assert tokens1 == tokens2
