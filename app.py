from flask import Flask, request, jsonify, render_template
from helpers import get_sol

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('input_form.html')

@app.route('/get_solution', methods=['POST'])
def get_solution():
    question = str(request.form.get('question'))  # Get question from the form submission
    
    # Check if question is None or not a string type
    if not question or not isinstance(question, str):
        return render_template('result.html', answer="Please submit a valid question.")
    
    # Use the question as you did before
    answer = get_sol(question)
    return render_template('result.html', answer=answer)


if __name__ == "__main__":
    app.run(debug=True)

