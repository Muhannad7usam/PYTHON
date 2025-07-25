# ui.py
import tkinter as tk
from tkinter import font as tkfont
from quiz_brain import QuizBrain

# Modern color scheme
PRIMARY_COLOR = "#3A7CA5"
SECONDARY_COLOR = "#2F6690"
BACKGROUND_COLOR = "#F0F8FF"
TEXT_COLOR = "#16425B"
CORRECT_COLOR = "#4CAF50"
WRONG_COLOR = "#F44336"
BUTTON_HOVER = "#1A4D6E"

class QuizInterface:
    """
    Creates the graphical user interface for the quiz application.
    
    Attributes:
        quiz (QuizBrain): The quiz logic handler
        window (Tk): Main application window
        fonts (dict): Dictionary of font styles
    """
    
    def __init__(self, quiz_brain: QuizBrain):
        """
        Initialize the UI with quiz logic.
        
        Args:
            quiz_brain (QuizBrain): The quiz logic handler
        """
        self.quiz = quiz_brain
        
        # Window setup
        self.window = tk.Tk()
        self.window.title("QuizMaster")
        self.window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)
        self.window.geometry("450x550")
        self.window.resizable(False, False)
        
        # Font setup
        self.fonts = {
            "title": tkfont.Font(family="Helvetica", size=18, weight="bold"),
            "question": tkfont.Font(family="Helvetica", size=14),
            "button": tkfont.Font(family="Helvetica", size=12, weight="bold"),
            "score": tkfont.Font(family="Helvetica", size=12)
        }
        
        # Score display
        self.score_label = tk.Label(
            text="Score: 0",
            fg=TEXT_COLOR,
            bg=BACKGROUND_COLOR,
            font=self.fonts["score"]
        )
        self.score_label.grid(row=0, column=1, pady=(0, 20), sticky="e")
        
        # Question display
        self.canvas = tk.Canvas(
            width=400,
            height=250,
            bg="white",
            highlightthickness=0
        )
        self.question_text = self.canvas.create_text(
            200,
            125,
            width=380,
            text="Loading questions...",
            fill=TEXT_COLOR,
            font=self.fonts["question"],
            justify="center"
        )
        self.canvas.grid(row=1, column=0, columnspan=2, pady=(0, 30))
        
        # True button
        self.true_button = tk.Button(
            text="✓ True",
            command=self.true_pressed,
            bg=SECONDARY_COLOR,
            fg="white",
            activebackground=BUTTON_HOVER,
            activeforeground="white",
            font=self.fonts["button"],
            padx=30,
            pady=10,
            bd=0,
            highlightthickness=0,
            relief="flat"
        )
        self.true_button.grid(row=2, column=0, padx=10, sticky="ew")
        
        # False button
        self.false_button = tk.Button(
            text="✗ False",
            command=self.false_pressed,
            bg=SECONDARY_COLOR,
            fg="white",
            activebackground=BUTTON_HOVER,
            activeforeground="white",
            font=self.fonts["button"],
            padx=30,
            pady=10,
            bd=0,
            highlightthickness=0,
            relief="flat"
        )
        self.false_button.grid(row=2, column=1, padx=10, sticky="ew")
        
        # Configure grid weights
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        
        # Start with first question
        self.get_next_question()
        
        # Add hover effects
        self.add_button_hover()
        
        self.window.mainloop()
    
    def add_button_hover(self):
        """Add hover effects to buttons."""
        self.true_button.bind("<Enter>", lambda e: self.true_button.config(bg=BUTTON_HOVER))
        self.true_button.bind("<Leave>", lambda e: self.true_button.config(bg=SECONDARY_COLOR))
        self.false_button.bind("<Enter>", lambda e: self.false_button.config(bg=BUTTON_HOVER))
        self.false_button.bind("<Leave>", lambda e: self.false_button.config(bg=SECONDARY_COLOR))
    
    def get_next_question(self):
        """Display the next question or end quiz if complete."""
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            self.score_label.config(text=f"Score: {self.quiz.score}")
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text, text=q_text)
        else:
            self.canvas.itemconfig(
                self.question_text,
                text=f"Quiz Completed!\nFinal Score: {self.quiz.score}/{len(self.quiz.question_list)}"
            )
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")
    
    def true_pressed(self):
        """Handle True button press."""
        self.give_feedback(self.quiz.check_answer("True"))
    
    def false_pressed(self):
        """Handle False button press."""
        self.give_feedback(self.quiz.check_answer("False"))
    
    def give_feedback(self, is_correct):
        """
        Provide visual feedback for the answer.
        
        Args:
            is_correct (bool): Whether the answer was correct
        """
        if is_correct:
            self.canvas.config(bg=CORRECT_COLOR)
        else:
            self.canvas.config(bg=WRONG_COLOR)
        self.window.after(1000, self.get_next_question)