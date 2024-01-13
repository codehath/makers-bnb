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

# Seed data for person table
persons_data = [
    {"name": "John Doe", "email": "john@example.com", "password": "password", "number": "00000000000"},
    {"name": "Bruce Wayne", "email": "bruce@example.com", "password": "password", "number": "00000000000"},
    {"name": "Jane Doe", "email": "jane@example.com", "password": "password123", "number": "00000000000"},
    {"name": "Alice Smith", "email": "alice@example.com", "password": "secret", "number": "00000000000"},
    {"name": "Bob Johnson", "email": "bob@example.com", "password": "pass123", "number": "00000000000"},
    {"name": "Eve Wilson", "email": "eve@example.com", "password": "securepass", "number": "00000000000"},
    {"name": "Charlie Brown", "email": "charlie@example.com", "password": "mysecret", "number": "00000000000"},
]

# Seed data for spaces
spaces_data = [
    {
        "name": "Cozy Cabin",
        "description": "A small cabin in the woods",
        "price": 20,
        "user_id": 1,
    },
    {
        "name": "City Apartment",
        "description": "Modern apartment in the heart of the city",
        "price": 80,
        "user_id": 2,
    },
    {
        "name": "Beach House",
        "description": "Beautiful house with ocean view",
        "price": 100,
        "user_id": 2,
    },
    {
        "name": "Mountain Retreat",
        "description": "Secluded retreat in the mountains",
        "price": 60,
        "user_id": 1,
    },
    {
        "name": "Urban Loft",
        "description": "Chic loft in a trendy neighborhood",
        "price": 70,
        "user_id": 1,
    },
]

# Seed data for availabilities
availabilities_data = [
    {
        "space_id": 1,
        "start_date": datetime.date(2024, 1, 15),
        "end_date": datetime.date(2024, 2, 28),
    },
    {
        "space_id": 2,
        "start_date": datetime.date(2024, 3, 1),
        "end_date": datetime.date(2024, 3, 31),
    },
    {
        "space_id": 3,
        "start_date": datetime.date(2024, 4, 5),
        "end_date": datetime.date(2024, 4, 25),
    },
    {
        "space_id": 4,
        "start_date": datetime.date(2024, 5, 20),
        "end_date": datetime.date(2024, 5, 25),
    },
    {
        "space_id": 5,
        "start_date": datetime.date(2024, 4, 1),
        "end_date": datetime.date(2024, 6, 30),
    },
]

# Seed data for bookings
bookings_data = [
    {
        "space_id": 1,
        "start_date": datetime.date(2024, 1, 29),
        "end_date": datetime.date(2024, 1, 31),
        "user_id": 4,
    },
    {
        "space_id": 1,
        "start_date": datetime.date(2024, 2, 5),
        "end_date": datetime.date(2024, 2, 8),
        "user_id": 1,
    },
    {
        "space_id": 1,
        "start_date": datetime.date(2024, 2, 15),
        "end_date": datetime.date(2024, 2, 18),
        "user_id": 2,
    },
    {
        "space_id": 1,
        "start_date": datetime.date(2024, 2, 25),
        "end_date": datetime.date(2024, 2, 28),
        "user_id": 7,
    },
    {
        "space_id": 2,
        "start_date": datetime.date(2024, 3, 5),
        "end_date": datetime.date(2024, 3, 8),
        "user_id": 2,
    },
    {
        "space_id": 2,
        "start_date": datetime.date(2024, 3, 15),
        "end_date": datetime.date(2024, 3, 18),
        "user_id": 3,
    },
    {
        "space_id": 2,
        "start_date": datetime.date(2024, 3, 25),
        "end_date": datetime.date(2024, 3, 28),
        "user_id": 3,
    },
    {
        "space_id": 3,
        "start_date": datetime.date(2024, 4, 5),
        "end_date": datetime.date(2024, 4, 8),
        "user_id": 4,
    },
    {
        "space_id": 3,
        "start_date": datetime.date(2024, 4, 15),
        "end_date": datetime.date(2024, 4, 18),
        "user_id": 6,
    },
    {
        "space_id": 5,
        "start_date": datetime.date(2024, 4, 25),
        "end_date": datetime.date(2024, 6, 28),
        "user_id": 1,
    },
]


# Bulk create records in tables
with db.atomic():  # Ensures all operations are treated as a single transaction
    Person.bulk_create([Person(**data) for data in persons_data])
    Space.bulk_create([Space(**data) for data in spaces_data])
    Availability.bulk_create([Availability(**data) for data in availabilities_data])
    Booking.bulk_create([Booking(**data) for data in bookings_data])
