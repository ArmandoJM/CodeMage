# feedback.py

import json
from datetime import datetime

def save_feedback(data):
    """
    Saves feedback data to a JSON file.
    :param data: dict containing feedback data
    """
    filename = 'feedback.json'
    try:
        # Read existing feedback data
        with open(filename, 'r') as file:
            feedback_list = json.load(file)
    except FileNotFoundError:
        # If the file does not exist, start with an empty list
        feedback_list = []

    # Add timestamp to the feedback data
    data['timestamp'] = datetime.now().isoformat()

    # Append the new feedback data
    feedback_list.append(data)

    # Write updated feedback data back to the file
    with open(filename, 'w') as file:
        json.dump(feedback_list, file, indent=4)

def get_feedback():
    """
    Retrieves feedback data from the JSON file.
    """
    filename = 'feedback.json'
    try:
        with open(filename, 'r') as file:
            feedback_list = json.load(file)
        return feedback_list
    except FileNotFoundError:
        # If the file does not exist, return an empty list
        return []
