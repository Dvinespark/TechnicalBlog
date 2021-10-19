from flask import Flask
from views import views

app = Flask(__name__, static_url_path='/static')

app.add_url_rule('/', 'index', view_func=views.index)

if __name__ == "__main__":
    app.run(debug=True)
