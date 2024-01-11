import requests
#from creds import MAILGUN_DOMAIN, MAILGUN_API_KEY

MAILGUN_API_KEY = '505fe23a102dbd5d37dd6d8f6c262c48-7ecaf6b5-0e4937a0'
MAILGUN_DOMAIN = 'sandbox8b4c55b97ded45258c9e7b59df25d875.mailgun.org'

def send_email(to_email, subject, body):
    mailgun_url = f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages'
    mailgun_auth = ('api', MAILGUN_API_KEY)
    mailgun_data = {
        'from': 'ala@gmail.com',
        'to': to_email,
        'subject': subject,
        'html': body
    }


    response = requests.post(mailgun_url, auth=mailgun_auth, data=mailgun_data)
    
    print(f"Email sent with status code: {response.status_code} and {response.content}")

def signup_email(user_email):
    subject = 'Welcome to MakersBnb'
    body = f'Thank you for signing up with MakersBnB. We are excited to have you on board!'
    send_email(user_email, subject, body)

def request_space_created(user_email, space_name):
    subject = 'Space Created'
    body = f'Congratulations! You have successfully created a space named {space_name}.'
    send_email(user_email, subject, body)

def request_space_updated(user_email, space_name):
    subject = 'Space Updated'
    body = f'The details of your space {space_name} have been updated. Check the changes and ensure they meet your requirements.'
    send_email(user_email, subject, body)

def request_to_book(user_email, space_name, start_date, end_date):
    subject = 'Booking Request Received'
    if start_date == end_date:
        body = f'Thank you for your booking request for {space_name} on {start_date}. We will review it shortly.'
    else:
        body = f'Thank you for your booking request for {space_name} from {start_date} to {end_date}. We will review it shortly.'
    send_email(user_email, subject, body)

def booking_request_pending(user_email, space_name):
    subject = 'Your Booking Request is Pending!'
    body = f'Thank you for requesting to book {space_name} on [Your Platform]. The host will review your request shortly.'
    send_email(subject, body, user_email)

def booking_confirmed(user_email, space_name, booking_date):
    subject = 'Booking Confirmed'
    body = f'Congratulations! Your booking request for {space_name} on {booking_date} has been confirmed.'
    send_email(user_email, subject, body)

def booking_denied(user_email, space_name, booking_date):
    subject = 'Booking Denied'
    body = f'We regret to inform you that your booking request for {space_name} on {booking_date} has been denied.'
    send_email(user_email, subject, body)

def booking_request(host_email, space_name):
    subject = 'New Booking Request for Your Space!'
    body = f'You have received a booking request for your space ({space_name}) on [Your Platform]. Please review and respond.'
    send_email(subject, body, host_email)



