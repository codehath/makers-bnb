from lib.helper_methods import date_string


def signup_email(person):
    subject = "Welcome to MakersBnb"
    body = (
        f"Thank you for signing up with MakersBnB. We are excited to have you on board!"
    )
    return subject, body


# Host Emails
def new_space_email(person, space):
    subject = "Space Listed"
    body = f"Congratulations! You have successfully listed your space {space.name}."
    return subject, body


def space_updated_email(person, space):
    subject = "Space Updated"
    body = f"The details of your space {space.name} have been updated. Check the changes and ensure they meet your requirements."
    return subject, body


def new_request_email(person, space, booking):
    subject = "New Booking Request for Your Space!"
    body = f"You have received a booking request for your space {space.name} {date_string(booking)}. Please review and respond."
    return subject, body


def request_approved_email(person, space, booking):
    subject = "Booking Request Approved!"
    body = f"You have approved the booking request for {space.name} {date_string(booking)}."
    return subject, body


# Guest Emails
def new_booking_email(person, space, booking):
    subject = "Booking Request Received"
    body = f"Thank you for requesting to book {space.name} {date_string(booking)}. The host will review your request shortly."
    return subject, body


def booking_confirmed_email(person, space, booking):
    subject = "Booking Confirmed"
    body = f"Congratulations! Your booking request for {space.name} {date_string(booking)} has been confirmed."
    return subject, body


def booking_denied_email(person, space, booking):
    subject = "Booking Denied"
    body = f"We regret to inform you that your booking request for {space.name} {date_string(booking)} has been denied."
    return subject, body


email_functions = {
    "signup": signup_email,
    "new_space": new_space_email,
    "space_updated": space_updated_email,
    "new_request": new_request_email,
    "request_approved": request_approved_email,
    "new_booking": new_booking_email,
    "booking_confirmed": booking_confirmed_email,
    "booking_denied": booking_denied_email,
}


def request_text(person, space, booking):
    message_body = f"{person.name} has requested to book {space.name} {date_string(booking)}. Please review the request."
    return message_body


def booking_confirmed_text(person, space, booking):
    message_body = f"Great news! Your booking request for {space.name} {date_string(booking)} has been confirmed. We look forward to welcoming you!"
    return message_body


def booking_denied_text(person, space, booking):
    message_body = f"We regret to inform you that your booking request for {space.name} {date_string(booking)} has been denied. Please contact us for more information."
    return message_body


text_functions = {
    "request": request_text,
    "booking_confirmed": booking_confirmed_text,
    "booking_denied": booking_denied_text,
}
