from flask import Flask
from views import views
from config import flask_secret_key

app = Flask(__name__, static_url_path='/static')
app.config["UPLOAD_FOLDER"] = "static/img/blog/"

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


# 1 blogs list
app.add_url_rule('/admin/blogs', 'blogs', view_func=views.blog_list, methods=["GET"])

# 2 create
app.add_url_rule('/admin/blogs/create', 'create-blog', view_func=views.blog_create, methods=["POST"])

# 3 delete
app.add_url_rule('/admin/blogs/delete', 'delete-blog', view_func=views.blog_delete, methods=["POST"])

# 4 update
app.add_url_rule('/admin/blogs/edit', 'edit-blog', view_func=views.blog_update, methods=["POST"])

# 5 admin Emails list
app.add_url_rule('/admin/emails', 'admin-email', view_func=views.admin_emails, methods=["GET"])

# admin email update

app.add_url_rule('/admin/emails/edit', 'email-update', view_func=views.admin_emails_update, methods=["POST"])

# /contact
app.add_url_rule('/contact', 'contact', view_func=views.contact, methods=["GET", "POST"])

# /about
app.add_url_rule('/about', 'about', view_func=views.about, methods=["GET"])


# /mobile_blogs
app.add_url_rule('/admin/mobile_blogs', 'mobile_blogs', view_func=views.mobile_blogs_list, methods=["GET"])

# 2 create
app.add_url_rule('/admin/mobile_blogs/create', 'create-mobile_blogs', view_func=views.mobile_blogs_create, methods=["POST"])

# 3 delete
app.add_url_rule('/admin/mobile_blogs/delete', 'delete-mobile_blogs', view_func=views.mobile_blogs_delete, methods=["POST"])

# 4 update
app.add_url_rule('/admin/mobile_blogs/edit', 'edit-mobile_blogs', view_func=views.mobile_blogs_update, methods=["POST"])




# 5 blog detail
app.add_url_rule('/blog/detail/<int:blog_id>', 'blog_detail', view_func=views.blog_detail, methods=["GET"])

# comment in blog
app.add_url_rule('/blog/comment', 'blog_comment', view_func=views.blog_comment, methods=["POST"])

# 5 admin comment list
app.add_url_rule('/admin/comments', 'admin-comments', view_func=views.admin_comments, methods=["GET"])

# admin email update

app.add_url_rule('/admin/comment/edit', 'comment-update', view_func=views.admin_comment_update, methods=["POST"])


# /electronics_blog
app.add_url_rule('/admin/electronics_blog', 'electronics_blog', view_func=views.electronics_blog_list, methods=["GET"])

# 2 create
app.add_url_rule('/admin/electronics_blog/create', 'create-electronics_blog', view_func=views.electronics_blog_create, methods=["POST"])

# 3 delete
app.add_url_rule('/admin/electronics_blog/delete', 'delete-electronics_blog', view_func=views.electronics_blog_delete, methods=["POST"])

# 4 update
app.add_url_rule('/admin/electronics_blog/edit', 'edit-electronics_blog', view_func=views.electronics_blog_update, methods=["POST"])

if __name__ == "__main__":
    app.run(debug=True)
