# snippets_manager.py
import json
import uuid
from datetime import datetime

SNIPPETS_FILE = 'snippets.json'


def save_snippet(problem_description, generated_code):
    try:
        with open(SNIPPETS_FILE, 'r') as file:
            snippets = json.load(file)
    except FileNotFoundError:
        snippets = []

    snippets.append({
        'id': str(uuid.uuid4()),
        'problem_description': problem_description,
        'generated_code': generated_code,
        'timestamp': datetime.now().isoformat()
    })

    with open(SNIPPETS_FILE, 'w') as file:
        json.dump(snippets, file, indent=4)


def get_snippets():
    try:
        with open(SNIPPETS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def delete_snippet(snippet_id):
    """Delete a snippet by its ID."""
    try:
        with open(SNIPPETS_FILE, 'r') as file:
            snippets = json.load(file)
        snippets = [snippet for snippet in snippets if snippet['id'] != snippet_id]
        with open(SNIPPETS_FILE, 'w') as file:
            json.dump(snippets, file, indent=4)
    except FileNotFoundError:
        pass



if __name__ == "__main__":
    # Replace these strings with actual data to simulate saving a snippet
    test_problem_description = "What is 2+2?"
    test_generated_code = "print(2+2)"
    save_snippet(test_problem_description, test_generated_code)