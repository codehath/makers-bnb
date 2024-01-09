from peewee import *
from creds import *
from lib.person import Person
from lib.space import Space

db = PostgresqlDatabase(db_name, user=user, password=password, host=host)


class Booking(Model):
    id = AutoField()
    space_id = ForeignKeyField(Space)
    start_date = DateField()
    end_date = DateField()
    approved = BooleanField(default=False)
    user_id = ForeignKeyField(Person)
    response = BooleanField(default=False)

    class Meta:
        database = db
