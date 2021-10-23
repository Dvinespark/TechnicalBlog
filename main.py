from flask import Flask
from views import views
from config import flask_secret_key

app = Flask(__name__, static_url_path='/static')
app.secret_key = flask_secret_key
# / home page
app.add_url_rule('/', 'index', view_func=views.index)

# login or register url
# /login get and post method
app.add_url_rule('/login', 'login', view_func=views.login, methods=["GET", "POST"])

# /logout get method
app.add_url_rule('/logout', 'logout', view_func=views.logout)

if __name__ == "__main__":
    app.run(debug=True)
