# app/routes.py
from app import app  # Import the existing app instance
from flask import request, render_template, redirect, url_for, jsonify
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

    # After saving feedback, you might want to redirect to a thank you page or back to the index
    return render_template('index.html')  # or redirect(url_for('index'))


@app.route('/snippets')
def snippets():
    return render_template('snippets.html', snippets=get_snippets())


@app.route('/generate_code', methods=['POST'])
def generate_code():
    problem_description = request.form['problem_description']
    generated_code = get_code_from_llm(problem_description)

    # Instead of returning JSON, render the index template with the generated code.
    return render_template('index.html', submitted=True,
                           problem_description=problem_description, generated_code=generated_code)


def is_code_quality_acceptable(code):
    # Placeholder for actual quality check logic
    return len(code) > 20 and "function" in code


# Add a new route to handle saving the snippet after the user has reviewed it
@app.route('/save_snippet', methods=['POST'])
def save_snippet_route():
    # Extract problem description and generated code from the form submission
    problem_description = request.form['problem_description']
    generated_code = request.form['generated_code']

    # Save the snippet
    save_snippet(problem_description, generated_code)

    # Redirect to the snippets page or wherever you'd like after saving
    return redirect(url_for('snippets'))


@app.route('/delete_snippet/<int:snippet_id>')
def delete_snippet_route(snippet_id):
    delete_snippet(snippet_id)
    return redirect(url_for('snippets'))
