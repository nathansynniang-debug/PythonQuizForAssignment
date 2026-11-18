# Trivia Quiz

A desktop-based multiple-choice trivia quiz built with Python and Tkinter. The application presents 10 randomly selected questions, gives the player 60 seconds to complete the quiz, and displays a score with an answer-by-answer review.

## Features

- **Graphical interface:** A clean, dark-themed interface built with Tkinter.
- **Random questions:** Selects 10 different questions at random each time the quiz starts.
- **Four answer choices:** Each question has four options, selectable with radio buttons.
- **Navigation:** Move between questions using the Previous and Next buttons.
- **Answer tracking:** Previously selected answers are retained when navigating between questions.
- **Countdown timer:** Each quiz has a 60-second time limit. The timer changes colour as time runs low.
- **Automatic submission:** The quiz is submitted automatically when the timer reaches zero.
- **Results and review:** Displays the final score and shows the selected answer alongside the correct answer for every question.

## Requirements

- Python 3.8 or later recommended
- Tkinter (usually included with standard Python installations)

The application uses only Python's standard library:

- `tkinter` and `tkinter.messagebox` for the graphical interface and error dialogs
- `pathlib` for locating the question file
- `random` for selecting questions

No third-party packages are required.

## Project structure

Keep the question file in the same directory as the Python script:

```text
trivia-quiz/
├── trivia_quiz.py
└── trivia_questions.txt
```

The application looks for `trivia_questions.txt` in the directory containing `trivia_quiz.py`.

## Getting started

1. Make sure Python is installed.
2. Place `trivia_quiz.py` and `trivia_questions.txt` in the same folder.
3. Add at least 10 valid questions to `trivia_questions.txt` (see the format below).
4. Open a terminal in that folder.
5. Run:

   ```bash
   python trivia_quiz.py
   ```

   On some systems, use `python3 trivia_quiz.py` instead.

## Question file format

Each non-empty line in `trivia_questions.txt` represents one question. Use this format:

```text
Question|Option A|Option B|Option C|Option D|Correct option number
```

The correct option number must be an integer from **1 to 4**, corresponding to the four options in order.

### Example

```text
What is the capital of Japan?|Seoul|Tokyo|Beijing|Bangkok|2
Which planet is known as the Red Planet?|Earth|Venus|Mars|Jupiter|3
What is 5 multiplied by 6?|11|25|30|35|3
```

### Formatting rules

- Each question must contain exactly six fields separated by `|`: one question, four options, and one answer number.
- The answer number must be `1`, `2`, `3`, or `4`.
- Add at least **10 valid questions** to the file.
- Blank lines are ignored.
- Lines beginning with `#` are treated as comments and ignored.
- Do not use the `|` character inside a question or option because it is the field separator.
- Save the file as UTF-8 text.

## How to play

1. Launch the application.
2. Read the displayed question and select one of the four options.
3. Use **Next** to move forward and **Previous** to return to an earlier question.
4. Your selections are retained as you move between questions.
5. Select **Submit Quiz** when you are ready to finish. The quiz also submits automatically when the timer expires.
6. Review your score and the correct answers on the results screen.
7. Select **Close** to exit.

You can submit the quiz without answering every question. Unanswered questions are counted as incorrect and shown as **Not answered** in the review.

## Configuration

The quiz settings can be changed near the top of `trivia_quiz.py`:

```python
QUIZ_SECONDS = 60
QUESTIONS_PER_QUIZ = 10
```

- `QUIZ_SECONDS` sets the time limit in seconds.
- `QUESTIONS_PER_QUIZ` sets how many questions are selected for each quiz.

The question file must contain at least as many valid questions as the configured `QUESTIONS_PER_QUIZ` value.

## Error handling

The application displays an error dialog in these situations:

- **Missing question file:** `trivia_questions.txt` cannot be found beside the Python script.
- **Invalid question format:** A non-comment line does not contain exactly six fields.
- **Invalid answer number:** The correct-answer field is not an integer from 1 to 4.
- **Empty question file:** No valid questions are found.
- **Not enough questions:** The file contains fewer valid questions than the configured quiz length.

## Implementation overview

- `load_questions()` reads and validates the question file, then stores each question, its four options, and its correct answer.
- `Questionnaire` manages the quiz state, interface, navigation, timer, scoring, and results.
- `show_question()` displays the current question and restores any saved selection.
- `save_current_answer()` stores or clears the current selection.
- `update_timer()` updates the countdown once per second and changes its colour as the remaining time decreases.
- `submit_quiz()` stops the timer, calculates the score, and opens the results review.
- `show_results()` displays the score and the answer review.
