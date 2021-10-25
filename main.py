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

# /register post method only
app.add_url_rule('/register', 'register', view_func=views.register, methods=["POST"])


# /admin for all those crud operations
app.add_url_rule('/admin', 'admin', view_func=views.admin, methods=["GET"])

# users
app.add_url_rule('/admin/users', 'users', view_func=views.users, methods=["GET"])

# delete users
app.add_url_rule('/admin/users/delete', 'delete-user', view_func=views.delete_user, methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)
