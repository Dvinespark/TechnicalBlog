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
        print(session)
        return render_template("index.html", data=context)
    session["login_flag"] = False
    session["username"] = None
    return render_template("signin.html", data=context)


def login():
    context = {
        "login_flag": False,
        "user_admin": False,
        "username": None
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
        username = request.form['username']
        password = request.form['password']

        if username and password:
            session["login_flag"] = True
            session["username"] = username
            return redirect(url_for('index'))
            # return render_template('index.html', data=context)
        return "something went wrong"


def logout():
    context = {
        "login_flag": False,
        "user_admin": False,
        "username": None
    }
    session["login_flag"] = False

    return render_template("signin.html", data=context)
