import requests
from random import shuffle


api = "https://opentdb.com/api.php"


# get the category_id and return the results in a list of dictionaries

def get_questions_from_api(category_id):
    param = {
        "category": category_id,
        "amount": 10,
        "type": "multiple"
    }
    results = []
    try:
        response = requests.get(api, params=param)
        data = response.json()["results"]
        for item in data:
            incorrect = list(item.get("incorrect_answers", "error"))
            incorrect.append(item.get("correct_answer", "error"))
            shuffle(incorrect)
            results.append(
                {
                    "question": item.get("question", "error"),
                    "category": item.get("category", "error"),
                    "difficulty": item.get("difficulty", "error"),
                    "correct_answer": item.get("correct_answer", "error"),
                    "all_answer": incorrect,
                }
            )


    except Exception as e:
        print(f"Error: {e}")

    return results




