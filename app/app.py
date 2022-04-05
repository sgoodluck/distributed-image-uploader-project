from flask import Flask
import socket

# Instantiate App
app = Flask(__name__)

# Setup Home Route
@app.route("/")
def home():
    return f"Hello this is a flask endpoint! Container ID: {socket.gethostname()}"

if __name__ == "__main__":
    app.run(debug=True)