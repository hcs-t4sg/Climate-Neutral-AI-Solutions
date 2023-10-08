from flask import Flask, render_template, request
from helpers import get_sol

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/proposal', methods=["POST"])
def proposal():
    prompt = request.form["prompt"]
    # proposal = get_sol(prompt)
    proposal = get_sol(prompt)
    return render_template("proposal.html", proposal=proposal)


if __name__ == "__main__":
    app.run(debug=True)


