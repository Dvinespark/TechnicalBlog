import datetime
from flask import render_template, request, redirect, url_for, session
from mongo.db_helper import MongoDB
import os
from werkzeug.utils import secure_filename

STATUS = {
    "success": 200,
    "error": 404,
}


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

    # start passing data to UI
    db = MongoDB()
    collection = db.get_collection("blogs")
    featured_blog = collection.find_one({"blog_type": "featured"})
    featured_blog_date = datetime.datetime.fromisoformat(featured_blog['created_at'])
    featured_blog['day'] = featured_blog_date.day
    featured_blog['month'] = featured_blog_date.strftime("%b")
    print(featured_blog)
    top_blog = collection.find({"blog_type": "top"}).limit(2)
    regular_blog = collection.find({"blog_type": "regular"}).limit(1)
    context = {
        "login_flag": False,
        "user_admin": False,
        "username": None,
        "featured_blog": featured_blog,
        "top_blog": top_blog,
        "regular_blog": regular_blog
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
    users = user_coll.find({'username': {"$ne": str(current_user)}})
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
    print("method called")
    print(request.form)
    print(request.files)
    # db.SOME_COLLECTION.find().sort({"_id": -1}).limit(1)
    db = MongoDB()
    blog_coll = db.get_collection("blogs")
    last_blog_id = 0
    try:
        last_blog_id = blog_coll.find({}, {"blog_id"}).sort("_id", -1).limit(1)[0]["blog_id"]
    except Exception as e:
        pass
    # do the logic to increment post_id
    blog_id = last_blog_id + 1

    current_user = session.get('username', None)
    login_flag = session.get('login_flag', False)
    data = {
        "created_by": current_user,
        "updated_by": None,
        "active": request.form.get('active', False),
        "title": request.form.get('title', None),
        "short_description": request.form.get('short_description', None),
        "long_description": request.form.get('long_description', None),
        "blog_id": blog_id,
        "photo_url": request.form.get("photo_url", None),
        "blog_type": request.form.get("blog_type", None),
        "blog_tech": request.form.get("blog_tech", None),
        "created_at": str(datetime.date.today()),
        "updated_at": None
    }
    if 'photo_url' in request.files:
        file = request.files['photo_url']
        import flask
        file_name = secure_filename(file.filename)
        file_name = file_name.split('.')[0].strip() + "_" + current_user + "_" + str(datetime.date.today()) + \
                    "." + file_name.split('.')[1]
        file.filename = file_name
        file_path = os.path.join(flask.current_app.root_path, 'static', 'img', 'blog', file_name)
        print(file_path)
        file.save(file_path)

        data['photo_url'] = file_name
    print(data)
    # check if user is logged in
    if current_user and login_flag:
        blog_coll.insert_one(data)
        return {
            "status_code": STATUS["success"],
            "message": "Blog created successfully.",
            "url": url_for("blogs")
        }

    else:
        return {
            "status_code": STATUS["error"],
            "message": "Sorry something went wrong. Please try again later.",
            "url": url_for("blogs")
        }


def blog_update():
    current_user = session.get('username', None)
    login_flag = session.get('login_flag', False)

    db = MongoDB()
    blog_coll = db.get_collection("blogs")

    blog_id = request.form['blog_id']
    active = request.form.get('active', True)
    short_description = request.form.get('short_description', None)
    long_description = request.form.get('long_description', None)
    blog_type = request.form.get('blog_type', "regular")
    blog_tech = request.form.get('blog_tech', "all")
    title = request.form.get('title', None)

    update_record = {
        "updated_by": current_user,
        "updated_at": str(datetime.date.today())
    }
    if active is not None:
        update_record["active"] = active

    if short_description is not None:
        update_record["short_description"] = short_description

    if request.form['long_description'] is not None:
        update_record["long_description"] = long_description

    if blog_type is not None:
        update_record["blog_type"] = blog_type

    if blog_tech is not None:
        update_record["blog_tech"] = blog_tech

    if title is not None:
        update_record["title"] = title

    if 'photo_url' in request.files:
        file = request.files['photo_url']
        import flask
        file_name = secure_filename(file.filename)
        file_name = file_name.split('.')[0].strip() + "_" + current_user + "_" + str(datetime.date.today()) + \
                    "." + file_name.split('.')[1]
        file.filename = file_name
        file_path = os.path.join(flask.current_app.root_path, 'static', 'img', 'blog', file_name)
        print(file_path)
        file.save(file_path)

        update_record['photo_url'] = file_name
    print(update_record)
    # check if user is logged in
    if current_user and login_flag:
        output = blog_coll.update({"blog_id": int(blog_id)}, {"$set": update_record})
        print(output)
        return {
            "status_code": STATUS["success"],
            "message": "Blog updated successfully.",
            "url": url_for("blogs")
        }

    else:
        return {
            "status_code": STATUS["error"],
            "message": "Sorry something went wrong. Please try again later.",
            "url": url_for("blogs")
        }


def blog_delete():
    blog_id = int(request.form['blog_id'])
    db = MongoDB()
    blog_coll = db.get_collection("blogs")
    # blog = blog_coll.find_one_and_delete({"blog_id": int(blog_id)})
    blog = blog_coll.delete_one({"blog_id": blog_id})
    return {
        "status_code": STATUS["success"],
        "message": "blog deleted successfully.",
        "db_message": str(blog),
        "url": url_for("blogs")
    }

# /admin/emails


def admin_emails():
    db = MongoDB()
    contact_coll = db.get_collection("contacts")
    emails = contact_coll.find({"responded": False})
    context = {
        "emails": emails
    }
    return render_template("admin/emails.html", data=context)


def admin_emails_update():
    current_user = session.get('username', None)
    login_flag = session.get('login_flag', False)

    db = MongoDB()
    contacts_coll = db.get_collection("contacts")

    id = request.form['id']
    responded = request.form.get('responded', 'false')
    if responded == 'false':
        responded = False
    else:
        responded = True
    update_record = {
        "updated_at": str(datetime.date.today())
    }
    if responded is not None:
        update_record["responded"] = responded


    # check if user is logged in
    if current_user and login_flag:
        output = contacts_coll.update({"id": int(id)}, {"$set": update_record})
        print(output)
        return {
            "status_code": STATUS["success"],
            "message": "Record updated successfully.",
            "url": url_for("admin-email")
        }

    else:
        return {
            "status_code": STATUS["error"],
            "message": "Sorry something went wrong. Please try again later.",
            "url": url_for("admin-email")
        }


def contact():
    message = None
    if request.method == "POST":
        db = MongoDB()
        blog_coll = db.get_collection("contacts")
        last_inserted_id = 0
        try:
            last_inserted_id = blog_coll.find({}, {"id"}).sort("_id", -1).limit(1)[0]["id"]
        except Exception as e:
            pass
        # do the logic to increment post_id
        contact_id = last_inserted_id + 1
        data = {
            "id": contact_id,
            "name": request.form.get('name', ''),
            "email": request.form.get('email', ''),
            "message": request.form.get('message'),
            "created_at": str(datetime.date.today()),
            "updated_at": '',
            "responded": False
        }
        blog_coll.insert_one(data)
        message = 'Your query has been submitted. Please allow our admins to reply in few hours!'
        return render_template("contact.html", data={'message': message})

    return render_template("contact.html", data={'message': message})


def about():
    return render_template("about.html", data={})