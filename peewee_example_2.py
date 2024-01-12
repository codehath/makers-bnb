import os, datetime
from lib.database_connection import get_flask_database_connection

from creds import *
from lib.person import *
from lib.availability import *
from lib.booking import *
from lib.space import *


# Define your Peewee database instance
db = PostgresqlDatabase(
    db_name,  # Your database name
    user=user,  # Your PostgreSQL username
    password=password,  # Your PostgreSQL password
    host=host,  # Your PostgreSQL host
)

# Connect to the database
db.connect()

db.drop_tables([Person, Space, Booking, Availability])
db.create_tables([Person, Space, Booking, Availability])

new_person = Person.create(name="John Doe", email="john@hotmail.com", password="password", number="07399155353")
new_person2 = Person.create(name="Bruce Wayne", email="troytolhurst@outlook.com", password="password", number="07500019238")
new_person3 = Person.create(name="Good Samaritan", email="goodsamiritan@gmail.com", password="password", number="07500019238")


# creating new space examples for db entry
new_space = Space.create(
    name="Test Home", description="Nice big house", price=500, user_id=new_person.id
)

new_space2 = Space.create(
    name="Test Home2", description="Nice big house2", price=100, user_id=new_person.id
)

new_space3 = Space.create(
    name="Test Home3", description="Nice big house3", price=250, user_id=new_person.id
)

new_space4 = Space.create(
    name="Test Home4", description="Nice big house4", price=750, user_id=new_person2.id
)

new_space5 = Space.create(
    name="Test Home5", description="Nice big house5", price=1000, user_id=new_person2.id
)

new_booking = Booking.create(
    space_id=new_space.id,
    start_date=datetime.date(2022, 1, 25),
    end_date=datetime.date(2022, 1, 28),
    user_id=new_person2.id,
)

new_availability = Availability.create(
    space_id=new_space.id,
    start_date=datetime.date(2022, 1, 25),
    end_date=datetime.date(2022, 1, 28),
)

# All houses above 500 in price
spaces_under_500 = Space.select().where(Space.price >= 500)

for space in spaces_under_500:
    print(space.name, space.description, space.price, space.user_id)
