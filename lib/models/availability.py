from peewee import *
from creds import *
from lib.models.space import Space
from lib.booking import *

db = PostgresqlDatabase(db_name, user=user, password=password, host=host)


class Availability(Model):
    id = AutoField()
    start_date = DateField()
    end_date = DateField()
    space_id = ForeignKeyField(Space)

    class Meta:
        database = db  # This model uses the "people.db" database.
