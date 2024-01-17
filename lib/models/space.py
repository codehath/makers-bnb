from peewee import *
from creds import *
from lib.models.person import Person

db = PostgresqlDatabase(db_name, user=user, password=password, host=host)


class Space(Model):
    id = AutoField()
    name = CharField()
    description = CharField()
    price = IntegerField()
    user_id = ForeignKeyField(Person)

    class Meta:
        database = db
