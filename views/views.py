from flask import render_template, request


def index():
    print(request)
    context = {
        'name': "subash"
    }
    return render_template("index.html", data=context)