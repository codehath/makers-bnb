import json
import os

# Had to put this in to avoid the tests breaking
path = os.getcwd()
index = path.index("bnb")
path = path[: index + 3] + "/credentials.json"

with open(path) as f:
    credentials = json.load(f)

user = credentials["user"]
password = credentials["pass"]
host = credentials["host"]
db_name = credentials["db_name"]
test_db_name = credentials["test_db_name"]
MAILGUN_API_KEY = credentials["MAILGUN_API_KEY"]
MAILGUN_DOMAIN = credentials["MAILGUN_DOMAIN"]
