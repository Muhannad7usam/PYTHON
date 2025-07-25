class Question:
    """
    Models a quiz question with text and answer.
    
    Attributes:
        text (str): The question text
        answer (str): The correct answer (True/False)
    """
    
    def __init__(self, q_text, q_answer):
        """
        Initialize a new question.
        
        Args:
            q_text (str): The question text
            q_answer (str): The correct answer
        """
        self.text = q_text
        self.answer = q_answer