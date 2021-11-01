import datetime

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
    # checks for admin
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

# Blog Part here


# 1 comment
def comment_list():
    comment_data = {
        "username": "username",
        "blog_id": "blog_id",
        "comment": "comment",
        "active": True
    }


def comment_create():
    pass


def comment_delete():
    pass


# 2 blog
def blog_list():
    # blog_data = {
    #     "blog_id": password1,
    #     "small_description": email,
    #     "active": True,
    #     "long_description": active,
    #     "photo_url": fullname,
    #     "blog_type": "feature",  # default type will be normal
    #     "blog_technology": "mobile", # desktop, science, all
    #     "inserted_date": today date,
    #     "updated_date": None,
    #     "created_by": username,
    #     "updated_by": username
    # }

    # do the admin check if admin then do the following

    db = MongoDB()
    blog_coll = db.get_collection("blogs")
    blogs = blog_coll.find({})
    context = {
        "blogs": blogs
    }
    return render_template("admin/blog.html", data=context)


def blog_create():
    # db.SOME_COLLECTION.find().sort({"_id": -1}).limit(1)
    db = MongoDB()
    blog_coll = db.get_collection("blogs")
    last_blog = blog_coll.find({}, {"_id", "post_id"}).sort({"_id": -1}).limit(1)
    # do the logic to increment post_id
    blog_id = 1

    current_user = session.get('username', None)
    login_flag = session.get('login_flag', False)

    if current_user and login_flag:
        blog_coll.insert_one({
            "created_by": current_user,
            "updated_by": None,
            "active": True,
            "small_description": request.form['small_description'],
            "long_description": request.form['long_description'],
            "blog_id": blog_id,
            "photo_url": request.form["photo_url"],
            "blog_type": request.form["blog_type"],
            "blog_tech": request.form["blog_technology"],
            "inserted_date": str(datetime.date.today()),
            "updated_date": None
        })

    else:
        message = "Sorry you're not logged in. Only logged in users are allowed to do this."



def blog_update():
    pass


def blog_delete():
    pass
