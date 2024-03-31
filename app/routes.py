# app/routes.py
from app import app  # Import the existing app instance
from flask import request, render_template,redirect, url_for
from model.llm_handler import get_code_from_llm
from feedback.feedback import save_feedback, get_feedback  # import the feedback functions


# No need to create a new Flask app here

@app.route('/', methods=['GET', 'POST'])
def index():
    problem_description = ''  # Initialize outside if
    generated_code = ''
    if request.method == 'POST':
        problem_description = request.form.get('problem_description', '')
        generated_code = get_code_from_llm(problem_description)
    return render_template('index.html', submitted=request.method == 'POST', problem_description=problem_description,
                           generated_code=generated_code)


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    feedback_data = {
        'problem_description': request.form['problem_description'],
        'generated_code': request.form['generated_code'],
        'feedback': request.form['feedback']  # Assuming there's an input with name 'feedback'
    }
    save_feedback(feedback_data)
    return redirect(url_for('index'))  # Redirect back to the main page after submitting feedback
