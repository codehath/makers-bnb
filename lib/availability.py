from peewee import *
from creds import *

db = PostgresqlDatabase(db_name, user=user, password=password, host=host)


class Availability(Model):
    id = AutoField()
    space_id = IntegerField()
    start_date = DateField()
    end_date = DateField()

    class Meta:
        database = db  # This model uses the "people.db" database.
