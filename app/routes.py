# app/routes.py
import json
import re
from app import app  # Import the existing app instance
from flask import request, render_template, redirect, url_for
from markupsafe import escape
from model.llm_handler import get_code_from_llm
from feedback.feedback import save_feedback  # import the feedback functions
# Import the snippets_manager functions at the top
from snippets.snippets_manager import get_snippets, delete_snippet, save_snippet


# No need to create a new Flask app here

@app.route('/', methods=['GET', 'POST'])
def index():
    problem_description = ''
    generated_code = ''
    submitted = False
    if request.method == 'POST':
        problem_description = request.form.get('problem_description', '')
        generated_code = get_code_from_llm(problem_description)
        # Save the snippet when the code is generated
        submitted = True  # Set to True after generating the code
        save_snippet(problem_description, generated_code)
    return render_template('index.html', submitted=request.method == 'POST',
                           problem_description=problem_description, generated_code=generated_code)


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback_data = {
        'problem_description': request.form['problem_description'],
        'generated_code': request.form['generated_code'],
        'feedback': request.form['feedback']
    }
    save_feedback(feedback_data)

    return redirect(url_for('show_generated_code'))


@app.route('/snippets', methods=['GET'])
def snippets():
    snippets = get_snippets()
    return render_template('snippets.html', snippets=snippets)


@app.route('/generate_code', methods=['POST'])
def generate_code():
    problem_description = escape(request.form['problem_description'])
    # Validate input format (optional)
    if not re.match(r'^[a-zA-Z0-9\s]+$', problem_description):
        return 'Invalid input format'
    generated_code = get_code_from_llm(problem_description)

    # Instead of returning JSON, render the index template with the generated code.
    return render_template('index.html', submitted=True,
                           problem_description=problem_description, generated_code=generated_code)


def execute_safe_code_generation(problem_description):
    # Execute code generation in a safe environment
    # Example: using ast.literal_eval() for safe evaluation
    return "Generated code for: " + problem_description


def is_code_quality_acceptable(code):
    # Placeholder for actual quality check logic
    return len(code) > 20 and "function" in code


@app.route('/snippets')
def list_snippets():
    """List all snippets."""
    snippets = get_snippets()
    return render_template('snippets.html', snippets=snippets)


# Add a new route to handle saving the snippet after the user has reviewed it
@app.route('/save_snippet', methods=['POST'])
def save_snippet_route():
    # Extract problem description and generated code from the form submission
    problem_description = request.form['problem_description']
    generated_code = request.form['generated_code']

    # Save the snippet using the snippets_manager function
    save_snippet(problem_description, generated_code)

    # Redirect the user to the snippet list
    return redirect(url_for('snippets'))


@app.route('/delete_snippet/<snippet_id>', methods=['POST', 'DELETE'])
def delete_snippet_route(snippet_id):
    # Convert snippet_id to the appropriate data type if needed
    # To Perform the deletion logic here
    return redirect(url_for('snippets'))


@app.route('/show_generated_code')
def show_generated_code():
    # Get the last feedback entry from feedback.json (or wherever feedback is stored)
    try:
        with open('feedback.json', 'r') as file:
            feedbacks = json.load(file)
        last_feedback = feedbacks[-1]  # Assuming the newest feedback is at the end of the list
    except (FileNotFoundError, IndexError):  # Handle if the file is missing or empty
        last_feedback = {'problem_description': '', 'generated_code': '', 'feedback': ''}

    # Pass the data to the template
    return render_template(
        'show_generated_code.html',
        problem_description=last_feedback['problem_description'],
        generated_code=last_feedback['generated_code'],
        feedback=last_feedback['feedback']
    )




if __name__ == '__main__':
    app.run(debug=True)
