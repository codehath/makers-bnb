import json

with open("credentials.json") as f:
    credentials = json.load(f)

user = credentials["user"]
password = credentials["pass"]
host = credentials["host"]
db_name = credentials["db_name"]
test_db_name = credentials["test_db_name"]
