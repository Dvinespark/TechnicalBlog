from flask import render_template, request
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
        'name': "subash"
    }
    return render_template("index.html", data=context)