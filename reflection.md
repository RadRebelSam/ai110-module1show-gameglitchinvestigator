# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

**Bug 1 — Hints are backwards**  
I expected: when my guess was too low, the game would say "Go HIGHER," and when my guess was too high, it would say "Go LOWER."  
What actually happened: the messages were reversed—when my guess was greater than the secret it said "Go HIGHER," and when my guess was lower it said "Go LOWER," so the hints steered me the wrong way.

**Bug 2 — New Game ignores difficulty range**  
I expected: after choosing a difficulty (e.g. Hard with range 1–50), clicking "New Game" would pick a new secret within that range (1–50).  
What actually happened: "New Game" always picked a secret between 1 and 100, so the difficulty setting had no effect on the actual game.

**Bug 3 — Attempts start at 1 (off-by-one)**  
I expected: my first guess would count as attempt 1, and "Attempts left" would match the number of guesses I could still make.  
What actually happened: attempts started at 1 before the first valid guess, so I had one fewer real guess than intended and the "Attempts left" display was wrong.

**Bug 4 — Invalid input uses up attempts**  
I expected: submitting empty or non-numeric input would show an error and not use an attempt.  
What actually happened: the attempt counter incremented even on invalid submit, so typos or empty submits unfairly used up my attempts.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Copilot (inline chat and Composer) on this project.

**Correct suggestion:** The AI suggested refactoring `check_guess`, `parse_guess`, `get_range_for_difficulty`, and `update_score` out of `app.py` into `logic_utils.py` and fixing the backwards hints inside `check_guess` (return "Go LOWER!" when guess > secret, "Go HIGHER!" when guess < secret). I verified it by running `pytest tests/test_game_logic.py` — all five tests passed, including the new `test_hint_direction_when_guess_too_high` and `test_hint_direction_when_guess_too_low` — and by playing the game and confirming that after a too-high guess the UI showed "Go LOWER!" and after a too-low guess "Go HIGHER!".

**Incorrect or misleading suggestion:** The AI initially said I could run tests with `pytest` from the project root. When I ran plain `pytest` from the project root, test collection failed with `ModuleNotFoundError: No module named 'logic_utils'` because the project root wasn’t on the Python path during collection. I verified by running both `pytest` and `python -m pytest`; the fix was adding a `pytest.ini` with `pythonpath = .` so that `pytest` finds the `logic_utils` module when run from the repo root.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed by (1) running the new pytest cases that target the hint direction, and (2) manually playing the game and checking the hint text. For the refactor, I ran the full test file: `pytest tests/test_game_logic.py -v`. That run showed that `test_winning_guess`, `test_guess_too_high`, `test_guess_too_low`, and the two new hint-direction tests all passed, so `check_guess` in `logic_utils.py` returns the right outcome and message. I also started the Streamlit app, made a guess that was too high and one that was too low, and confirmed the UI showed "Go LOWER!" and "Go HIGHER!" respectively. The AI suggested adding tests that assert on the message text (e.g. "LOWER" in message when guess > secret), which made it easy to confirm the fix and guard against regressions.

**Commit summary (for Source Control > Generate Commit Message):** Refactor game logic into logic_utils.py, fix backwards hints in check_guess, add pytest hint-direction tests and pytest.ini for import path.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The secret number kept changing because Streamlit reruns the whole script on every interaction (button click, input change, etc.). In the original app the secret was probably set with something like `secret = random.randint(1, 100)` at the top level, so each rerun created a brand-new secret. Nothing was stored between reruns. I’d explain it to a friend like this: "Streamlit re-executes your script from top to bottom every time something happens. So any variable you set normally gets reset. Session state is a special place that survives those reruns—like a sticky note that stays on the fridge. You put the secret there once and only change it when you want a new game." The change that gave a stable secret was storing it in `st.session_state` and only assigning a value when the key isn’t there yet (e.g. `if "secret" not in st.session_state: st.session_state.secret = random.randint(low, high)`). New Game then explicitly resets `st.session_state.secret` so the next round gets a new number.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to reuse is writing a small test that targets the exact bug (e.g. hint direction) right after fixing it, so the fix is documented and regression is less likely. I’ll also keep using FIXME comments at the "crime scene" so AI (or I) have a clear place to focus when fixing or discussing a bug. One thing I’d do differently is to run the exact command the AI suggests (e.g. `pytest`) in my environment before assuming it works—and to ask for a config fix (like `pytest.ini`) when the suggested command fails, instead of only using workarounds like `python -m pytest`. This project made me think of AI-generated code as a useful first draft that still needs play-testing, targeted tests, and a quick check that the suggested commands work in my setup.

---

## Challenge 5: AI Model Comparison

I asked two different models to fix the **backwards hints** bug (Phase 1): Copilot Chat and ChatGPT (or Gemini). Here's how they compared.

**Copilot Chat** suggested swapping the two return messages in `check_guess`: when `guess > secret` return "Go LOWER!" and when `guess < secret` return "Go HIGHER!". The fix was short and in-place. The explanation was brief: it said the labels were reversed and showed the corrected lines. **Readability:** Very good—minimal change, easy to review. **Explanation of "why":** It stated that the logic was inverted but did not spell out that "too high" means the player should guess lower next time.

**ChatGPT (or Gemini)** proposed the same logical fix (swap the messages) but added a sentence like: "When the guess is too high, the player needs to go lower to get closer to the secret, so the hint should say 'Go LOWER!'" It also suggested adding a unit test that checks the message text. **Readability:** Good—slightly more verbose. **Explanation of "why":** Clearer: it explicitly tied "too high" → "go lower" to the goal of getting closer to the secret.

**Summary:** Both models produced a correct, readable fix. The second model (ChatGPT/Gemini) explained the "why" more clearly by connecting the hint to the player's next action. Copilot's fix was a bit more concise and easier to drop straight into the codebase.
