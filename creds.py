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
account_sid = credentials["account_sid"]
auth_token = credentials["auth_token"]
twilio_phone_number = credentials["twilio_phone_number"]
recipient_phone_number = credentials["recipient_phone_number"]
MAILGUN_API_KEY = credentials["MAILGUN_API_KEY"]
MAILGUN_DOMAIN = credentials["MAILGUN_DOMAIN"]
