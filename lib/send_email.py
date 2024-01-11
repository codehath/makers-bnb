import requests
from creds import MAILGUN_DOMAIN, MAILGUN_API_KEY


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

def signup_email(person):
    subject = 'Welcome to MakersBnb'
    body = f'Thank you for signing up with MakersBnB. We are excited to have you on board!'
    send_email(person.email, subject, body)

def request_space_created(person, space):
    subject = 'Space Created'
    body = f'Congratulations! You have successfully created a space named {space.name}.'
    send_email(person.email, subject, body)

def request_space_updated(person, space):
    subject = 'Space Updated'
    body = f'The details of your space {space.name} have been updated. Check the changes and ensure they meet your requirements.'
    send_email(person.email, subject, body)

def request_to_book(person, space, booking):
    subject = 'Booking Request Received'
    if booking.start_date == booking.end_date:
        body = f'Thank you for your booking request for {space.name} on {booking.start_date}. We will review it shortly.'
    else:
        body = f'Thank you for your booking request for {space.name} from {booking.start_date} to {booking.end_date}. We will review it shortly.'
    send_email(personal.email, subject, body)

def booking_request_pending(person, space):
    subject = 'Your Booking Request is Pending!'
    body = f'Thank you for requesting to book {space.name} on [Your Platform]. The host will review your request shortly.'
    send_email(subject, body, person.email)

def booking_confirmed(person, space, booking):
    subject = 'Booking Confirmed'
    body = f'Congratulations! Your booking request for {space.name} on {booking.start_date} has been confirmed.'
    send_email(person.email, subject, body)

def booking_denied(perosn, space, booking):
    subject = 'Booking Denied'
    body = f'We regret to inform you that your booking request for {space.name} on {booking.start_date} has been denied.'
    send_email(person.email, subject, body)

def booking_request(person, space):
    subject = 'New Booking Request for Your Space!'
    body = f'You have received a booking request for your space ({space.name}) on [Your Platform]. Please review and respond.'
    send_email(subject, body, person.email)



