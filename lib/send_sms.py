from twilio.rest import Client
from creds import *

client = Client(account_sid, auth_token)

def send_booking_sms(client, recipient_phone_number,  message_body):
    message = client.messages.create(
        body=message_body,
        from_=twilio_phone_number,
        to=recipient_phone_number
    )

    print(f"Message SID: {message.sid}")

# booking_status, person_name, space_name, booking_date
def requested_text(person, space, booking):
    message_body = f"{person.name} has requested to book {space.name} on {booking.start_date}. Please review the request."
    send_booking_sms(client, person.phone_number, message_body)

def requested_text_confirmed(space, booking):
    message_body = f"Great news! Your booking request for {space.name} on {booking.start_date} has been confirmed. We look forward to welcoming you!"
    send_booking_sms(client, person.phone_number, message_body)

def requested_text_denied(space, booking):
    message_body = f"We regret to inform you that your booking request for {space.name} on {booking.start_date} has been denied. Please contact us for more information."
    send_booking_sms(client, person.phone_number, message_body)


    
# Test Data
person_name = "Mohammed Miah"
space_name = "Oval"
booking_date = "2024-01-15"
booking_status_requested = "requested"
booking_status_confirmed = "confirmed"
booking_status_denied = "denied"

# Testing with different statuses
#send_booking_sms(client, recipient_phone_number, booking_status_requested, person_name, space_name, booking_date)
#send_booking_sms(client, recipient_phone_number, booking_status_confirmed, person_name, space_name, booking_date)
#send_booking_sms(client, recipient_phone_number, booking_status_denied, person_name, space_name, booking_date)

