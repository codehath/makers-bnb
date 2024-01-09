from peewee import *
from creds import *

db = PostgresqlDatabase(db_name, user=user, password=password, host=host)


class Space(Model):
    id = AutoField()
    name = CharField()
    description = CharField()
    price = IntegerField()
    user_id = IntegerField()

    class Meta:
        database = db
