import html

class QuizBrain:
    """
    Manages the quiz logic, question flow, and scoring.
    
    Attributes:
        question_number (int): Current question index
        score (int): Current score
        question_list (list): List of Question objects
        current_question (Question): Current question object
    """
    
    def __init__(self, q_list):
        """
        Initialize the quiz with a list of questions.
        
        Args:
            q_list (list): List of Question objects
        """
        self.question_number = 0
        self.score = 0
        self.question_list = q_list
        self.current_question = None

    def still_has_questions(self):
        """Check if there are more questions remaining."""
        return self.question_number < len(self.question_list)

    def next_question(self):
        """
        Get the next question in the list.
        
        Returns:
            str: Formatted question text with number
        """
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        q_text = html.unescape(self.current_question.text)  # Decode HTML entities
        return f"Q.{self.question_number}: {q_text}"

    def check_answer(self, user_answer):
        """
        Check if the user's answer is correct.
        
        Args:
            user_answer (str): User's answer (True/False)
            
        Returns:
            bool: True if answer is correct, False otherwise
        """
        correct_answer = self.current_question.answer
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        return False