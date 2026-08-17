from flask import Flask

app = Flask(__name__)

VERSION = "1.0.0"


@app.route("/")
def home():
    return f"Blue-Green Demo Application - Version {VERSION}\n"


@app.route("/health")
def health():
    return "OK\n"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
