import requests
from twilio.rest import Client
from creds import (
    account_sid,
    auth_token,
    twilio_phone_number,
    MAILGUN_DOMAIN,
    MAILGUN_API_KEY,
)
from lib.notification_templates import email_functions, text_functions

client = Client(account_sid, auth_token)


def send_email(to_email, subject, body):
    # mailgun_url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
    # mailgun_auth = ("api", MAILGUN_API_KEY)
    # mailgun_data = {
    #     "from": "ala@gmail.com",
    #     "to": to_email,
    #     "subject": subject,
    #     "html": body,
    # }

    # response = requests.post(mailgun_url, auth=mailgun_auth, data=mailgun_data)

    # print(f"Email sent with status code: {response.status_code} and {response.content}")
    print("EMAIL SENT")


def send_sms(client, recipient_phone_number, message_body):
    # message = client.messages.create(
    #     body=message_body, from_=twilio_phone_number, to=recipient_phone_number
    # )

    # print(f"Message SID: {message.sid}")
    print("TEXT SENT")


def email_notification(email_key, person, *args):
    generate_email = email_functions[email_key]
    subject, body = generate_email(person, *args)
    print(subject, body)
    send_email(person.email, subject, body)


def sms_notification(text_key, person, *args):
    generate_text = text_functions[text_key]
    body = generate_text(person, *args)
    print(body)
    send_sms(client, person.number, body)
