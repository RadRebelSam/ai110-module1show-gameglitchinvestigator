# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- **Game's purpose:** A number-guessing game where the player picks a difficulty (Easy 1–20, Normal 1–100, Hard 1–50), gets a limited number of attempts, and receives higher/lower hints until they win or run out of tries. Score changes based on outcome and attempt count.
- **Bugs found:** (1) Hints were backwards (too high showed "Go HIGHER!", too low showed "Go LOWER!"); (2) New Game always used range 1–100 instead of the selected difficulty range; (3) attempts started at 1 before the first guess (off-by-one); (4) invalid input (empty or non-numeric) still consumed an attempt.
- **Fixes applied:** Refactored core logic (`check_guess`, `parse_guess`, `get_range_for_difficulty`, `update_score`) into `logic_utils.py` and fixed hint direction in `check_guess` (too high → "Go LOWER!", too low → "Go HIGHER!"). Added pytest tests for hint direction and `pytest.ini` so `pytest` finds `logic_utils` from the project root. The app uses `st.session_state` for the secret so it stays stable across reruns.

**Write Reflection:** Complete the questions in `reflection.md` (what was broken, how you used AI, debugging and testing, Streamlit and state, and habits going forward).

## 📸 Demo

- Run the app: `python -m streamlit run app.py`. Choose a difficulty, use the Developer Debug Info to see the secret if needed, then win by following the corrected hints ("Go LOWER!" when too high, "Go HIGHER!" when too low).
- [ ] [Insert a screenshot of your fixed, winning game here]

---

## Challenge 1: Advanced Edge-Case Testing

Three edge-case inputs are covered by pytest: **negative numbers** (e.g. `-5`), **decimals** (e.g. `33.7`, truncated to int), and **very large values** (e.g. `999999999`). The suite verifies that `parse_guess` and `check_guess` handle these without crashing and with consistent behavior. Run:

```bash
pytest tests/test_game_logic.py -v
```

**Screenshot:** Add a screenshot below showing the terminal with the `pytest` command and all tests passing (e.g. 8 passed).

- [ ] [Insert screenshot: `pytest tests/test_game_logic.py -v` with test results here]

---

## Challenge 2: Feature Expansion (Agent Mode)

**High Score tracker:** The best score is saved to `high_score.txt` in the project directory and loaded on startup. When you win with a score higher than the stored value, it is updated and shown in the sidebar metric "🏆 High Score".

**Guess History sidebar:** The sidebar shows "Guess History" with each guess and how far it was from the secret ("off by X"). Invalid inputs are listed as well. History is cleared when you click "New Game".

The agent contributed by proposing the file path for `high_score.txt` (using `os.path.dirname(os.path.abspath(__file__))` so it works when running from the project root), the structure of `load_high_score` / `save_high_score`, and the sidebar layout for Guess History (enumerating `st.session_state.history` and computing distance from the current secret). See comments in `app.py` marked "Challenge 2 (Agent)".

---

## Challenge 3: Documentation and Linting

- **Docstrings:** Every function in `logic_utils.py` has a professional-style docstring (module summary, Args, Returns, and brief description). Generated with the "Generate documentation" smart action and then refined.
- **PEP 8:** The code was reviewed for style (line length, naming, spacing). Fixes included a module-level docstring, consistent return type hints, and removal of redundant `else` after `return`.

---

## Challenge 4: Enhanced Game UI

- **Color-coded hints:** Win → green (`st.success`), Too High → red (`st.error`), Too Low → orange (`st.warning`).
- **Hot/Cold feedback:** After each non-winning guess, a caption shows 🔥 **Hot!** (off by ≤5), 🌡️ **Warm** (off by ≤15), or ❄️ **Cold** (otherwise).
- **Session summary table:** A "Session summary" dataframe lists each attempt with columns Attempt, Guess, Result, and Off by. It appears once you have at least one valid guess and does not change core game logic.

**Screenshot:** Add a screenshot of the enhanced player experience (hints, hot/cold, and summary table visible).

- [ ] [Insert a screenshot of your Enhanced Game UI here]

---

## 🚀 Stretch Features

- [ ] [If you complete additional stretch work, add a screenshot or link here.]
