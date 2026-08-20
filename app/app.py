from flask import Flask

app = Flask(__name__)

VERSION = "1.2.0"


@app.route("/")
def home():
    return f"Blue-Green Demo Application - Version {VERSION} - GREEN\n"


@app.route("/health")
def health():
    return "Health Check Failed\n", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
