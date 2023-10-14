from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # process form data here
        form_data = request.form
        message = "Form received. Here are the details: <br>"
        for key, value in form_data.items():
            if value and value != '\n':
                message += f"{key}: {value} <br>"
        return message
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)


