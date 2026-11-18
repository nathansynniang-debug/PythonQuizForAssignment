import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import random

# Keep trivia_questions.txt in the same folder as this Python file.
QUESTION_FILE = Path(__file__).with_name("trivia_questions.txt")
QUIZ_SECONDS = 60
QUESTIONS_PER_QUIZ = 10

# Modern dark theme
BG = "#111827"
PANEL = "#1F2937"
PANEL_LIGHT = "#273449"
FG = "#F9FAFB"
MUTED = "#9CA3AF"
ACCENT = "#8B5CF6"
ACCENT_HOVER = "#7C3AED"
GREEN = "#34D399"
RED = "#F87171"

TITLE_FONT = ("Segoe UI", 22, "bold")
QUESTION_FONT = ("Segoe UI", 15, "bold")
BODY_FONT = ("Segoe UI", 11)
SMALL_FONT = ("Segoe UI", 10)


def load_questions(filename):
    """Read questions, four options and the correct option number from a text file."""
    questions = []
    with open(filename, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split("|")
            if len(parts) != 6:
                raise ValueError(
                    f"Line {line_number}: expected a question, four options and an answer."
                )

            question, *rest = parts
            options = rest[:4]
            correct = int(rest[4])

            if correct not in range(1, 5):
                raise ValueError(f"Line {line_number}: answer must be from 1 to 4.")

            questions.append({
                "question": question,
                "options": options,
                "answer": correct - 1  # Store answer as index 0-3.
            })

    if not questions:
        raise ValueError("The question file does not contain any questions.")
    return questions


class Questionnaire:
    def __init__(self):
        all_questions = load_questions(QUESTION_FILE)
        if len(all_questions) < QUESTIONS_PER_QUIZ:
            raise ValueError(
                f"The question file must contain at least {QUESTIONS_PER_QUIZ} questions."
            )

        # Pick 10 different questions at random each time the quiz starts.
        self.questions = random.sample(all_questions, QUESTIONS_PER_QUIZ)
        self.total_questions = len(self.questions)
        self.current_question = 0

        # Dictionary: question index -> selected option index.
        self.user_answers = {}

        self.time_left = QUIZ_SECONDS
        self.timer_job = None
        self.submitted = False

        self.root = tk.Tk()
        self.root.title("Trivia Quiz")
        self.root.geometry("720x600")
        self.root.minsize(620, 540)
        self.root.configure(bg=BG)

        self.selected_option = tk.IntVar(value=-1)
        self.option_buttons = []

        self.build_interface()
        self.show_question()
        self.update_timer()
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.root.mainloop()

    def build_interface(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=30, pady=(22, 12))

        tk.Label(
            header, text="TRIVIA TIME", font=TITLE_FONT,
            bg=BG, fg=FG
        ).pack(side="left")

        self.timer_label = tk.Label(
            header, text="01:00", font=("Segoe UI", 15, "bold"),
            bg=PANEL, fg=GREEN, padx=16, pady=8
        )
        self.timer_label.pack(side="right")

        self.progress_label = tk.Label(
            self.root, text="", font=SMALL_FONT, bg=BG, fg=MUTED
        )
        self.progress_label.pack(anchor="w", padx=34, pady=(8, 5))

        self.progress_bar = tk.Canvas(
            self.root, height=6, bg=PANEL, highlightthickness=0
        )
        self.progress_bar.pack(fill="x", padx=30, pady=(0, 18))

        self.card = tk.Frame(self.root, bg=PANEL, padx=25, pady=24)
        self.card.pack(fill="both", expand=True, padx=30, pady=4)

        self.question_label = tk.Label(
            self.card, text="", font=QUESTION_FONT,
            bg=PANEL, fg=FG, wraplength=600, justify="left",
            anchor="w"
        )
        self.question_label.pack(fill="x", pady=(0, 22))

        for i in range(4):
            rb = tk.Radiobutton(
                self.card,
                text="",
                variable=self.selected_option,
                value=i,
                font=BODY_FONT,
                bg=PANEL_LIGHT,
                fg=FG,
                activebackground=PANEL_LIGHT,
                activeforeground=FG,
                selectcolor=ACCENT,
                indicatoron=True,
                anchor="w",
                justify="left",
                padx=14,
                pady=11,
                wraplength=560,
                cursor="hand2",
                highlightthickness=0
            )
            rb.pack(fill="x", pady=5)
            self.option_buttons.append(rb)

        navigation = tk.Frame(self.root, bg=BG)
        navigation.pack(fill="x", padx=30, pady=20)

        self.previous_button = tk.Button(
            navigation, text="← Previous", command=self.previous_question,
            font=BODY_FONT, bg=PANEL_LIGHT, fg=FG,
            activebackground=PANEL, activeforeground=FG,
            relief="flat", padx=18, pady=10, cursor="hand2"
        )
        self.previous_button.pack(side="left")

        self.submit_button = tk.Button(
            navigation, text="Submit Quiz", command=self.submit_quiz,
            font=BODY_FONT, bg=GREEN, fg="#052E2B",
            activebackground="#10B981", relief="flat",
            padx=18, pady=10, cursor="hand2"
        )
        self.submit_button.pack(side="right")

        self.next_button = tk.Button(
            navigation, text="Next →", command=self.next_question,
            font=BODY_FONT, bg=ACCENT, fg="white",
            activebackground=ACCENT_HOVER, relief="flat",
            padx=22, pady=10, cursor="hand2"
        )
        self.next_button.pack(side="right", padx=10)

    def save_current_answer(self):
        """Save the selected radio-button value for the current question."""
        selected = self.selected_option.get()
        if selected != -1:
            self.user_answers[self.current_question] = selected
        else:
            self.user_answers.pop(self.current_question, None)

    def show_question(self):
        question_data = self.questions[self.current_question]
        self.question_label.config(text=question_data["question"])

        for i, option in enumerate(question_data["options"]):
            self.option_buttons[i].config(text=f"{chr(65 + i)}.  {option}")

        # Restore the answer previously selected for this question.
        self.selected_option.set(
            self.user_answers.get(self.current_question, -1)
        )

        self.progress_label.config(
            text=f"QUESTION {self.current_question + 1} OF {self.total_questions}"
        )
        self.progress_bar.delete("all")
        width = self.progress_bar.winfo_width()
        if width <= 1:
            width = 660
        progress = width * (self.current_question + 1) / self.total_questions
        self.progress_bar.create_rectangle(
            0, 0, progress, 6, fill=ACCENT, outline=""
        )

        self.previous_button.config(
            state="normal" if self.current_question > 0 else "disabled"
        )
        self.next_button.config(
            state="normal" if self.current_question < self.total_questions - 1
            else "disabled"
        )

    def next_question(self):
        if self.submitted:
            return
        self.save_current_answer()
        if self.current_question < self.total_questions - 1:
            self.current_question += 1
            self.show_question()

    def previous_question(self):
        if self.submitted:
            return
        self.save_current_answer()
        if self.current_question > 0:
            self.current_question -= 1
            self.show_question()

    def update_timer(self):
        if self.submitted:
            return

        minutes, seconds = divmod(self.time_left, 60)
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

        if self.time_left <= 10:
            self.timer_label.config(fg=RED)
        elif self.time_left <= 30:
            self.timer_label.config(fg="#FBBF24")
        else:
            self.timer_label.config(fg=GREEN)

        if self.time_left == 0:
            self.submit_quiz(time_expired=True)
            return

        self.time_left -= 1
        self.timer_job = self.root.after(1000, self.update_timer)

    def submit_quiz(self, time_expired=False):
        if self.submitted:
            return

        self.save_current_answer()
        self.submitted = True

        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        score = sum(
            1 for index, question in enumerate(self.questions)
            if self.user_answers.get(index) == question["answer"]
        )

        self.show_results(score, time_expired)

    def show_results(self, score, time_expired):
        for widget in self.root.winfo_children():
            widget.destroy()

        heading = "Time's up!" if time_expired else "Quiz completed!"
        tk.Label(
            self.root, text=heading, font=TITLE_FONT, bg=BG, fg=FG
        ).pack(pady=(25, 5))

        tk.Label(
            self.root,
            text=f"Your score: {score} / {self.total_questions}",
            font=("Segoe UI", 19, "bold"), bg=BG, fg=GREEN
        ).pack(pady=(0, 15))

        review_frame = tk.Frame(self.root, bg=PANEL)
        review_frame.pack(fill="both", expand=True, padx=25, pady=10)

        # Scrollable answer review
        canvas = tk.Canvas(review_frame, bg=PANEL, highlightthickness=0)
        scrollbar = tk.Scrollbar(review_frame, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=PANEL)

        inner.bind(
            "<Configure>",
            lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas_window = canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(canvas_window, width=event.width)
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=(12, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 8), pady=10)

        for i, question in enumerate(self.questions):
            chosen = self.user_answers.get(i)
            correct = question["answer"]
            is_correct = chosen == correct

            status = "✓ Correct" if is_correct else "✗ Incorrect"
            colour = GREEN if is_correct else RED

            tk.Label(
                inner, text=f"{i + 1}. {question['question']}",
                font=("Segoe UI", 10, "bold"), bg=PANEL, fg=FG,
                wraplength=590, justify="left", anchor="w"
            ).pack(fill="x", padx=12, pady=(10, 2))

            chosen_text = (
                question["options"][chosen] if chosen is not None
                else "Not answered"
            )
            correct_text = question["options"][correct]

            tk.Label(
                inner,
                text=f"{status}  |  Your answer: {chosen_text}  |  Correct answer: {correct_text}",
                font=SMALL_FONT, bg=PANEL, fg=colour,
                wraplength=590, justify="left", anchor="w"
            ).pack(fill="x", padx=12, pady=(0, 8))

        tk.Button(
            self.root, text="Close", command=self.root.destroy,
            font=BODY_FONT, bg=ACCENT, fg="white",
            activebackground=ACCENT_HOVER, relief="flat",
            padx=25, pady=9, cursor="hand2"
        ).pack(pady=(5, 20))

    def close_window(self):
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
        self.root.destroy()


if __name__ == "__main__":
    try:
        Questionnaire()
    except FileNotFoundError:
        messagebox.showerror(
            "Missing file",
            f"Could not find {QUESTION_FILE.name}. Keep it in the same folder as this Python file."
        )
    except ValueError as error:
        messagebox.showerror("Question file error", str(error))
