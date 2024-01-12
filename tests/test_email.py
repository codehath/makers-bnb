# test_email.py
from lib.send_email import send_signup_email

def main():
    # Test data
    user_email = 'ala78698@hotmail.co.uk'
    space_name = 'Oval'
    booking_date = '2024-01-15'

    recipient_email = 'ala78698@hotmail.co.uk'
    subject = 'Welcome to MakersBnB'
    body = '<p>This is a test email.</p>'
    send_signup_email(user_email)

if __name__ == "__main__":
    main()
