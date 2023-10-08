from flask import Flask
from helpers import get_sol
import os
from secret import OPENAI_API_KEY

app = Flask(__name__)
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


@app.route('/')
def index():
    query = {"company_type": "technology", "target": "materials"}
    answer = get_sol(query)
    return f'{answer}'

if __name__ == "__main__":
    app.run(debug=True)


