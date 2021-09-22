from flask import Flask, render_template
app = Flask(__name__, template_folder='html')

# Routes


@app.route("/")
def index():
    return render_template('index.html')


# Running the app directly from Python
if __name__ == "__main__":
    app.run(debug=True, port=3000)
