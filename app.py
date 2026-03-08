import os
import random
import streamlit as st

# FIX: Refactored core game logic into logic_utils.py with AI pair programming; UI stays here.
from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)

# Challenge 2 (Agent): High score persisted to file; path chosen so it works from project root.
HIGH_SCORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "high_score.txt")


def load_high_score():
    """Load best score from file; return 0 if file missing or invalid."""
    try:
        if os.path.isfile(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, "r", encoding="utf-8") as f:
                return int(f.read().strip())
    except (ValueError, OSError):
        pass
    return 0


def save_high_score(score: int):
    """Overwrite high score file with new best score."""
    try:
        with open(HIGH_SCORE_FILE, "w", encoding="utf-8") as f:
            f.write(str(score))
    except OSError:
        pass


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# Challenge 2 (Agent): High Score tracker — load once per session, show in sidebar.
if "high_score" not in st.session_state:
    st.session_state.high_score = load_high_score()
st.sidebar.metric("🏆 High Score", st.session_state.high_score)

# Challenge 2 (Agent): Guess History sidebar — visualize how close each guess was.
st.sidebar.subheader("Guess History")
secret_int = st.session_state.secret
if st.session_state.history:
    for i, g in enumerate(st.session_state.history):
        if isinstance(g, int):
            off = abs(g - secret_int)
            st.sidebar.caption(f"Guess {i + 1}: **{g}** — off by {off}")
        else:
            st.sidebar.caption(f"Guess {i + 1}: `{g}` (invalid)")
else:
    st.sidebar.caption("_No guesses yet._")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

# Challenge 4: Summary table data (attempt, guess, result, off-by) for session table.
if "history_details" not in st.session_state:
    st.session_state.history_details = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    st.session_state.history = []
    st.session_state.history_details = []
    # FIXME: Logic breaks here — New Game uses (1, 100) instead of current difficulty range (low, high)
    st.session_state.secret = random.randint(1, 100)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        # FIX: check_guess from logic_utils returns correct hint direction; verified with pytest.
        outcome, message = check_guess(guess_int, secret)
        secret_int_val = st.session_state.secret
        distance = abs(guess_int - secret_int_val)

        # Challenge 4: Store row for summary table (core logic unchanged).
        st.session_state.history_details.append({
            "Attempt": st.session_state.attempts,
            "Guess": guess_int,
            "Result": outcome,
            "Off by": distance,
        })

        if show_hint:
            # Challenge 4: Color-coded hints and Hot/Cold feedback.
            if outcome == "Win":
                st.success(message)
            elif outcome == "Too High":
                st.error(message)
            else:
                st.warning(message)
            if outcome != "Win":
                if distance <= 5:
                    st.caption("🔥 **Hot!** Very close.")
                elif distance <= 15:
                    st.caption("🌡️ **Warm**")
                else:
                    st.caption("❄️ **Cold**")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            # Challenge 2 (Agent): persist new high score to file when player beats it.
            if st.session_state.score > st.session_state.high_score:
                st.session_state.high_score = st.session_state.score
                save_high_score(st.session_state.high_score)
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# Challenge 4: Session summary table (does not change game logic).
if st.session_state.history_details:
    st.subheader("Session summary")
    st.dataframe(
        st.session_state.history_details,
        use_container_width=True,
        hide_index=True,
    )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
