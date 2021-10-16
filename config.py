db_credentials = {
    "conn_string": "mongodb+srv://{0}:{1}@techdb.4qbal.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl"
                   "=true&ssl_cert_reqs=CERT_NONE",
    "db_name": "TechDB",
    "db_user": "techUser",
    "db_password": "Technical123"

}
db_connection_string = db_credentials["conn_string"].format(db_credentials["db_user"], db_credentials["db_password"])
