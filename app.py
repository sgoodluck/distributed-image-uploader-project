from flask import Flask

# Instantiate App
app = Flask(__name__)

# Setup Home Route
@app.route("/")
def home():
    return "Hello this is a flask endpoint!"

if __name__ == "__main__":
    app.run(debug=True)