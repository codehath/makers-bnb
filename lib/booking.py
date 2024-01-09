from peewee import *
from creds import *

db = PostgresqlDatabase(db_name, user=user, password=password, host=host)


class Booking(Model):
    id = AutoField()
    space_id = IntegerField()
    start_date = DateField()
    end_date = DateField()
    approved = BooleanField(default=False)
    user_id = IntegerField()

    class Meta:
        database = db
