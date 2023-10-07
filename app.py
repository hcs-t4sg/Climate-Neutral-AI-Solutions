# from flask import Flask

# app = Flask(__name__)


# @app.route('/')
# def index():
#     return 'Hello, World!'

# if __name__ == "__main__":
#     app.run(debug=True)

# from flask import Flask, request, jsonify
# from helpers import get_sol

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return 'Hello, World!'

# @app.route('/ask', methods=['POST'])
# def ask():
#     data = request.json
#     query = data.get('query')
#     if not query:
#         return jsonify({"error": "No query provided"}), 400

#     answer = get_sol(query)
#     return jsonify({"answer": answer})

# if __name__ == "__main__":
#     app.run(debug=True)


# from flask import Flask, request, jsonify
# from helpers import get_sol

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return 'Hello, World!'

# @app.route('/get_solution', methods=['GET'])
# def get_solution():
#     data = request.json
#     if not data or 'question' not in data:
#         return jsonify({"error": "No question provided."}), 400

#     question = data['question']
#     solution = get_sol(question)
#     return jsonify({"answer": solution})

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)

from flask import Flask, request, jsonify, render_template
from helpers import get_sol

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('input_form.html')

# @app.route('/get_solution', methods=['POST'])
# def get_solution():
#     question = request.form.get('question')  # Get question from the form submission
    
#     if not question:
#         return render_template('result.html', answer="Please submit a valid question.")
    
#     # Use the question as you did before
#     answer = get_sol(question)
#     return render_template('result.html', answer=answer["answer"])

@app.route('/get_solution', methods=['POST'])
def get_solution():
    question = str(request.form.get('question'))  # Get question from the form submission
    
    # Check if question is None or not a string type
    if not question or not isinstance(question, str):
        return render_template('result.html', answer="Please submit a valid question.")
    
    # Use the question as you did before
    answer = get_sol(question)
    return render_template('result.html', answer=answer["answer"])


if __name__ == "__main__":
    app.run(debug=True)

