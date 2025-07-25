# main.py
from question_model import Question
from data import question_data
from quiz_brain import QuizBrain
from ui import QuizInterface

def create_question_bank():
    """
    Create a list of Question objects from the question data.
    
    Returns:
        list: List of Question objects
    """
    question_bank = []
    for question in question_data:
        new_question = Question(
            question["question"],
            question["correct_answer"]
        )
        question_bank.append(new_question)
    return question_bank

def main():
    """Initialize and run the quiz application."""
    question_bank = create_question_bank()
    quiz = QuizBrain(question_bank)
    quiz_ui = QuizInterface(quiz)  # This starts the GUI application

if __name__ == "__main__":
    main()