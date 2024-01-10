from twilio.rest import Client

account_sid = 'ACd5d7bda44df88fcdaeb7fea20e7b2747'
auth_token = '18d0d863dd7b2674527884d8d12a17e6'
twilio_phone_number = '+447400361560'
recipient_phone_number = '+447943092053' 

client = Client(account_sid, auth_token)

def send_booking_sms(client, recipient_phone_number,  message_body):
    message = client.messages.create(
        body=message_body,
        from_=twilio_phone_number,
        to=recipient_phone_number
    )

    print(f"Message SID: {message.sid}")

# booking_status, person_name, space_name, booking_date
def requested_text(person_name, space_name, booking_date):
    message_body = f"{person_name} has requested to book {space_name} on {booking_date}. Please review the request."
    send_booking_sms(client, person.Number, message_body)

def requested_text_confirmed(space_name, booking_date):
    message_body = f"Great news! Your booking request for {space_name} on {booking_date} has been confirmed. We look forward to welcoming you!"
    send_booking_sms(client, person.Number, message_body)

def requested_text_denied(space_name, booking_date):
    message_body = f"We regret to inform you that your booking request for {space_name} on {booking_date} has been denied. Please contact us for more information."
    send_booking_sms(client, person.Number, message_body)


    
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

