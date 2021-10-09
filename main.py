from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return "App is running..."


if __name__ == "__name__":
    app.run()
