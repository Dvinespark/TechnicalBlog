from flask import render_template, request, redirect, url_for, session
from mongo.db_helper import MongoDB


def index():
    # db = MongoDB()
    # print(db.connection_string)
    # print(db.database_name)
    # print(db.mongo_client)
    #
    # # list databases
    # # print(db._db)
    # # for d in db.mongo_client.list_databases():
    # #     print(d)
    #
    # collection = db.get_collection("user")
    # result = collection.find({})
    # for document in result:
    #     print(document)
    context = {
        "login_flag": False,
        "user_admin": False,
        "username": None
    }
    login_flag = session.get('login_flag', False)
    username = session.get('username', None)
    if login_flag and username:
        return render_template("index.html", data=context)

    # session variables
    session["login_flag"] = False
    session["username"] = None
    session["signup_flag"] = False
    session["signup_message"] = None

    return render_template("signin.html", data=context)


def login():
    context = {
        "login_flag": False,
        "user_admin": False,
        "username": None,
        "login_message": ""
    }
    login_flag = session.get("login_flag", False)
    username = session.get("username", None)

    if request.method == "GET":
        print("Get method called.")
        if login_flag and username is not None:
            return redirect(url_for('index'))
        return render_template("signin.html", data=context)

    if request.method == "POST":
        print("Post method called")

        session["signup_flag"] = False
        session["signup_message"] = None

        username = request.form['username']
        password = request.form['password']
        # get data from db
        db = MongoDB()
        collection = db.get_collection("user")
        users = collection.find({})
        for user in users:
            if username == user['username'] and password == user["password"]:
                session["login_flag"] = True
                session["username"] = username
                session["admin_flag"] = False
                if user['type'] == "admin":
                    session["admin_flag"] = True
                return redirect(url_for('index'))
            else:
                session["login_flag"] = False
        # if username and password doesnot match
        context["login_message"] = "Incorrect username and password."
        return render_template("signin.html", data=context)


def logout():
    context = {
        "login_flag": False,
        "user_admin": False,
        "username": None
    }
    session["login_flag"] = False
    session["signup_flag"] = False
    session["signup_message"] = None

    return render_template("signin.html", data=context)


def register():
    """
    Create new user
    :return:
    """
    print("register post method called")
    context = {
        "login_flag": False,
        "user_admin": False,
        "username": None
    }
    session["login_flag"] = False
    username = request.form['username']
    password1 = request.form['password1']
    email = request.form['email']
    fullname = request.form['fullname']
    user_type = "normal"
    active = True
    # store information in mongodb
    try:
        db = MongoDB()
        user_coll = db.get_collection("user")
        users = user_coll.find({})
        print(users)
        print("working upto here")
        for user in users:
            if user["username"] == username:
                session["signup_message"] = "User already exists! Please create a new one with different user."
                session["signup_flag"] = False
                return {
                    "status_code": 201,
                    "message": "User already exists! Please create a new one with different user.",
                    "url": url_for("login")
                }
        user_coll.insert_one({
            "username": username,
            "password": password1,
            "email": email,
            "type": user_type,
            "active": active,
            "fullname": fullname
        })
        session["signup_flag"] = True
        session["signup_message"] = "User registered successfully. Please proceed login with the user"
        return {
            "status_code": 200,
            "message": "user created successfully.",
            "url": url_for("login")
        }
    except Exception as e:
        print(e)
        session["signup_flag"] = False
        session["signup_message"] = "Something went wrong. Please try again later."
        return {
            "status_code": 101,
            "message": "Something went wrong.",
            "url": url_for("login")
        }

# admin panel

def admin():

    context = {
        "login_flag": False,
        "user_admin": False,
        "username": None
    }
    login_flag = session.get('login_flag', False)
    username = session.get('username', None)
    admin_flag = session.get('admin_flag', False)
    if login_flag and username and admin_flag:
        return render_template("admin/admin.html", data=context)

    # session variables
    session["signup_flag"] = False
    session["signup_message"] = None
    session["login_flag"] = False
    context["login_message"] = "You have to be admin to access that page."
    return render_template("signin.html", data=context)


# list
def users():
    current_user = session.get('username', None)
    db = MongoDB()
    user_coll = db.get_collection("user")
    users = user_coll.find({'username': { "$ne": str(current_user) }})
    context = {
        "login_flag": False,
        "user_admin": False,
        "username": None,
        "users": users
    }
    return render_template("admin/users.html", data=context)


# delete user
def delete_user():
    context = {
        "login_flag": False,
        "user_admin": False,
        "username": None
    }
    username = request.form['username']
    db = MongoDB()
    user_coll = db.get_collection('user')
    user = user_coll.find_one_and_delete({"username": username})
    return {
        "status_code": 200,
        "message": "user deleted successfully.",
        "url": url_for("users")
    }