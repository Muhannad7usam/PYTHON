import requests

def get_question_data():
    """
    Fetches trivia questions from the OpenTDB API.
    Returns a list of question dictionaries or default questions if API fails.
    """
    parameters = {
        "amount": 10,
        "type": "boolean",
    }
    
    try:
        response = requests.get("https://opentdb.com/api.php", 
                              params=parameters, 
                              timeout=5)
        response.raise_for_status()
        data = response.json()
        return data["results"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching questions: {e}")
        return [
            {"question": "The Earth is flat.", "correct_answer": "False"},
            {"question": "Python is a compiled language.", "correct_answer": "False"},
            {"question": "The Great Wall of China is visible from space.", "correct_answer": "False"},
            {"question": "The sun revolves around the Earth.", "correct_answer": "False"},
            {"question": "Water boils at 100 degrees Fahrenheit.", "correct_answer": "False"},
            {"question": "The human body has four lungs.", "correct_answer": "False"},
            {"question": "The capital of France is London.", "correct_answer": "False"},
            {"question": "Light travels faster than sound.", "correct_answer": "True"},
            {"question": "The currency of Japan is the Yuan.", "correct_answer": "False"},
            {"question": "Mount Everest is the tallest mountain in the world.", "correct_answer": "True"}
        ]

question_data = get_question_data()