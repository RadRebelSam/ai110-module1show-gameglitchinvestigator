from logic_utils import check_guess, parse_guess


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert "Correct" in message


def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


def test_hint_direction_when_guess_too_high():
    """Targets the 'hints backwards' bug: when guess > secret, hint must say Go LOWER! (not Go HIGHER!)."""
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, "When guess is too high, hint should tell player to go LOWER"


def test_hint_direction_when_guess_too_low():
    """Targets the 'hints backwards' bug: when guess < secret, hint must say Go HIGHER! (not Go LOWER!)."""
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, "When guess is too low, hint should tell player to go HIGHER"


# --- Edge-case tests (Challenge 1): inputs that might break the game ---


def test_parse_guess_negative_number():
    """Edge case: negative input is parsed as int; game handles gracefully (e.g. always Too Low for positive secret)."""
    ok, value, err = parse_guess("-5")
    assert ok is True
    assert value == -5
    assert err is None
    outcome, _ = check_guess(-5, 50)
    assert outcome == "Too Low"


def test_parse_guess_decimal_truncated():
    """Edge case: decimal input is truncated to int; no crash, consistent behavior."""
    ok, value, err = parse_guess("33.7")
    assert ok is True
    assert value == 33
    assert err is None
    outcome, _ = check_guess(33, 50)
    assert outcome == "Too Low"


def test_parse_guess_very_large_value():
    """Edge case: extremely large value is accepted; check_guess still returns valid outcome."""
    ok, value, err = parse_guess("999999999")
    assert ok is True
    assert value == 999999999
    assert err is None
    outcome, message = check_guess(999999999, 50)
    assert outcome == "Too High"
    assert "LOWER" in message
