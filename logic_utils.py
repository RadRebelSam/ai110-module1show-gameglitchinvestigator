"""Game logic for the number-guessing game (range, parsing, comparison, scoring)."""


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive (low, high) guess range for a given difficulty.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard".

    Returns:
        A 2-tuple (low, high) of integers. Easy: (1, 20),
        Normal: (1, 100), Hard: (1, 50). Unknown defaults to (1, 100).
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str) -> tuple[bool, int | None, str | None]:
    """Parse user input into a numeric guess.

    Accepts integers and decimals (truncated to int). Rejects None, empty
    string, and non-numeric input with an error message.

    Args:
        raw: The user's raw input string (or None).

    Returns:
        A 3-tuple (ok, value, error_message). If ok is True, value is the
        parsed int and error_message is None. If ok is False, value is None
        and error_message is a short string for the user.
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """Compare guess to secret and return outcome plus user-facing message.

    Args:
        guess: The player's guess (integer).
        secret: The target number (integer).

    Returns:
        A 2-tuple (outcome, message). outcome is one of "Win", "Too High",
        or "Too Low". message is a hint string (e.g. "Go LOWER!" when too high).
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        # FIX: Hint direction corrected with AI pair programming.
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g, s = str(guess), str(secret)
        if g == s:
            return "Win", "🎉 Correct!"
        if int(g) > int(s):
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


def update_score(
    current_score: int,
    outcome: str,
    attempt_number: int,
) -> int:
    """Update running score based on guess outcome and attempt number.

    Win: adds points (higher for fewer attempts, minimum 10). Too High / Too
    Low: adds or subtracts 5 depending on attempt parity.

    Args:
        current_score: The score before this update.
        outcome: One of "Win", "Too High", or "Too Low".
        attempt_number: The 1-based attempt index for this guess.

    Returns:
        The new score after applying this outcome.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
